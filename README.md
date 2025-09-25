# SimpleBot - YouTube to Lemmy Bot

A Python bot that filters and posts YouTube videos to a Lemmy community based on configurable criteria.

## Features

- Monitors YouTube channels for new videos and livestreams
- Filters videos based on keywords in titles and descriptions
- Scores videos using a configurable point system
- Posts videos that meet a threshold score to a Lemmy community
- Avoids duplicate posts
- Supports both single-run and continuous operation modes

## Requirements

- Python 3.6+
- YouTube Data API key
- Lemmy account credentials

## Installation

1. Clone this repository:
   ```
   git clone -b https://github.com/frostytrichs/simplebot/tree/feature/initial-implementation.git
   cd simplebot
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Copy the example environment file and edit it with your credentials:
   ```
   cp .env.example .env
   ```
   
   Edit the `.env` file with your YouTube API key and Lemmy credentials.

4. Configure the bot:
   - Edit `config/config.yaml` with your desired settings
   - Edit `config/channels.json` to add YouTube channels to monitor
   - Edit `config/keywords.json` to configure keyword filtering

## Configuration

### Main Configuration (config.yaml)

The main configuration file contains settings for the YouTube API, Lemmy API, scoring system, and bot operation:

```yaml
# YouTube API settings
youtube:
  api_key: "YOUR_YOUTUBE_API_KEY"  # Can also be set via environment variable
  quota_limit_per_day: 10000  # Default YouTube API quota limit
  check_interval_minutes: 60  # How often to check for new videos
  lookback_hours: 24  # How far back to look for videos

# Lemmy settings
lemmy:
  instance_url: "https://lemmy.example.com"  # Your Lemmy instance URL
  username: "YOUR_USERNAME"
  password: "YOUR_PASSWORD"
  community: "YOUR_COMMUNITY"  # Community name to post to
  check_duplicate_days: 7  # How many days back to check for duplicates

# Scoring settings
scoring:
  threshold: 25  # Minimum score required to post a video
  top_keyword_points: 25  # Points for each top keyword match
  other_keyword_points: 5  # Points for each other keyword match
  negative_keyword_points: -15  # Points for each negative keyword match
  auto_reject: true  # Whether to auto-reject videos with auto_reject keywords

# Bot operation
operation:
  mode: "continuous"  # "continuous" or "single_run"
  log_level: "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Channels Configuration (channels.json)

Define the YouTube channels to monitor:

```json
[
  {
    "name": "Channel Name",
    "channelID": "YOUTUBE_CHANNEL_ID",
    "primary_series_tag": "TAG",
    "secondary_series_tags": ["TAG1", "TAG2"]
  }
]
```

### Keywords Configuration (keywords.json)

Define keywords for filtering videos:

```json
{
  "auto_reject": [
    "keyword1",
    "keyword2"
  ],
  "negative_keywords": [
    "keyword1",
    "keyword2"
  ],
  "top_keywords": [
    "keyword1",
    "keyword2"
  ],
  "other_keywords": [
    "keyword1",
    "keyword2"
  ]
}
```

## Usage

### Single Run Mode

To run the bot once:

```
python main.py --mode single
```

### Continuous Mode

To run the bot continuously:

```
python main.py --mode continuous
```

### Using Custom Configuration Paths

```
python main.py --config /path/to/config --logs /path/to/logs
```

## Deployment

For deployment on a headless Linux server:

1. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Use a process manager like systemd or supervisor to keep the bot running.

Example systemd service file (`/etc/systemd/system/simplebot.service`):

```
[Unit]
Description=SimpleBot YouTube to Lemmy Bot
After=network.target

[Service]
User=yourusername
WorkingDirectory=/path/to/simplebot
ExecStart=/path/to/simplebot/venv/bin/python main.py --mode continuous
Restart=on-failure
RestartSec=5s
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```
sudo systemctl enable simplebot
sudo systemctl start simplebot
```

## Logging

Logs are stored in the `logs` directory by default. The log level can be configured in `config.yaml`.

## License

[MIT License](LICENSE)
