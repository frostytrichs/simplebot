### Broad overview of future bot functionality:

#### Requirements:

        - Deployable and managable via headless ssh to linux VPS
        - No sudo permission
        - Uses python3
        - Uses Lemmy API v3 with support for upcoming v4
        - Uses Youtube API with configurable limits on quota usage
        - Coded specifically for use with Lemmy

#### Bot functionality as invisioned:

        - Checks Youtube channels for new live streams and videos at configurable intervals
        - Pulls videos and live streams from a configurable interval (e.g.- from the last hour, etc)
        - Compares the video URls to posts in the Lemmy community within a configurable timeframe to avoid double posting
        - Scans the video title and description for specified keywords
        - Configurable scoring for videos based on the number and type of keywords (e.g.- top keywords might be worth 25 points, other keywords worth 5 points, negative keywords worth -15 points, etc)
        - Posts the videos and live streams that pass a configurable scoring threshold to a Lemmy community
        - Offers single run and continuous modes for testing and production.

#### Useful resources:

        - Official Lemmy Documentation: https://lemmy.readme.io/reference/
        - Lemmy API Information: https://join-lemmy.org/docs/contributors/04-api.html
        - Bot Library for Lemmy: https://github.com/SleeplessOne1917/lemmy-bot
