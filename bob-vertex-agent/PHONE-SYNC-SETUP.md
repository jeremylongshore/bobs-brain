# Phone Sync to Bob's Knowledge Base

**Created:** 2025-11-09
**Purpose:** Sync phone data to Bob so he knows EVERYTHING

---

## Overview

Your phone becomes another data source for Bob:
- Photos → Auto-captioned and indexed
- Notes → Searchable by Bob
- Voice memos → Transcribed and indexed
- Documents → Added to knowledge base
- App data → Synced to computer

---

## Option 1: Google Drive Auto-Sync (EASIEST)

**Setup:**
1. Enable Google Photos backup on phone
2. Enable Google Drive backup for:
   - Documents
   - Notes (Google Keep)
   - Voice memos

3. Mount Google Drive on computer with rclone:
```bash
# Configure (one-time)
rclone config

# Mount
mkdir -p /home/jeremy/gdrive
rclone mount gdrive: /home/jeremy/gdrive --daemon

# Auto-mount on boot
echo "@reboot /usr/bin/rclone mount gdrive: /home/jeremy/gdrive --daemon" | crontab -
```

4. Add to daily Bob sync:
```bash
# In daily-sync.sh
rsync -av /home/jeremy/gdrive/ gs://bobs-brain-life-work-backup/phone/
```

**Bob will see:**
- ✅ All Google Photos (with auto-captions)
- ✅ All Google Drive files
- ✅ Google Keep notes
- ✅ Google Docs/Sheets/Slides
- ✅ WhatsApp backups (if enabled)

---

## Option 2: Syncthing (BEST for Real-Time Sync)

**What it is:**
- Peer-to-peer sync (no cloud middleman)
- Real-time sync (changes appear instantly)
- Works over WiFi or Internet
- Free and open source

**Setup:**

**On Computer:**
```bash
# Install Syncthing
sudo apt-get install syncthing

# Start Syncthing
syncthing

# Open web UI: http://localhost:8384
```

**On Phone:**
1. Install Syncthing app from Play Store/App Store
2. Open app → Add folder
3. Select folders to sync:
   - Camera (photos)
   - DCIM (screenshots)
   - Documents
   - Voice Recorder
   - Notes

4. Add computer as device (scan QR code from web UI)
5. Accept on computer

**What syncs:**
- ✅ Photos in real-time
- ✅ Screenshots
- ✅ Voice memos
- ✅ Documents
- ✅ Any folder you choose

**Bob integration:**
```bash
# Syncthing syncs to: /home/jeremy/Sync/
# Add to daily Bob ingestion:
/home/jeremy/Sync/ → Vertex AI Search
```

---

## Option 3: Nextcloud (Most Features)

**What it is:**
- Self-hosted or managed Nextcloud
- Like your own Google Drive
- Notes, files, calendar, contacts

**Setup:**
1. Sign up for Nextcloud provider OR self-host
2. Install Nextcloud app on phone
3. Configure auto-upload for:
   - Photos
   - Documents
   - Notes

4. Mount on computer:
```bash
rclone config  # Add Nextcloud remote
rclone mount nextcloud: /home/jeremy/nextcloud --daemon
```

---

## Option 4: Multi-Sync (RECOMMENDED)

**Use ALL methods for different data:**

**Phone → Google Drive:**
- Photos (Google Photos)
- Documents
- Email backups

**Phone → Syncthing:**
- Screenshots (real-time)
- Voice memos (real-time)
- Work notes (real-time)

**Phone → rclone → Bob:**
- Everything syncs to computer
- Daily ingestion to Bob
- Bob knows phone content

---

## Data Flow with Phone

```
┌──────────────────────────────────────────┐
│           YOUR PHONE                     │
├──────────────────────────────────────────┤
│  • Photos (Google Photos backup)         │
│  • Documents (Google Drive)              │
│  • Notes (Google Keep)                   │
│  • Voice Memos (Drive/Syncthing)         │
│  • Screenshots (Syncthing real-time)     │
│  • App data (selective)                  │
└──────────────┬───────────────────────────┘
               │
               │ Auto-sync (24/7)
               ▼
┌──────────────────────────────────────────┐
│      COMPUTER (/home/jeremy)             │
├──────────────────────────────────────────┤
│  /home/jeremy/gdrive/     (Google Drive) │
│  /home/jeremy/Sync/       (Syncthing)    │
│  /home/jeremy/nextcloud/  (Nextcloud)    │
└──────────────┬───────────────────────────┘
               │
               │ Daily ingestion (2 AM)
               ▼
┌──────────────────────────────────────────┐
│         BOB'S KNOWLEDGE BASE             │
│         (Vertex AI Search)               │
├──────────────────────────────────────────┤
│  • Computer files (67GB)                 │
│  • Phone photos (captioned)              │
│  • Phone notes (indexed)                 │
│  • Voice memos (transcribed)             │
│  • Google Drive                          │
└──────────────────────────────────────────┘
```

---

## Bob's Phone Capabilities

**After phone sync, Bob can:**

1. **Find photos:** "Show me photos from my trip to Austin last month"
2. **Search notes:** "What did I write about the new project idea?"
3. **Transcribe voice:** "What was in that voice memo from Tuesday?"
4. **Find documents:** "Where's that PDF I saved on my phone?"
5. **Track context:** "What was I working on when I took that screenshot?"

---

## Smart Filtering for Phone Data

**INCLUDE:**
- ✅ Notes and documents
- ✅ Screenshots with text
- ✅ Voice memos (transcribed)
- ✅ Work-related photos
- ✅ PDFs and documents

**EXCLUDE:**
- ❌ Personal photos (family, friends) - unless you want Bob to see
- ❌ Sensitive documents
- ❌ Banking apps data
- ❌ Private messages

**Configuration:**
```bash
# In phone-filter-rules.txt
INCLUDE: /Sync/Documents/**
INCLUDE: /Sync/Screenshots/**
INCLUDE: /Sync/VoiceMemos/**
INCLUDE: /gdrive/Documents/**
INCLUDE: /gdrive/Keep/**

EXCLUDE: /Sync/DCIM/Camera/202*/  # Personal photos
EXCLUDE: /gdrive/Banking/**        # Sensitive
EXCLUDE: **/password*              # Passwords
```

---

## Voice Memo Transcription

**Automatic transcription pipeline:**

1. **Phone records voice memo** → Saves to Syncthing folder
2. **Computer detects new file** → Triggers transcription
3. **Whisper API transcribes** → Creates text file
4. **Bob ingests transcript** → Searchable by content
5. **Links preserved** → Bob knows audio + transcript

**Setup:**
```bash
# Install whisper
pip install openai-whisper

# Auto-transcribe script
cat > /home/jeremy/006-scripts/transcribe-voice-memos.sh << 'EOF'
#!/bin/bash
# Transcribe new voice memos

VOICE_DIR="/home/jeremy/Sync/VoiceMemos"
TRANSCRIPT_DIR="/home/jeremy/Sync/Transcripts"

mkdir -p "$TRANSCRIPT_DIR"

# Find new audio files
find "$VOICE_DIR" -name "*.m4a" -o -name "*.wav" | while read audio; do
    transcript="${TRANSCRIPT_DIR}/$(basename "$audio" .m4a).txt"

    if [ ! -f "$transcript" ]; then
        echo "Transcribing: $(basename "$audio")"
        whisper "$audio" --output_dir "$TRANSCRIPT_DIR" --output_format txt
    fi
done
EOF

chmod +x /home/jeremy/006-scripts/transcribe-voice-memos.sh

# Add to cron (every hour)
echo "0 * * * * /home/jeremy/006-scripts/transcribe-voice-memos.sh" | crontab -
```

---

## Photo Captioning

**Auto-caption photos for Bob:**

```bash
# Use Gemini Vision to caption photos
pip install google-generativeai

# Auto-caption script
cat > /home/jeremy/006-scripts/caption-photos.sh << 'EOF'
#!/bin/bash
# Caption photos with Gemini Vision

PHOTO_DIR="/home/jeremy/gdrive/GooglePhotos"
CAPTION_DIR="/home/jeremy/gdrive/PhotoCaptions"

mkdir -p "$CAPTION_DIR"

# Find new photos
find "$PHOTO_DIR" -name "*.jpg" -o -name "*.png" | while read photo; do
    caption_file="${CAPTION_DIR}/$(basename "$photo" .jpg).txt"

    if [ ! -f "$caption_file" ]; then
        echo "Captioning: $(basename "$photo")"
        # Call Gemini Vision API
        python3 /home/jeremy/006-scripts/caption_photo.py "$photo" > "$caption_file"
    fi
done
EOF

chmod +x /home/jeremy/006-scripts/caption-photos.sh
```

---

## Cost Impact

**Phone data processing:**
- Voice transcription (Whisper API): ~$0.006 per minute
- Photo captioning (Gemini Vision): ~$0.0025 per image
- Storage (GCS): ~$0.02 per GB/month
- Vertex AI Search: ~$10/month per GB

**Example monthly costs:**
- 1000 photos captioned: $2.50
- 100 voice memos (5 min each): $3.00
- 5GB phone data storage: $0.10 (GCS) + $50 (Vertex AI)
- **Total phone integration: ~$55/month**

---

## Privacy Considerations

**What goes to Bob:**
- Work documents ✅
- Project notes ✅
- Screenshots of code/design ✅
- Voice memos about work ✅

**What stays private:**
- Personal photos ❌ (unless you want)
- Private messages ❌
- Banking info ❌
- Passwords ❌

**You control:**
- Which folders sync
- What Bob sees
- Retention periods
- Privacy filters

---

## Setup Commands (Quick Start)

```bash
# 1. Install tools
sudo apt-get update
sudo apt-get install -y rclone syncthing

# 2. Configure Google Drive
rclone config
# Follow prompts to add Google Drive

# 3. Mount Google Drive
mkdir -p /home/jeremy/gdrive
rclone mount gdrive: /home/jeremy/gdrive --daemon

# 4. Install Syncthing on phone
# Play Store: https://play.google.com/store/apps/details?id=com.nutomic.syncthingandroid
# App Store: Search "Syncthing"

# 5. Start Syncthing on computer
syncthing
# Open: http://localhost:8384

# 6. Add computer to phone app
# Scan QR code from Syncthing web UI

# 7. Select folders to sync on phone
# Camera, Documents, Voice Memos, etc.

# 8. Test sync
# Take photo on phone → Check /home/jeremy/Sync/ on computer

# 9. Add to Bob's daily sync
# Edit: /home/jeremy/000-projects/iams/bobs-brain/bob-vertex-agent/daily-sync.sh
# Add: rsync -av /home/jeremy/Sync/ $KNOWLEDGE_BASE_DIR/phone/
```

---

## Benefits

**With phone synced to Bob:**

1. **Universal search:** Bob searches computer + phone + cloud
2. **Context everywhere:** Bob knows what you did on phone
3. **Backup:** Phone data backed up to 3 tiers
4. **Cross-device:** Work on phone, Bob remembers
5. **Voice to text:** Speak ideas, Bob indexes them
6. **Photo memory:** Bob describes your screenshots
7. **Complete timeline:** Bob tracks all activity

**Example queries:**
- "What did I write in that note on my phone yesterday?"
- "Find the screenshot I took of the API error"
- "Transcribe the voice memo from this morning"
- "Show me photos related to the hustle project"
- "What was I working on when I took these screenshots?"

---

## Next Steps

1. Choose sync method (Google Drive, Syncthing, or both)
2. Install apps on phone
3. Configure sync folders
4. Test sync to computer
5. Add to Bob's daily ingestion
6. Set up transcription (optional)
7. Configure privacy filters

---

**Ready to set up?** Let me know which method you prefer and we'll get it running!
