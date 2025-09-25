import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

class BotLogger:
    """
    Class for handling bot logging
    """
    
    def __init__(self, log_dir: str = "../logs", log_level: str = "INFO"):
        """
        Initialize the logger
        
        Args:
            log_dir: Directory to store log files
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.log_dir = log_dir
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        
        # Create logs directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Set up logger
        self.logger = logging.getLogger("SimpleBot")
        self.logger.setLevel(self.log_level)
        
        # Clear any existing handlers
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Create log file name with date
        log_file = os.path.join(log_dir, f"simplebot_{datetime.now().strftime('%Y%m%d')}.log")
        
        # Create file handler for logging to file
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(self.log_level)
        
        # Create console handler for logging to console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        
        # Create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def get_logger(self) -> logging.Logger:
        """
        Get the logger instance
        
        Returns:
            Logger instance
        """
        return self.logger