from typing import Dict, List, Any, Tuple

class VideoFilter:
    """
    Class for filtering and scoring YouTube videos based on keywords
    """
    
    def __init__(self, keywords: Dict[str, List[str]], scoring_config: Dict[str, Any]):
        """
        Initialize the video filter
        
        Args:
            keywords: Dictionary containing keyword lists
            scoring_config: Dictionary containing scoring configuration
        """
        self.auto_reject_keywords = keywords.get('auto_reject', [])
        self.negative_keywords = keywords.get('negative_keywords', [])
        self.top_keywords = keywords.get('top_keywords', [])
        self.other_keywords = keywords.get('other_keywords', [])
        
        self.top_keyword_points = scoring_config.get('top_keyword_points', 25)
        self.other_keyword_points = scoring_config.get('other_keyword_points', 5)
        self.negative_keyword_points = scoring_config.get('negative_keyword_points', -15)
        self.threshold = scoring_config.get('threshold', 25)
        self.auto_reject = scoring_config.get('auto_reject', True)
        
    def should_auto_reject(self, title: str, description: str) -> bool:
        """
        Check if a video should be automatically rejected based on auto-reject keywords
        
        Args:
            title: Video title
            description: Video description
            
        Returns:
            True if the video should be rejected, False otherwise
        """
        if not self.auto_reject:
            return False
            
        title_lower = title.lower()
        description_lower = description.lower()
        
        for keyword in self.auto_reject_keywords:
            if keyword.lower() in title_lower or keyword.lower() in description_lower:
                return True
                
        return False
        
    def score_video(self, title: str, description: str) -> Tuple[int, Dict[str, List[str]]]:
        """
        Score a video based on keywords in title and description
        
        Args:
            title: Video title
            description: Video description
            
        Returns:
            Tuple containing (score, matched_keywords_dict)
        """
        score = 0
        matched_keywords = {
            'top_keywords': [],
            'other_keywords': [],
            'negative_keywords': []
        }
        
        title_lower = title.lower()
        description_lower = description.lower()
        
        # Check for auto-reject keywords first
        if self.should_auto_reject(title, description):
            return -1000, matched_keywords
        
        # Check for top keywords
        for keyword in self.top_keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in title_lower or keyword_lower in description_lower:
                score += self.top_keyword_points
                matched_keywords['top_keywords'].append(keyword)
        
        # Check for other keywords
        for keyword in self.other_keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in title_lower or keyword_lower in description_lower:
                score += self.other_keyword_points
                matched_keywords['other_keywords'].append(keyword)
        
        # Check for negative keywords
        for keyword in self.negative_keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in title_lower or keyword_lower in description_lower:
                score += self.negative_keyword_points
                matched_keywords['negative_keywords'].append(keyword)
        
        return score, matched_keywords
        
    def passes_threshold(self, score: int) -> bool:
        """
        Check if a score passes the threshold
        
        Args:
            score: Video score
            
        Returns:
            True if the score passes the threshold, False otherwise
        """
        return score >= self.threshold
        
    def filter_videos(self, videos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter a list of videos based on keywords and scoring
        
        Args:
            videos: List of video information dictionaries
            
        Returns:
            List of filtered video dictionaries with added score information
        """
        filtered_videos = []
        
        for video in videos:
            snippet = video.get('snippet', {})
            title = snippet.get('title', '')
            description = snippet.get('description', '')
            
            # Skip videos with empty titles
            if not title:
                continue
                
            # Score the video
            score, matched_keywords = self.score_video(title, description)
            
            # Check if the video passes the threshold
            if self.passes_threshold(score):
                # Add score and matched keywords to the video info
                video['filter_data'] = {
                    'score': score,
                    'matched_keywords': matched_keywords
                }
                filtered_videos.append(video)
                
        return filtered_videos