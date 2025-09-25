import os
import time
import datetime
import schedule
from typing import Dict, List, Any, Optional

from .config_loader import ConfigLoader
from .youtube_api import YouTubeAPI
from .lemmy_api import LemmyAPI
from .video_filter import VideoFilter
from .logger import BotLogger

class SimpleBot:
    """
    Main bot class that coordinates YouTube video fetching, filtering, and posting to Lemmy
    """
    
    def __init__(self, config_dir: str = "../config", log_dir: str = "../logs"):
        """
        Initialize the bot
        
        Args:
            config_dir: Directory containing configuration files
            log_dir: Directory to store log files
        """
        # Load configurations
        self.config_loader = ConfigLoader(config_dir)
        self.config_loader.load_all_configs()
        
        # Get operation config
        operation_config = self.config_loader.get_operation_config()
        log_level = operation_config.get('log_level', 'INFO')
        
        # Set up logger
        self.logger_manager = BotLogger(log_dir, log_level)
        self.logger = self.logger_manager.get_logger()
        
        # Initialize APIs and components
        self.init_components()
        
    def init_components(self) -> None:
        """
        Initialize bot components (APIs, filters, etc.)
        """
        try:
            # Get configurations
            youtube_config = self.config_loader.get_youtube_config()
            lemmy_config = self.config_loader.get_lemmy_config()
            scoring_config = self.config_loader.get_scoring_config()
            
            # Initialize YouTube API
            api_key = youtube_config.get('api_key')
            if not api_key or api_key == "YOUR_YOUTUBE_API_KEY":
                self.logger.error("YouTube API key not configured")
                self.youtube_api = None
            else:
                self.youtube_api = YouTubeAPI(api_key)
                
            # Initialize Lemmy API
            instance_url = lemmy_config.get('instance_url')
            username = lemmy_config.get('username')
            password = lemmy_config.get('password')
            community = lemmy_config.get('community')
            
            if not instance_url or instance_url == "https://lemmy.example.com" or \
               not username or username == "YOUR_USERNAME" or \
               not password or password == "YOUR_PASSWORD" or \
               not community or community == "YOUR_COMMUNITY":
                self.logger.error("Lemmy credentials not configured")
                self.lemmy_api = None
                self.community_id = None
            else:
                self.lemmy_api = LemmyAPI(instance_url, username, password)
                self.community_id = self.lemmy_api.get_community_id(community)
                
            # Initialize video filter
            self.video_filter = VideoFilter(
                self.config_loader.keywords,
                scoring_config
            )
            
            # Set up configuration values
            self.check_interval_minutes = youtube_config.get('check_interval_minutes', 60)
            self.lookback_hours = youtube_config.get('lookback_hours', 24)
            self.check_duplicate_days = lemmy_config.get('check_duplicate_days', 7)
            
        except Exception as e:
            self.logger.error(f"Error initializing bot components: {e}")
            
    def get_lookback_time(self) -> datetime.datetime:
        """
        Get the datetime to look back to for videos
        
        Returns:
            Datetime object representing the lookback time
        """
        return datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=self.lookback_hours)
        
    def fetch_channel_videos(self, channel: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Fetch videos from a channel
        
        Args:
            channel: Channel configuration dictionary
            
        Returns:
            List of video information dictionaries
        """
        if not self.youtube_api:
            self.logger.error("YouTube API not initialized")
            return []
            
        channel_id = channel.get('channelID')
        channel_name = channel.get('name')
        
        if not channel_id:
            self.logger.error(f"Channel ID not found for channel: {channel_name}")
            return []
            
        self.logger.info(f"Fetching videos for channel: {channel_name} ({channel_id})")
        
        lookback_time = self.get_lookback_time()
        videos = self.youtube_api.get_channel_videos(channel_id, lookback_time)
        
        self.logger.info(f"Found {len(videos)} videos for channel {channel_name} since {lookback_time}")
        
        # Add channel information to videos
        for video in videos:
            video['channel_info'] = channel
            
        return videos
        
    def process_videos(self) -> None:
        """
        Process videos from all configured channels
        """
        if not self.youtube_api or not self.lemmy_api or not self.community_id:
            self.logger.error("Bot not fully initialized. Check configuration.")
            return
            
        self.logger.info("Starting video processing")
        
        all_videos = []
        
        # Fetch videos from all channels
        for channel in self.config_loader.channels:
            channel_videos = self.fetch_channel_videos(channel)
            all_videos.extend(channel_videos)
            
        self.logger.info(f"Fetched {len(all_videos)} videos in total")
        
        # Filter videos
        filtered_videos = self.video_filter.filter_videos(all_videos)
        self.logger.info(f"{len(filtered_videos)} videos passed filtering")
        
        # Post videos to Lemmy
        posted_count = 0
        for video in filtered_videos:
            if self.post_video_to_lemmy(video):
                posted_count += 1
                
        self.logger.info(f"Posted {posted_count} videos to Lemmy")
        
    def post_video_to_lemmy(self, video: Dict[str, Any]) -> bool:
        """
        Post a video to Lemmy
        
        Args:
            video: Video information dictionary
            
        Returns:
            True if posting was successful, False otherwise
        """
        if not self.lemmy_api or not self.community_id:
            self.logger.error("Lemmy API not initialized")
            return False
            
        snippet = video.get('snippet', {})
        video_id = video.get('id')
        title = snippet.get('title', '')
        description = snippet.get('description', '')
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Check if the video has already been posted
        if self.lemmy_api.is_url_already_posted(self.community_id, url, self.check_duplicate_days):
            self.logger.info(f"Video already posted: {title}")
            return False
            
        # Create post title
        channel_info = video.get('channel_info', {})
        channel_name = channel_info.get('name', 'Unknown Channel')
        primary_series_tag = channel_info.get('primary_series_tag', '')
        
        # Add series tag if available
        post_title = f"[{primary_series_tag}] {title}" if primary_series_tag else title
        
        # Add live indicator if it's a live stream
        if self.youtube_api.is_live_stream(video):
            post_title = f"[LIVE] {post_title}"
            
        # Truncate title if too long (Lemmy might have title length limits)
        if len(post_title) > 200:
            post_title = post_title[:197] + "..."
            
        # Create post body with video information and matched keywords
        filter_data = video.get('filter_data', {})
        score = filter_data.get('score', 0)
        matched_keywords = filter_data.get('matched_keywords', {})
        
        body = f"Channel: {channel_name}\n\n"
        
        # Add video description (truncated)
        if description:
            max_desc_length = 500
            truncated_desc = description[:max_desc_length] + "..." if len(description) > max_desc_length else description
            body += f"Description:\n{truncated_desc}\n\n"
            
        # Add matched keywords info (for debugging, can be removed in production)
        body += f"Video score: {score}\n\n"
        
        if matched_keywords.get('top_keywords'):
            body += f"Top keywords: {', '.join(matched_keywords['top_keywords'])}\n"
        if matched_keywords.get('other_keywords'):
            body += f"Other keywords: {', '.join(matched_keywords['other_keywords'])}\n"
        if matched_keywords.get('negative_keywords'):
            body += f"Negative keywords: {', '.join(matched_keywords['negative_keywords'])}\n"
            
        # Post to Lemmy
        try:
            self.logger.info(f"Posting video: {post_title}")
            post_result = self.lemmy_api.create_post(self.community_id, post_title, url, body)
            
            if post_result:
                self.logger.info(f"Successfully posted video: {post_title}")
                return True
            else:
                self.logger.error(f"Failed to post video: {post_title}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error posting video: {e}")
            return False
            
    def run_once(self) -> None:
        """
        Run the bot once
        """
        self.logger.info("Running bot in single run mode")
        self.process_videos()
        
    def run_continuously(self) -> None:
        """
        Run the bot continuously at scheduled intervals
        """
        self.logger.info(f"Running bot in continuous mode (checking every {self.check_interval_minutes} minutes)")
        
        # Run once immediately
        self.process_videos()
        
        # Schedule regular runs
        schedule.every(self.check_interval_minutes).minutes.do(self.process_videos)
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(1)
            
    def run(self) -> None:
        """
        Run the bot based on configured mode
        """
        operation_config = self.config_loader.get_operation_config()
        mode = operation_config.get('mode', 'single_run')
        
        if mode == 'continuous':
            self.run_continuously()
        else:
            self.run_once()