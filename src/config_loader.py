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
        Load the main configuration file
        
        Returns:
            Dict containing configuration settings
        """
        config_path = os.path.join(self.config_dir, "config.yaml")
        try:
            with open(config_path, 'r') as file:
                self.config = yaml.safe_load(file)
            return self.config
        except Exception as e:
            print(f"Error loading main configuration: {e}")
            return {}
            
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