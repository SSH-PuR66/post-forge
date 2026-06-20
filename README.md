# post-forge

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Stripe](https://img.shields.io/badge/Stripe-008FC7?style=for-the-badge&logo=stripe&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Social media post scheduler with multi-platform support and analytics**

Schedule posts intelligently • Track engagement metrics • Batch operations • Export analytics

[Features](#features) • [Quick Start](#quick-start) • [Configuration](#configuration) • [API Reference](#api-reference) • [Examples](#examples)

</div>

---

## Overview

post-forge is a Python-based social media automation tool designed for content creators and marketing teams. Schedule posts across multiple platforms, track performance in real-time, and export detailed analytics—all from a unified CLI or API.

**Use Cases:**
- Automate content calendar management
- Schedule posts during optimal engagement hours
- Track post performance across platforms
- Batch-import campaigns from CSV
- Export analytics for reporting

---

## Features

| Feature | Details |
|---------|---------|
| **Multi-Platform** | Twitter, LinkedIn, Instagram (extensible to TikTok, Pinterest) |
| **Batch Scheduling** | Import posts from CSV, schedule with offsets |
| **Performance Tracking** | Real-time engagement metrics (likes, shares, comments) |
| **Analytics Export** | JSON, CSV, Markdown formats for reporting |
| **Rate Limiting** | Configurable max posts per platform per day |
| **Retry Logic** | Automatic retry with exponential backoff |
| **CLI & API** | Use as command-line tool or import as Python module |
| **Lightweight** | Minimal dependencies, quick startup |
| **SQLite Backend** | No database setup required |

---

## System Architecture

```
┌──────────────────────────────────┐
│  CLI / API Client                │
│  (post_forge.py / Python API)    │
└──────────────┬───────────────────┘
               │
┌──────────────▼───────────────────┐
│  Core Scheduler Service          │
│  - Task queue management         │
│  - Rate limiting logic           │
│  - Retry handler                 │
│  - Time-based scheduling         │
└──────────────┬───────────────────┘
               │
┌──────────────▼───────────────────┐
│  Platform Adapters               │
│  - Twitter/X API v2              │
│  - LinkedIn API                  │
│  - Instagram Graph API           │
└──────────────┬───────────────────┘
               │
┌──────────────▼───────────────────┐
│  SQLite Database                 │
│  - posts table                   │
│  - analytics table               │
│  - accounts table                │
│  - schedule_log table            │
└──────────────────────────────────┘
```

### Directory Structure

```
post-forge/
├── post_forge.py          # Main CLI entry point
├── scheduler.py           # Core scheduling logic
├── platforms/
│   ├── twitter.py         # Twitter/X adapter
│   ├── linkedin.py        # LinkedIn adapter
│   └── instagram.py       # Instagram adapter
├── analytics.py           # Performance tracking
├── database.py            # SQLite operations
├── config.json            # Platform & rate limit config
└── requirements.txt       # Python dependencies
```

---

## Installation

### Prerequisites

- **Python** 3.11+ ([download](https://www.python.org/downloads/))
- **pip** (included with Python)
- **Social Media API Keys** (free for all platforms):
  - Twitter/X: https://developer.twitter.com/en/portal/dashboard
  - LinkedIn: https://www.linkedin.com/developers/apps
  - Instagram: https://developers.facebook.com

### Quick Install

```bash
# Clone the repository
git clone https://github.com/SSH-PuR66/post-forge.git
cd post-forge

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Verify installation:

```bash
python post_forge.py --version
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Twitter/X API v2
TWITTER_API_KEY=xxxxxxxxxxxxx
TWITTER_API_SECRET=xxxxxxxxxxxxx
TWITTER_ACCESS_TOKEN=xxxxxxxxxxxxx
TWITTER_ACCESS_SECRET=xxxxxxxxxxxxx
TWITTER_BEARER_TOKEN=Bearer xxxxxxxxxxxxx

# LinkedIn
LINKEDIN_ACCESS_TOKEN=xxxxxxxxxxxxx
LINKEDIN_ORG_ID=xxxxxxxxxxxxx

# Instagram (via Facebook Graph API)
INSTAGRAM_ACCESS_TOKEN=xxxxxxxxxxxxx
INSTAGRAM_BUSINESS_ACCOUNT_ID=xxxxxxxxxxxxx

# Platform Configuration
TWITTER_MAX_POSTS_PER_DAY=10
LINKEDIN_MAX_POSTS_PER_DAY=3
INSTAGRAM_MAX_POSTS_PER_DAY=5

# Scheduling
TIMEZONE=US/Eastern
AUTO_RETRY=true
RETRY_DELAY_MINUTES=30

# Output
DEFAULT_EXPORT_FORMAT=csv
```

### config.json

Override defaults:

```json
{
  "platforms": {
    "twitter": {
      "enabled": true,
      "max_posts_per_day": 10,
      "rate_limit_per_hour": 450,
      "retry_failed": true
    },
    "linkedin": {
      "enabled": true,
      "max_posts_per_day": 3,
      "rate_limit_per_hour": 300
    },
    "instagram": {
      "enabled": true,
      "max_posts_per_day": 5,
      "rate_limit_per_hour": 200
    }
  },
  "scheduling": {
    "timezone": "US/Eastern",
    "auto_retry": true,
    "retry_delay_minutes": 30,
    "retry_max_attempts": 3
  },
  "analytics": {
    "track_engagement": true,
    "update_interval_minutes": 60,
    "retention_days": 90
  }
}
```

---

## Quick Start

### 1. Schedule a Single Post

```bash
python post_forge.py schedule \
  --platform twitter \
  --text "Check out our new product launch! 🚀 #innovation #tech" \
  --schedule "2026-06-21 10:00" \
  --media product.jpg
```

### 2. Schedule Multiple Posts (Batch)

Create `posts.csv`:

```csv
platform,text,media,hashtags,scheduled_time
twitter,"Q3 sales up 40%!","chart.png","#sales #growth",2026-06-21 09:00
linkedin,"Excited to announce our new partnership","banner.jpg","#partnership #news",2026-06-21 10:00
instagram,"Behind the scenes at the office","office.jpg","#teamlife #startup",2026-06-21 11:00
twitter,"Did you know? 95% of startups fail. We're not one of them.","tip.jpg","#startup #tips",2026-06-21 14:00
```

Schedule all:

```bash
python post_forge.py batch \
  --file posts.csv \
  --schedule-offset 1h \
  --verbose
```

This schedules posts starting from 9:00 AM, with 1-hour intervals between each.

### 3. Check Performance

```bash
# Get analytics for today
python post_forge.py analytics --date-range today

# Get analytics for last 7 days
python post_forge.py analytics --date-range last_7_days

# Filter by platform
python post_forge.py analytics --platform twitter --date-range last_7_days

# Export to CSV
python post_forge.py analytics \
  --date-range last_30_days \
  --export csv \
  --output campaign_report.csv
```

---

## Usage Guide

### Command Reference

#### Schedule Operations

```bash
# Single post
python post_forge.py schedule \
  --platform twitter \
  --text "Your message" \
  --schedule "2026-06-21 14:30" \
  --media image.jpg \
  --hashtags "#topic #news"

# From template
python post_forge.py schedule \
  --template "product_launch.txt" \
  --platform all

# Interactive mode
python post_forge.py schedule --interactive
```

#### Batch Operations

```bash
# Import and schedule
python post_forge.py batch \
  --file posts.csv \
  --schedule-offset 2h \
  --dry-run          # Preview without posting

# Schedule existing drafts
python post_forge.py batch --file posts.csv --force
```

#### Listing & Management

```bash
# List all scheduled posts
python post_forge.py list --status scheduled

# List published posts
python post_forge.py list --status published

# List failed posts
python post_forge.py list --status failed

# Retry failed posts
python post_forge.py retry --status failed

# Cancel scheduled post
python post_forge.py cancel --id post_12345

# Reschedule post
python post_forge.py reschedule --id post_12345 --new-time "2026-06-22 10:00"
```

#### Analytics

```bash
# Daily breakdown
python post_forge.py analytics --date-range today

# Weekly trends
python post_forge.py analytics --date-range last_7_days --granularity daily

# Campaign performance
python post_forge.py analytics \
  --filter "tag:campaign_summer" \
  --export json \
  --output summer_campaign_report.json

# Platform comparison
python post_forge.py analytics --compare-platforms
```

#### Configuration Management

```bash
# Show current configuration
python post_forge.py config --show

# Update rate limit
python post_forge.py config --set twitter.max_posts_per_day=15

# Reset to defaults
python post_forge.py config --reset
```

### Batch CSV Format

Required columns:

```csv
platform,text,scheduled_time
twitter,"Your message",2026-06-21 10:00
```

Optional columns:

```csv
platform,text,media,hashtags,scheduled_time,metadata
twitter,"Message","image.jpg","#tag1 #tag2",2026-06-21 10:00,campaign_id:123
linkedin,"Message","banner.png","#tag1",2026-06-21 11:00,utm_source:email
instagram,"Message","photo.jpg","#tag1 #tag2 #tag3",2026-06-21 12:00,country:US
```

---

## API Reference

### Python Module Usage

```python
from post_forge import Scheduler, Analytics, PostManager

# Initialize scheduler
scheduler = Scheduler(config_file="config.json")

# Schedule a single post
post = scheduler.schedule(
    platform="twitter",
    text="Hello world!",
    scheduled_time="2026-06-21 10:00",
    media_paths=["image.jpg"],
    hashtags=["#hello", "#world"]
)
print(f"Post queued: {post.id}")

# Batch schedule
posts = scheduler.batch_schedule(
    posts_data=[
        {"platform": "twitter", "text": "Post 1", "scheduled_time": "2026-06-21 10:00"},
        {"platform": "linkedin", "text": "Post 2", "scheduled_time": "2026-06-21 11:00"},
    ]
)

# Get analytics
analytics = Analytics()
report = analytics.get_performance(days=7)
print(f"Total engagements: {report['total_engagement']}")
print(f"Average reach: {report['avg_reach']}")

# Manage posts
manager = PostManager()
manager.cancel_post("post_id")
manager.list_posts(status="scheduled")
manager.retry_failed_posts()
```

### Database Schema

```sql
-- Posts table
CREATE TABLE posts (
    id TEXT PRIMARY KEY,
    platform TEXT NOT NULL,
    content TEXT NOT NULL,
    media_urls TEXT,
    hashtags TEXT,
    scheduled_time DATETIME,
    published_time DATETIME,
    status TEXT,  -- scheduled, published, failed, cancelled
    retry_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Analytics table
CREATE TABLE analytics (
    id TEXT PRIMARY KEY,
    post_id TEXT NOT NULL,
    platform TEXT NOT NULL,
    likes INTEGER,
    shares INTEGER,
    comments INTEGER,
    impressions INTEGER,
    reach INTEGER,
    engagement_rate REAL,
    captured_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id)
);

-- Accounts table
CREATE TABLE accounts (
    id TEXT PRIMARY KEY,
    platform TEXT NOT NULL,
    account_handle TEXT NOT NULL,
    access_token TEXT ENCRYPTED,
    token_expires_at DATETIME,
    connected_at DATETIME,
    UNIQUE(platform, account_handle)
);

-- Schedule log
CREATE TABLE schedule_log (
    id TEXT PRIMARY KEY,
    post_id TEXT NOT NULL,
    event TEXT,  -- scheduled, published, failed, retried
    status_code INTEGER,
    error_message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id)
);
```

---

## Examples

### Example 1: Daily Post Automation

```bash
# Create posts.csv with your daily content
cat > daily_posts.csv << EOF
platform,text,hashtags,scheduled_time
twitter,"Good morning! What are you working on today?","#motivation #startup",2026-06-21 07:00
linkedin,"6 lessons I learned building a SaaS in 30 days","#startup #learning",2026-06-21 09:00
twitter,"The best time to start was yesterday. The second best time is now.","#startup #inspiration",2026-06-21 12:00
twitter,"Just shipped a major feature. Feeling productive!","#development #shipping",2026-06-21 18:00
EOF

# Schedule all
python post_forge.py batch --file daily_posts.csv

# Check results
python post_forge.py list --status published
```

### Example 2: Campaign Tracking

```bash
# Create campaign posts with metadata
cat > campaign.csv << EOF
platform,text,media,hashtags,scheduled_time,metadata
twitter,"Summer sale starts TODAY! 🌞 20% off everything","banner.jpg","#sale #summer",2026-06-21 08:00,campaign_id:summer_2026
linkedin,"Announcing our Summer Flash Sale - Learn more on our blog","graphic.png","#sale",2026-06-21 09:00,campaign_id:summer_2026
instagram,"Hot deals this season! Swipe to shop","summer.jpg","#sale #summer #deals",2026-06-21 10:00,campaign_id:summer_2026
twitter,"Only 2 days left! Grab 20% off while supplies last 🔥","banner.jpg","#sale #urgency",2026-06-22 09:00,campaign_id:summer_2026
EOF

# Schedule campaign
python post_forge.py batch --file campaign.csv

# Track performance
python post_forge.py analytics \
  --filter "metadata:campaign_id:summer_2026" \
  --date-range "2026-06-21 to 2026-06-23" \
  --export csv \
  --output summer_campaign_metrics.csv
```

### Example 3: Multi-Platform Distribution

```bash
# Write post once, publish everywhere
python post_forge.py schedule \
  --platform all \
  --text "Just launched: New analytics dashboard. 10x faster, 100% free. Check it out!" \
  --media dashboard.jpg \
  --hashtags "#launch #analytics #startup" \
  --schedule "2026-06-21 14:00"
```

### Example 4: Performance Analysis

```bash
# Compare platforms
python post_forge.py analytics --compare-platforms

# Output:
# Platform | Posts | Avg Likes | Avg Shares | Avg Comments | Engagement %
# ---------|-------|-----------|-----------|--------------|-------------
# Twitter  | 45    | 12.3      | 2.1       | 1.8          | 0.85%
# LinkedIn | 23    | 45.2      | 8.9       | 3.2          | 2.15%
# Instagram| 18    | 156.7     | 12.1      | 8.3          | 4.32%

# Find best-performing content
python post_forge.py analytics \
  --sort-by engagement_rate \
  --limit 10 \
  --export markdown \
  --output top_posts.md
```

---

## Troubleshooting

### "Authentication failed"

```bash
# Verify credentials in .env
echo $TWITTER_BEARER_TOKEN

# Test API connection
python post_forge.py test --platform twitter

# Regenerate tokens from platform dashboards
# Twitter: https://developer.twitter.com/en/portal/dashboard
# LinkedIn: https://www.linkedin.com/developers/apps
```

### "Rate limited"

```bash
# Check current rate limits
python post_forge.py config --show | grep rate_limit

# Adjust configuration
python post_forge.py config --set twitter.rate_limit_per_hour=300

# Schedule posts further apart
python post_forge.py batch --file posts.csv --schedule-offset 2h
```

### "Post didn't publish"

```bash
# Check logs
tail -f logs/post_forge.log

# List failed posts
python post_forge.py list --status failed

# View error details
python post_forge.py list --status failed --verbose

# Retry with debug output
python post_forge.py retry --debug
```

### "Database locked"

```bash
# Close all instances of post_forge
pkill -f post_forge

# Clear locks
rm -f posts.db-wal posts.db-shm

# Restart
python post_forge.py list
```

---

## Advanced Configuration

### Custom Platform Adapter

```python
# platforms/custom.py
from platforms.base import PlatformAdapter

class CustomPlatform(PlatformAdapter):
    def publish_post(self, post_data):
        # Your custom implementation
        pass
    
    def get_engagement_metrics(self, post_id):
        # Track engagement
        pass
```

### Scheduled Background Execution

```bash
# macOS/Linux: Add to crontab
crontab -e

# Run every hour to check scheduled posts
0 * * * * cd /path/to/post-forge && python post_forge.py execute --background

# Retry failed posts every 30 minutes
*/30 * * * * cd /path/to/post-forge && python post_forge.py retry
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "post_forge.py", "execute", "--background"]
```

```bash
docker build -t post-forge .
docker run -d \
  -e TWITTER_BEARER_TOKEN="..." \
  -e LINKEDIN_ACCESS_TOKEN="..." \
  post-forge
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License — see [LICENSE](LICENSE) file

---

## Author

Built by [Sergio Rodriguez](https://github.com/SSH-PuR66)

- **GitHub**: https://github.com/SSH-PuR66
- **Portfolio**: https://sergrdz.pages.dev
- **LinkedIn**: https://www.linkedin.com/in/serg-rodriguez-453551275/

---

## Roadmap

- [x] Twitter/X support
- [x] LinkedIn support
- [x] Instagram support
- [ ] TikTok support
- [ ] Pinterest support
- [ ] Mastodon support
- [ ] AI-powered caption generation
- [ ] Sentiment analysis
- [ ] Competitor tracking
- [ ] Web dashboard
- [ ] Webhooks & integrations

---

**Made for content creators who want to automate, not cut corners.**
