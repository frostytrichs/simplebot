#!/usr/bin/env python3
import os
import sys
import argparse
from dotenv import load_dotenv
from src.simple_bot import SimpleBot

def main():
    """
    Main entry point for the SimpleBot
    """
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='SimpleBot - YouTube to Lemmy Bot')
    parser.add_argument('--config', type=str, default='config',
                        help='Path to configuration directory (default: config)')
    parser.add_argument('--logs', type=str, default='logs',
                        help='Path to logs directory (default: logs)')
    parser.add_argument('--mode', type=str, choices=['single', 'continuous'], default=None,
                        help='Override operation mode (single or continuous)')
    
    args = parser.parse_args()
    
    # Initialize the bot
    bot = SimpleBot(config_dir=args.config, log_dir=args.logs)
    
    # Override mode if specified
    if args.mode:
        if args.mode == 'single':
            bot.run_once()
        else:
            bot.run_continuously()
    else:
        # Use mode from config
        bot.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBot stopped by user")
        sys.exit(0)