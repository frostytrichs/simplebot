import os
import datetime
from typing import List, Dict, Any, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class YouTubeAPI:
    """
    Class for interacting with the YouTube API
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the YouTube API client
        
        Args:
            api_key: YouTube API key
        """
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        
    def get_channel_videos(self, channel_id: str, published_after: datetime.datetime) -> List[Dict[str, Any]]:
        """
        Get videos from a channel published after a specific time
        
        Args:
            channel_id: YouTube channel ID
            published_after: Datetime object representing the earliest publication time to include
            
        Returns:
            List of video information dictionaries
        """
        try:
            # Convert datetime to RFC 3339 format
            published_after_str = published_after.isoformat() + 'Z'
            
            # First, get the channel's uploads playlist ID
            channels_response = self.youtube.channels().list(
                part="contentDetails",
                id=channel_id
            ).execute()
            
            if not channels_response.get('items'):
                print(f"No channel found with ID: {channel_id}")
                return []
                
            uploads_playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Now get videos from the uploads playlist
            videos = []
            next_page_token = None
            
            while True:
                playlist_items_response = self.youtube.playlistItems().list(
                    part="snippet,contentDetails",
                    playlistId=uploads_playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                ).execute()
                
                for item in playlist_items_response['items']:
                    video_published_at = datetime.datetime.fromisoformat(
                        item['contentDetails']['videoPublishedAt'].replace('Z', '+00:00')
                    )
                    
                    if video_published_at >= published_after:
                        video_id = item['contentDetails']['videoId']
                        
                        # Get more detailed video information
                        video_response = self.youtube.videos().list(
                            part="snippet,contentDetails,statistics,liveStreamingDetails",
                            id=video_id
                        ).execute()
                        
                        if video_response['items']:
                            videos.append(video_response['items'][0])
                
                next_page_token = playlist_items_response.get('nextPageToken')
                if not next_page_token:
                    break
                    
            return videos
            
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
            
    def get_video_details(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific video
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Dictionary containing video details or None if not found
        """
        try:
            video_response = self.youtube.videos().list(
                part="snippet,contentDetails,statistics,liveStreamingDetails",
                id=video_id
            ).execute()
            
            if video_response['items']:
                return video_response['items'][0]
            else:
                return None
                
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
            
    def is_live_stream(self, video_details: Dict[str, Any]) -> bool:
        """
        Check if a video is a live stream
        
        Args:
            video_details: Video details dictionary
            
        Returns:
            True if the video is a live stream, False otherwise
        """
        return 'liveStreamingDetails' in video_details and \
               video_details.get('snippet', {}).get('liveBroadcastContent') in ['live', 'upcoming']