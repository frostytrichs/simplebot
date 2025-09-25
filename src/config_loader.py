import os
import json
import yaml
from typing import Dict, List, Any

class ConfigLoader:
    """
    Utility class for loading and managing bot configurations
    """
    
    def __init__(self, config_dir: str = "../config"):
        """
        Initialize the config loader
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = config_dir
        self.config = {}
        self.channels = []
        self.keywords = {}
        
    def load_all_configs(self) -> None:
        """
        Load all configuration files
        """
        self.load_main_config()
        self.load_channels()
        self.load_keywords()
        
    def load_main_config(self) -> Dict[str, Any]:
        """
        Load the main configuration file and override with environment variables
        
        Returns:
            Dict containing configuration settings
        """
        config_path = os.path.join(self.config_dir, "config.yaml")
        try:
            with open(config_path, 'r') as file:
                self.config = yaml.safe_load(file)
                
            # Override with environment variables if they exist
            # YouTube settings
            if os.environ.get('YOUTUBE_API_KEY'):
                if 'youtube' not in self.config:
                    self.config['youtube'] = {}
                self.config['youtube']['api_key'] = os.environ.get('YOUTUBE_API_KEY')
                
            # Lemmy settings
            if 'lemmy' not in self.config:
                self.config['lemmy'] = {}
                
            if os.environ.get('LEMMY_INSTANCE'):
                self.config['lemmy']['instance_url'] = os.environ.get('LEMMY_INSTANCE')
                
            if os.environ.get('LEMMY_USERNAME'):
                self.config['lemmy']['username'] = os.environ.get('LEMMY_USERNAME')
                
            if os.environ.get('LEMMY_PASSWORD'):
                self.config['lemmy']['password'] = os.environ.get('LEMMY_PASSWORD')
                
            if os.environ.get('LEMMY_COMMUNITY'):
                self.config['lemmy']['community'] = os.environ.get('LEMMY_COMMUNITY')
                
            return self.config
        except Exception as e:
            print(f"Error loading main configuration: {e}")
            
            # Create minimal config from environment variables if config file failed to load
            self.config = {
                'youtube': {
                    'api_key': os.environ.get('YOUTUBE_API_KEY', ''),
                    'quota_limit_per_day': 10000,
                    'check_interval_minutes': 60,
                    'lookback_hours': 24
                },
                'lemmy': {
                    'instance_url': os.environ.get('LEMMY_INSTANCE', ''),
                    'username': os.environ.get('LEMMY_USERNAME', ''),
                    'password': os.environ.get('LEMMY_PASSWORD', ''),
                    'community': os.environ.get('LEMMY_COMMUNITY', ''),
                    'check_duplicate_days': 7
                },
                'scoring': {
                    'threshold': 25,
                    'top_keyword_points': 25,
                    'other_keyword_points': 5,
                    'negative_keyword_points': -15,
                    'auto_reject': True
                },
                'operation': {
                    'mode': 'single_run',
                    'log_level': 'INFO'
                }
            }
            return self.config
            
    def load_channels(self) -> List[Dict[str, Any]]:
        """
        Load the channels configuration
        
        Returns:
            List of channel configurations
        """
        channels_path = os.path.join(self.config_dir, "channels.json")
        try:
            with open(channels_path, 'r') as file:
                self.channels = json.load(file)
            return self.channels
        except Exception as e:
            print(f"Error loading channels configuration: {e}")
            return []
            
    def load_keywords(self) -> Dict[str, List[str]]:
        """
        Load the keywords configuration
        
        Returns:
            Dict containing keyword lists
        """
        keywords_path = os.path.join(self.config_dir, "keywords.json")
        try:
            with open(keywords_path, 'r') as file:
                self.keywords = json.load(file)
            return self.keywords
        except Exception as e:
            print(f"Error loading keywords configuration: {e}")
            return {}
    
    def get_youtube_config(self) -> Dict[str, Any]:
        """Get YouTube-specific configuration"""
        return self.config.get('youtube', {})
        
    def get_lemmy_config(self) -> Dict[str, Any]:
        """Get Lemmy-specific configuration"""
        return self.config.get('lemmy', {})
        
    def get_scoring_config(self) -> Dict[str, Any]:
        """Get scoring-specific configuration"""
        return self.config.get('scoring', {})
        
    def get_operation_config(self) -> Dict[str, Any]:
        """Get operation-specific configuration"""
        return self.config.get('operation', {})