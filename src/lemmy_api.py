import datetime
from typing import List, Dict, Any, Optional
from pythorhead import Lemmy

class LemmyAPI:
    """
    Class for interacting with the Lemmy API
    """
    
    def __init__(self, instance_url: str, username: str, password: str):
        """
        Initialize the Lemmy API client
        
        Args:
            instance_url: URL of the Lemmy instance
            username: Lemmy username
            password: Lemmy password
        """
        self.instance_url = instance_url
        self.username = username
        self.password = password
        self.lemmy = Lemmy(instance_url)
        self.community_id = None
        self.login()
        
    def login(self) -> bool:
        """
        Log in to the Lemmy instance
        
        Returns:
            True if login successful, False otherwise
        """
        try:
            self.lemmy.log_in(self.username, self.password)
            return True
        except Exception as e:
            print(f"Failed to log in to Lemmy: {e}")
            return False
            
    def get_community_id(self, community_name: str) -> Optional[int]:
        """
        Get the ID of a community by name
        
        Args:
            community_name: Name of the community
            
        Returns:
            Community ID or None if not found
        """
        try:
            response = self.lemmy.discover_community(community_name)
            communities = response.get('communities', [])
            
            for community in communities:
                if community['community']['name'].lower() == community_name.lower():
                    self.community_id = community['community']['id']
                    return self.community_id
                    
            print(f"Community '{community_name}' not found")
            return None
            
        except Exception as e:
            print(f"Error getting community ID: {e}")
            return None
            
    def create_post(self, community_id: int, title: str, url: str, body: str = "") -> Optional[Dict[str, Any]]:
        """
        Create a new post in a community
        
        Args:
            community_id: ID of the community
            title: Post title
            url: URL to link to
            body: Post body text (optional)
            
        Returns:
            Post information dictionary or None if creation failed
        """
        try:
            response = self.lemmy.post.create(
                community_id=community_id,
                name=title,
                url=url,
                body=body
            )
            
            return response.get('post_view')
            
        except Exception as e:
            print(f"Error creating post: {e}")
            return None
            
    def get_recent_posts(self, community_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent posts from a community
        
        Args:
            community_id: ID of the community
            limit: Maximum number of posts to retrieve
            
        Returns:
            List of post information dictionaries
        """
        try:
            response = self.lemmy.post.list(
                community_id=community_id,
                limit=limit,
                sort="New"
            )
            
            return response.get('posts', [])
            
        except Exception as e:
            print(f"Error getting recent posts: {e}")
            return []
            
    def is_url_already_posted(self, community_id: int, url: str, days: int = 7) -> bool:
        """
        Check if a URL has already been posted to a community within a time period
        
        Args:
            community_id: ID of the community
            url: URL to check
            days: Number of days back to check
            
        Returns:
            True if the URL has already been posted, False otherwise
        """
        try:
            # Get recent posts
            posts = self.get_recent_posts(community_id, limit=100)
            
            # Calculate the cutoff date
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
            
            # Check if any post has the same URL and is newer than the cutoff date
            for post in posts:
                post_url = post.get('post', {}).get('url')
                if post_url and post_url == url:
                    published_time = datetime.datetime.fromisoformat(
                        post.get('post', {}).get('published').replace('Z', '+00:00')
                    )
                    if published_time >= cutoff_date:
                        return True
                        
            return False
            
        except Exception as e:
            print(f"Error checking if URL already posted: {e}")
            return False