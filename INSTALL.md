# SimpleBot Installation Guide

This guide will help you install and configure SimpleBot, a YouTube to Lemmy bot.

## Prerequisites

- Python 3.8 or higher
- A YouTube API key
- A Lemmy account

## Installation Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/frostytrichs/simplebot.git
   cd simplebot
   ```

2. **Run the setup script**

   ```bash
   ./setup.sh
   ```

   This will:
   - Create a virtual environment
   - Install dependencies
   - Create a .env file from the template

3. **Configure the bot**

   You have two options for configuration:

   ### Option 1: Using .env file (Recommended for sensitive information)
   
   Edit the `.env` file with your credentials:

   ```
   YOUTUBE_API_KEY=your_youtube_api_key_here
   LEMMY_INSTANCE=https://lemmy.example.com
   LEMMY_USERNAME=your_username_here
   LEMMY_PASSWORD=your_password_here
   LEMMY_COMMUNITY=your_community_name_here
   ```

   ### Option 2: Using config.yaml
   
   Edit `config/config.yaml` for all other settings:
   
   ```yaml
   # YouTube API settings
   youtube:
     # This will be overridden by YOUTUBE_API_KEY in .env if present
     api_key: "YOUR_YOUTUBE_API_KEY"
     quota_limit_per_day: 10000
     check_interval_minutes: 60
     lookback_hours: 24
   
   # Other settings...
   ```

   > **Note:** Environment variables in `.env` take precedence over values in `config.yaml`. 
   > It's recommended to put sensitive information like API keys and passwords in the `.env` file
   > and other configuration in the `config.yaml` file.

4. **Edit the channel and keyword files**

   - `config/channels.json`: YouTube channels to monitor
   - `config/keywords.json`: Keywords for filtering videos

## Getting a YouTube API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the YouTube Data API v3
4. Create credentials (API key)
5. Add the key to your `.env` file

## Running the Bot

### Single Run Mode

To run the bot once:

```bash
./main.py --mode single
```

### Continuous Mode

To run the bot continuously:

```bash
./main.py --mode continuous
```

## Troubleshooting

### Common Issues

1. **pythorhead version error**

   If you encounter an error with the pythorhead package, try updating to the latest version:

   ```bash
   pip install --upgrade pythorhead
   ```

2. **YouTube API quota exceeded**

   The YouTube API has a daily quota limit. If you exceed this limit, you'll need to wait until it resets or adjust the `check_interval_minutes` setting in `config/config.yaml`.

3. **Lemmy authentication issues**

   Make sure your Lemmy credentials are correct and that your account has permission to post in the specified community.

## Deployment

For deployment on a headless Linux server, you can use systemd to keep the bot running:

1. Create a systemd service file:

   ```bash
   sudo cp simplebot.service /etc/systemd/system/
   ```

2. Edit the service file to match your installation path:

   ```bash
   sudo nano /etc/systemd/system/simplebot.service
   ```

3. Enable and start the service:

   ```bash
   sudo systemctl enable simplebot
   sudo systemctl start simplebot
   ```

4. Check the status:

   ```bash
   sudo systemctl status simplebot
   ```

## Logs

Logs are stored in the `logs` directory. You can view them with:

```bash
tail -f logs/simplebot_YYYYMMDD.log
```