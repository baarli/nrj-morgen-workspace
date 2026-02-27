---
name: podcast-manager
description: Comprehensive podcast management system for episode fetching, clip generation, email notifications, and system verification. Supports "Baarli og Benjamin går i terapi" and "NRJ Morgen Podkast".
triggers:
  - fetch latest podcast episode
  - create podcast clip
  - send podcast email
  - verify podcast system
  - list podcast episodes
  - analyze podcast audio
  - generate podcast report
---

# 🎙️ Podcast Manager

**Complete podcast management system** for automated episode handling, clip generation, and distribution.

## 📋 Overview

This skill provides a complete workflow for managing podcast episodes:

1. **Fetch** - Download episodes from RSS feeds
2. **Analyze** - Find perfect clips using AI-powered analysis
3. **Generate** - Create video clips for social media
4. **Notify** - Send email notifications with clips
5. **Verify** - System health checks and monitoring

## 🎯 Supported Podcasts

| Podcast | RSS Feed | Status |
|---------|----------|--------|
| Baarli og Benjamin går i terapi | `https://rss.podplaystudio.com/4035.xml` | ✅ Active |
| NRJ Morgen Podkast | `https://rss.podplaystudio.com/3873.xml` | ✅ Active |

## 🚀 Quick Start

### Fetch Latest Episodes
```bash
# Fetch all episodes from RSS
python3 /root/.openclaw/workspace/skills/podcast-manager/scripts/podcast-clipper.py fetch-latest

# List recent episodes
python3 /root/.openclaw/workspace/skills/podcast-manager/scripts/podcast-clipper.py list --limit 5
```

### Create Daily Clips
```bash
# Run daily clip generation
bash /root/.openclaw/workspace/skills/podcast-manager/scripts/daily-podcast-clips.sh

# Generate clips with email notification
python3 /root/.openclaw/workspace/skills/podcast-manager/scripts/daily-podcast-email.py --send-email
```

### Find Perfect Clips (AI-Powered)
```bash
# Analyze audio and find best clips
python3 /root/.openclaw/workspace/skills/podcast-manager/scripts/perfect-clip-finder.py /path/to/episode.mp3

# With transcription (requires Whisper)
python3 /root/.openclaw/workspace/skills/podcast-manager/scripts/perfect-clip-finder.py /path/to/episode.mp3 --transcribe
```

### Verify System
```bash
# Run system verification
bash /root/.openclaw/workspace/skills/podcast-manager/scripts/verify-podcast-system.sh
```

## 📁 File Structure

```
skills/podcast-manager/
├── SKILL.md                          # This documentation
├── scripts/
│   ├── podcast-clipper.py           # Episode fetching and basic clipping
│   ├── daily-podcast-clips.sh       # Automated daily workflow
│   ├── perfect-clip-finder.py       # AI-powered clip detection
│   ├── daily-podcast-email.py       # Email notifications
│   └── verify-podcast-system.sh     # System verification
└── config/
    └── podcasts.json                # Podcast configuration
```

## 🔧 Scripts Reference

### 1. podcast-clipper.py
**Purpose:** Fetch episodes and create basic clips

**Commands:**
```bash
# Fetch latest episodes from RSS
python3 podcast-clipper.py fetch-latest

# List episodes
python3 podcast-clipper.py list --limit 10

# Download specific episode
python3 podcast-clipper.py download --episode-index 0 --output-dir ./downloads

# Create manual clip
python3 podcast-clipper.py create-clip \
  --file episode.mp3 \
  --start 120 \
  --end 150 \
  --output clip.mp3

# Analyze audio file
python3 podcast-clipper.py analyze --file episode.mp3
```

### 2. daily-podcast-clips.sh
**Purpose:** Automated daily workflow for clip generation

**What it does:**
1. Checks for new episodes
2. Downloads latest episode
3. Creates 3 clips (30 seconds each)
4. Saves to `/tmp/podcast-clips/YYYYMMDD/`
5. Logs all activity

**Usage:**
```bash
# Manual run
bash daily-podcast-clips.sh

# Check output
ls -la /tmp/podcast-clips/$(date +%Y%m%d)/
```

**Output Structure:**
```
/tmp/podcast-clips/20260228/
├── Episode_Title.mp3          # Full episode
├── clip_0_laughter.mp3        # Clip 1
├── clip_1_conversation.mp3    # Clip 2
├── clip_2_reaction.mp3        # Clip 3
└── daily-clips.log            # Activity log
```

### 3. perfect-clip-finder.py
**Purpose:** AI-powered analysis to find the best clips

**Scoring Parameters:**
| Parameter | Weight | Description |
|-----------|--------|-------------|
| Audio Energy | 15% | Volume and dynamics |
| Laughter Detection | 20% | Identifies funny moments |
| Conversation Pace | 15% | Speech rhythm analysis |
| Emotional Intensity | 20% | Excitement level |
| Quote Quality | 15% | Relatable content |
| Viral Potential | 15% | Shareability score |

**Usage:**
```bash
# Basic analysis
python3 perfect-clip-finder.py episode.mp3

# Find 5 clips
python3 perfect-clip-finder.py episode.mp3 --clips 5

# Custom duration
python3 perfect-clip-finder.py episode.mp3 --min-duration 20 --max-duration 40

# With transcription (better quality)
python3 perfect-clip-finder.py episode.mp3 --transcribe --output clips.json
```

**Requirements:**
- `pydub` - Audio analysis
- `numpy` - Signal processing
- `whisper` - Transcription (optional)

### 4. daily-podcast-email.py
**Purpose:** Generate clips and send email notifications

**Features:**
- Processes multiple podcasts
- Generates video clips (1080x1920)
- Sends email with attachments
- Tracks processed episodes

**Usage:**
```bash
# Generate clips only
python3 daily-podcast-email.py

# Generate and send email
python3 daily-podcast-email.py --send-email

# Custom recipient
python3 daily-podcast-email.py --send-email --email user@example.com
```

**Email Content:**
- Episode titles and summaries
- List of generated clips
- Video attachments (MP4 format)
- Timestamps for each clip

### 5. verify-podcast-system.sh
**Purpose:** System health verification

**Checks:**
- ✅ Required files exist
- ✅ Dependencies installed (ffmpeg, python3)
- ✅ Today's production status
- ✅ MP3 file validity
- ✅ Cron job status
- ✅ RSS feed accessibility

**Usage:**
```bash
# Run verification
bash verify-podcast-system.sh

# Exit codes:
# 0 = All checks passed
# >0 = Number of errors found
```

## ⚙️ Configuration

### Podcast Configuration
Edit `config/podcasts.json` to add or modify podcasts:

```json
{
  "podcasts": {
    "baarli": {
      "name": "Baarli og Benjamin går i terapi",
      "rss": "https://rss.podplaystudio.com/4035.xml",
      "emoji": "🎙️",
      "enabled": true
    },
    "nrj": {
      "name": "NRJ Morgen Podkast",
      "rss": "https://rss.podplaystudio.com/3873.xml",
      "emoji": "📻",
      "enabled": true
    }
  },
  "settings": {
    "clips_per_episode": 3,
    "clip_duration": 30,
    "output_format": "mp4",
    "video_resolution": "1080x1920"
  }
}
```

### Email Configuration
Set up email credentials in `.credentials/nrj-morgen.env`:

```bash
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
```

### Cron Job Setup
Add to crontab for daily automation:

```bash
# Daily at 07:00
0 7 * * * cd /root/.openclaw/workspace/skills/podcast-manager && bash scripts/daily-podcast-clips.sh

# Daily at 08:00 with email
0 8 * * * cd /root/.openclaw/workspace/skills/podcast-manager && python3 scripts/daily-podcast-email.py --send-email
```

## 📊 Workflow Diagram

```
┌─────────────────┐
│  RSS Feed Check │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Download Episode│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Analyze Audio   │◄──── perfect-clip-finder.py
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Generate Clips  │◄──── ffmpeg
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Create Videos   │◄──── 1080x1920 format
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Send Email      │◄──── daily-podcast-email.py
└─────────────────┘
```

## 🔍 Troubleshooting

### Common Issues

**1. ffmpeg not found**
```bash
# Install ffmpeg
sudo apt-get update
sudo apt-get install ffmpeg

# Verify
ffmpeg -version
```

**2. pydub not installed**
```bash
pip3 install pydub numpy
```

**3. Whisper not available**
```bash
pip3 install openai-whisper
```

**4. RSS feed unreachable**
```bash
# Test connectivity
curl -I https://rss.podplaystudio.com/4035.xml

# Check DNS
nslookup rss.podplaystudio.com
```

**5. Email sending fails**
- Verify credentials in `.credentials/nrj-morgen.env`
- Check Gmail app password (not regular password)
- Ensure less secure apps is enabled or use app password

### Log Files

Check logs for debugging:
```bash
# Daily clips log
tail -f /tmp/podcast-clips/$(date +%Y%m%d)/daily-clips.log

# Processed episodes cache
cat /tmp/podcast-daily/processed.json

# Episode cache
cat /tmp/podcast-clips/episodes.json
```

## 📈 Performance Metrics

Typical processing times:
- Episode download: 10-30 seconds (28MB MP3)
- Basic clip generation: 5-10 seconds per clip
- AI analysis (with pydub): 30-60 seconds
- Transcription (with Whisper): 2-5 minutes
- Video conversion: 10-20 seconds per clip

## 🛡️ Best Practices

1. **Run verification daily** - Use `verify-podcast-system.sh` to catch issues early
2. **Monitor disk space** - Clips are stored in `/tmp/` and may accumulate
3. **Check email delivery** - Verify spam folders if emails not received
4. **Review clip quality** - AI analysis helps but manual review is recommended
5. **Update dependencies** - Keep ffmpeg and Python packages current

## 🔗 Integration with Other Skills

- **content-aggregator** - Can trigger podcast clips from morning routine
- **email-automation** - Shares email infrastructure
- **monitoring-system** - Can monitor podcast system health
- **mission-control** - Dashboard can display podcast status

## 📝 Version History

- **1.0.0** (2026-02-28) - Initial skill creation
  - Consolidated all podcast scripts
  - Added comprehensive documentation
  - Created verification system

## 📚 References

- [ffmpeg Documentation](https://ffmpeg.org/documentation.html)
- [pydub Documentation](https://github.com/jiaaro/pydub)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [RSS Specification](https://www.rssboard.org/rss-specification)

---

**Maintainer:** BaarliClaw  
**Last Updated:** 2026-02-28  
**Status:** Production Ready ✅
