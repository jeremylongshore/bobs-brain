# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The NWSL directory contains a sophisticated video documentary generation pipeline that produces a 60-second video exposing NWSL's transgender policy. It uses Google Cloud Vertex AI's Veo 3.0 for video generation and Lyria for audio, with comprehensive CI/CD automation via GitHub Actions.

## Architecture & Pipeline

### Core Pipeline Flow
1. **Canon Specifications** → Video/Audio Generation → Assembly → Final Output
2. **CI-Only Execution**: Enforced through GitHub Actions with Workload Identity Federation (no local execution)
3. **9-Segment Assembly**: 8 video segments (8s each) + end card (4s) = 68 seconds total

### Directory Structure
```
nwsl/
├── 000-docs/              # Canon specifications and documentation
│   ├── 004-011-*.md      # Veo segment prompts (SEG-01 to SEG-08)
│   ├── 6767-*.md         # Master briefs and templates
│   └── *-AA-AACR-*.md    # After Action reports
├── 001-assets/            # Reference images for Imagen
├── 020-audio/music/       # Lyria-generated audio (60.04s instrumental)
├── 030-video/shots/       # Veo-generated video segments
├── 040-overlays/          # Text overlays and subtitles
├── 050-scripts/           # Core pipeline scripts
├── 060-renders/final/     # Final assembled video output
└── gate.sh               # CI enforcement gate
```

### Key Pipeline Scripts
- `gate.sh` - Enforces CI-only execution with WIF authentication
- `050-scripts/lyria_render.sh` - Generates 60s instrumental score
- `050-scripts/veo_render.sh` - Generates 8 video segments from canon
- `050-scripts/ffmpeg_assembly_9seg.sh` - Assembles 9-segment final video
- `050-scripts/query_vertex_logs.sh` - Vertex AI observability

## Common Commands

### CI/CD Pipeline (GitHub Actions Only)
```bash
# Trigger full pipeline via GitHub Actions
# Go to Actions tab → "Assemble NWSL Documentary" → Run workflow

# Dry run mode (uses placeholders)
# Select: dry_run = true

# Production mode (actual Vertex AI generation)
# Select: dry_run = false
```

### Local Development (Limited - Most Operations CI-Only)
```bash
# Navigate to NWSL directory
cd /home/jeremy/000-projects/hustle/nwsl

# Verify canon files exist
ls -la 000-docs/*-DR-REFF-veo-seg-*.md

# Check pipeline scripts
ls -la 050-scripts/*.sh

# View generation switches configuration
cat 000-docs/032-OD-CONF-generation-switches.md

# Check vertex operations log (after CI run)
cat vertex_ops.log
```

## Canon Specification System

### Segment Mapping
Each video segment has a corresponding canon file:
- SEG-01 → `000-docs/004-DR-REFF-veo-seg-01.md` (The Innocence)
- SEG-02 → `000-docs/005-DR-REFF-veo-seg-02.md` (The Commissioner)
- SEG-03 → `000-docs/006-DR-REFF-veo-seg-03.md` (Michele Kang)
- SEG-04 → `000-docs/007-DR-REFF-veo-seg-04.md` (Angie Long)
- SEG-05 → `000-docs/008-DR-REFF-veo-seg-05.md` (The Wilfs)
- SEG-06 → `000-docs/009-DR-REFF-veo-seg-06.md` (Fallout)
- SEG-07 → `000-docs/010-DR-REFF-veo-seg-07.md` (Empty Fields)
- SEG-08 → `000-docs/011-DR-REFF-veo-seg-08.md` (Title Card)

### Canon Format
```markdown
---
Segment: N
Duration: Xs
Scene: Description
---

[Veo prompt content]

Conditioning: [Visual requirements]
Aspect: 16:9
Audio: FALSE
```

## Vertex AI Configuration

### Models Used
- **Veo 3.0**: `veo-3.0-generate-001` - Video generation (1080p, 16:9)
- **Lyria**: Music generation model - 60s instrumental score
- **Imagen 3**: Reference image generation for styleboards

### API Endpoints
- Region: `us-central1`
- Project: `hustleapp-production` (CI only)
- Endpoints: `https://us-central1-aiplatform.googleapis.com/v1/`

### Generation Parameters
```json
{
  "aspectRatio": "16:9",
  "resolution": "1080p",
  "durationSeconds": 8,  // 4 for end card
  "generateAudio": false,
  "sampleCount": 1
}
```

## GitHub Actions Workflows

### Main Workflow: `.github/workflows/assemble.yml`
1. **Authentication**: Workload Identity Federation (no service account keys)
2. **Gate Check**: Enforces CI-only execution
3. **Canon Import**: Syncs specifications from NWSL repo
4. **Generation**: Lyria audio → Veo video segments
5. **Assembly**: FFmpeg 9-segment pipeline with overlays
6. **QC**: Quality control and duration validation
7. **Upload**: Artifacts to GCS and GitHub

### Environment Variables (CI)
```bash
PROJECT_ID=hustleapp-production
REGION=us-central1
GCS_BUCKET=gs://hustleapp-production-media
DRY_RUN=true/false
```

## Assembly Pipeline

### 9-Segment Structure
1. Segments 1-8: 8.0 seconds each (video content)
2. Segment 9: 4.01 seconds (end card)
3. Total duration: 68.04 seconds
4. Audio: 60.04 seconds (ends before segment 9)

### FFmpeg Assembly (`ffmpeg_assembly_9seg.sh`)
- Concatenates 9 video segments
- Adds instrumental audio track (60.04s)
- Applies text overlays if present
- Exports to H.264/AAC in MP4 container

## Quality Control

### Acceptance Criteria
- File size > 50MB (indicates good quality)
- Duration: 68.04 seconds (±0.1s tolerance)
- Resolution: 1920x1080 (16:9)
- Frame rate: 24fps
- Audio: 48kHz stereo

### Validation Scripts
- `050-scripts/video_qc.sh` - Video quality checks
- `050-scripts/audio_qc.sh` - Audio loudness validation
- `050-scripts/generate_checksums.sh` - File integrity

## Troubleshooting

### Common Issues
```bash
# Check CI execution logs
# Go to GitHub Actions → workflow run → view logs

# Verify WIF authentication
gcloud auth list --filter=status:ACTIVE

# Check Vertex AI quotas
gcloud compute project-info describe --project=hustleapp-production

# View generation failures
cat nwsl/000-docs/*-LS-STAT-*.md  # Error documentation

# Inspect vertex operations
cat nwsl/vertex_ops.log
```

### Debug Mode
Set `DRY_RUN=true` in GitHub Actions to use placeholder media instead of Vertex AI

## Documentation Standards

All documentation follows Document Filing System v2.0:
- Format: `NNN-CC-TYPE-description.md`
- Categories: PP (Planning), AT (Architecture), AA (After Action), etc.
- Flat structure in `000-docs/` directory

## Important Notes

1. **CI-Only Execution**: The pipeline CANNOT run locally - it requires GitHub Actions WIF
2. **Canon Lock**: Video prompts in `004-011-*.md` files are production-critical
3. **Cost Control**: Each full run costs ~$50 in Vertex AI credits
4. **No Manual Edits**: All segments generated via AI, assembled programmatically
5. **Artifact Storage**: Outputs stored in GCS under `ci/{run_id}/`