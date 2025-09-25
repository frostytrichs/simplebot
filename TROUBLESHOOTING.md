# Troubleshooting Guide for SimpleBot

This guide addresses common issues you might encounter when setting up and running SimpleBot.

## Installation Issues

### ModuleNotFoundError: No module named 'pythorhead'

This error occurs when the pythorhead module wasn't installed correctly.

**Solution:**

1. Make sure your virtual environment is activated:
   ```bash
   source venv/bin/activate
   ```

2. Try installing pythorhead manually:
   ```bash
   pip install pythorhead
   ```

3. If that doesn't work, try specifying a specific version:
   ```bash
   pip install pythorhead==0.34.0
   ```

4. If you're using Python 3.11 or higher, make sure you're using a compatible version of pythorhead.

### Other Module Import Errors

If you encounter other import errors, try reinstalling all dependencies:

```bash
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration Issues

### YouTube API Key Not Working

1. Make sure your API key is correctly set in the `.env` file
2. Verify that your API key has the YouTube Data API v3 enabled
3. Check if you've exceeded your daily quota limit

### Lemmy Authentication Failed

1. Verify your Lemmy credentials in the `.env` file
2. Make sure the instance URL is correct and includes the protocol (https://)
3. Check if your account has permission to post in the specified community

## Runtime Issues

### Bot Not Posting Videos

1. Check the logs for any errors
2. Verify that the scoring threshold isn't too high
3. Make sure the YouTube channels in channels.json are correct
4. Check if the bot is finding videos but they're not passing the keyword filter

### High CPU or Memory Usage

If the bot is using too much CPU or memory:

1. Increase the check interval in config.yaml
2. Reduce the number of channels being monitored
3. Limit the lookback period for videos

## Log Analysis

The bot logs are stored in the `logs` directory. To view the most recent log:

```bash
ls -lt logs/ | head -2  # Find the most recent log file
cat logs/simplebot_YYYYMMDD.log  # Replace with the actual filename
```

Common log messages and their meanings:

- `YouTube API key not configured`: Your API key is missing or invalid
- `Lemmy credentials not configured`: Your Lemmy credentials are missing or invalid
- `Community not found`: The specified community doesn't exist or you don't have access
- `Error creating post`: Failed to post to Lemmy, check your permissions

## Getting Help

If you're still experiencing issues:

1. Check the GitHub repository for open issues or create a new one
2. Include relevant log files and error messages when reporting issues
3. Specify your operating system and Python version