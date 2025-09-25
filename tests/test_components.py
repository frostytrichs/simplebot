#!/usr/bin/env python3
import os
import sys
import json
import yaml
from datetime import datetime, timedelta

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config_loader import ConfigLoader
from src.youtube_api import YouTubeAPI
from src.video_filter import VideoFilter

def test_config_loader():
    """Test the ConfigLoader class"""
    print("Testing ConfigLoader...")
    
    config_loader = ConfigLoader("../config")
    config_loader.load_all_configs()
    
    # Check if configurations were loaded
    print("Main config loaded:", bool(config_loader.config))
    print("Channels loaded:", len(config_loader.channels))
    print("Keywords loaded:", len(config_loader.keywords))
    
    # Print some config values
    print("\nYouTube config:")
    youtube_config = config_loader.get_youtube_config()
    for key, value in youtube_config.items():
        print(f"  {key}: {value}")
        
    print("\nScoring config:")
    scoring_config = config_loader.get_scoring_config()
    for key, value in scoring_config.items():
        print(f"  {key}: {value}")
        
    print("\nChannels:")
    for channel in config_loader.channels:
        print(f"  {channel.get('name')} ({channel.get('channelID')})")
        
    print("\nKeyword categories:")
    for category, keywords in config_loader.keywords.items():
        print(f"  {category}: {len(keywords)} keywords")
        
    return config_loader

def test_youtube_api(api_key):
    """Test the YouTubeAPI class"""
    print("\nTesting YouTubeAPI...")
    
    if not api_key or api_key == "YOUR_YOUTUBE_API_KEY":
        print("No YouTube API key provided. Skipping YouTube API test.")
        return None
        
    youtube_api = YouTubeAPI(api_key)
    
    # Test getting channel videos
    channel_id = "UC-yHapH6mW1ceZ_5PDUf1_g"  # GT World channel from channels.json
    published_after = datetime.now() - timedelta(days=7)  # Last 7 days
    
    print(f"Fetching videos for channel {channel_id} since {published_after}...")
    videos = youtube_api.get_channel_videos(channel_id, published_after)
    
    print(f"Found {len(videos)} videos")
    
    # Print details of the first few videos
    for i, video in enumerate(videos[:3]):
        if i >= len(videos):
            break
            
        snippet = video.get('snippet', {})
        video_id = video.get('id')
        title = snippet.get('title', '')
        published_at = snippet.get('publishedAt', '')
        
        print(f"\nVideo {i+1}:")
        print(f"  ID: {video_id}")
        print(f"  Title: {title}")
        print(f"  Published: {published_at}")
        print(f"  URL: https://www.youtube.com/watch?v={video_id}")
        
    return youtube_api, videos

def test_video_filter(config_loader, videos):
    """Test the VideoFilter class"""
    print("\nTesting VideoFilter...")
    
    if not videos:
        print("No videos to filter. Skipping VideoFilter test.")
        return
        
    # Create video filter
    scoring_config = config_loader.get_scoring_config()
    video_filter = VideoFilter(config_loader.keywords, scoring_config)
    
    # Filter videos
    filtered_videos = video_filter.filter_videos(videos)
    
    print(f"Filtered {len(filtered_videos)} out of {len(videos)} videos")
    
    # Print details of filtered videos
    for i, video in enumerate(filtered_videos[:3]):
        if i >= len(filtered_videos):
            break
            
        snippet = video.get('snippet', {})
        title = snippet.get('title', '')
        filter_data = video.get('filter_data', {})
        score = filter_data.get('score', 0)
        matched_keywords = filter_data.get('matched_keywords', {})
        
        print(f"\nFiltered Video {i+1}:")
        print(f"  Title: {title}")
        print(f"  Score: {score}")
        
        if matched_keywords.get('top_keywords'):
            print(f"  Top keywords: {', '.join(matched_keywords['top_keywords'])}")
        if matched_keywords.get('other_keywords'):
            print(f"  Other keywords: {', '.join(matched_keywords['other_keywords'])}")
        if matched_keywords.get('negative_keywords'):
            print(f"  Negative keywords: {', '.join(matched_keywords['negative_keywords'])}")

def main():
    """Main test function"""
    print("SimpleBot Component Tests\n")
    
    # Get YouTube API key from environment or config
    api_key = os.environ.get('YOUTUBE_API_KEY')
    
    # If not in environment, try to load from config
    if not api_key:
        try:
            with open('../config/config.yaml', 'r') as f:
                config = yaml.safe_load(f)
                api_key = config.get('youtube', {}).get('api_key')
        except Exception as e:
            print(f"Error loading config: {e}")
    
    # Test components
    config_loader = test_config_loader()
    youtube_api_result = test_youtube_api(api_key)
    
    if youtube_api_result:
        youtube_api, videos = youtube_api_result
        test_video_filter(config_loader, videos)
    
    print("\nTests completed.")

if __name__ == "__main__":
    main()