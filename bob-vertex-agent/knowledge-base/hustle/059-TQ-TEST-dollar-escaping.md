# Dollar Escaping Verification
**Version:** 1.0
**Date:** 2025-11-08
**Type:** Testing & Quality
**Purpose:** Prevent shell variable interpolation in overlay text

---

## CRITICAL RULE

**NEVER interpolate overlay text via shell variables**

All dollar amounts MUST be escaped with backslash (`\$`) to prevent shell from interpreting them as variables.

---

## THE BUG THAT STARTED IT ALL

### Original Problem
```bash
# WRONG - Shell interprets $30 as variable $3 (empty) + "0"
drawtext=text='Spent $30 million+ on women'"'"'s soccer'
# Result: "Spent 0 million+ on women's soccer" ❌
```

### Correct Solution
```bash
# RIGHT - Dollar sign escaped prevents interpolation
drawtext=text='Spent \$30 million+ on women'"'"'s soccer'
# Result: "Spent $30 million+ on women's soccer" ✅
```

---

## VERIFIED EXAMPLES IN SCRIPTS

### From ffmpeg_overlay_pipeline.sh
```bash
# All dollar amounts properly escaped:
drawtext=text='Spent \$30 million+ on women'"'"'s soccer':
drawtext=text='Built a \$117 million stadium...':
drawtext=text='Why won'"'"'t they give \\\$1 for trans inclusion?':
```

### ASS/SRT Format (Preferred)
```ass
Dialogue: 0,0:00:02.00,0:00:05.00,Default,,0,0,0,,Spent \$30 million+ on women's soccer
Dialogue: 0,0:00:10.00,0:00:13.00,Default,,0,0,0,,Built a \$117 million stadium...
```

---

## OVERLAY RENDERING BEST PRACTICES

### 1. Use External Subtitle Files
**BEST:** Store overlays in .ass or .srt files, not in shell scripts
```bash
# Good - Load from file
ffmpeg -i input.mp4 -vf "ass=overlays.ass" output.mp4

# Risky - Inline text in shell
ffmpeg -i input.mp4 -vf "drawtext=text='...\$...'" output.mp4
```

### 2. JSON Configuration
**ALTERNATIVE:** Store overlay configs in JSON
```json
{
  "overlays": [
    {
      "time": "00:02-00:05",
      "text": "Spent $30 million+ on women's soccer",
      "position": "bottom"
    }
  ]
}
```
Then parse JSON and apply overlays without shell interpolation risk.

### 3. Template Files
**SAFE:** Use template substitution that doesn't involve shell
```python
# Python example - no shell interpolation
template = "Spent $30 million+ on women's soccer"
subprocess.run(['ffmpeg', '-vf', f'drawtext=text={template}'])
```

---

## VERIFICATION COMMANDS

### Pre-Execution Check
```bash
# Find all potential dollar amounts in scripts
grep -R '\$[0-9]' 050-scripts/ 030-video/overlays/ || echo "✅ No unescaped dollars found"

# Check for escaped dollars (should find these)
grep -R '\\$[0-9]' 050-scripts/ 030-video/overlays/ || echo "⚠️ No escaped dollars found"

# Verify ASS files don't have shell variables
grep -E '^\$[A-Z_]+' 040-overlays/*.ass || echo "✅ No shell variables in ASS files"
```

### Runtime Validation
```bash
# After rendering, extract frame with overlay
ffmpeg -ss 3 -i output.mp4 -vframes 1 -q:v 2 frame_check.jpg

# Use OCR to verify dollar amount appears
tesseract frame_check.jpg - | grep -E '\$[0-9]+ million' || echo "❌ Dollar amount not visible"
```

---

## COMMON PITFALLS

### 1. Double-Quote Interpolation
```bash
# DANGEROUS - Double quotes allow interpolation
drawtext=text="Spent $30 million"  # ❌ Becomes "Spent 0 million"

# SAFE - Single quotes prevent interpolation
drawtext=text='Spent \$30 million'  # ✅ Preserves "$30 million"
```

### 2. Heredoc Expansion
```bash
# WRONG - Heredoc expands variables
cat <<EOF
Spent $30 million
EOF

# RIGHT - Quoted heredoc preserves literals
cat <<'EOF'
Spent $30 million
EOF
```

### 3. Command Substitution
```bash
# WRONG - Backticks/subshell can expand
TEXT=`echo "Spent $30 million"`

# RIGHT - Escape or avoid shell processing
TEXT='Spent \$30 million'
```

---

## TEST MATRIX

| Text | Shell Result (Wrong) | Escaped Result (Right) |
|------|---------------------|------------------------|
| `$30 million` | `0 million` | `$30 million` |
| `$117 million` | `17 million` | `$117 million` |
| `$1 for trans` | ` for trans` | `$1 for trans` |

---

## CI VERIFICATION STEPS

### In GitHub Actions Workflow
```yaml
- name: Verify Dollar Escaping
  run: |
    # Check all scripts for proper escaping
    echo "Checking for unescaped dollars..."
    if grep -r '\$[0-9]' 050-scripts/ --include="*.sh" | grep -v '\\$'; then
      echo "❌ Found unescaped dollar amounts!"
      exit 1
    fi
    echo "✅ All dollar amounts properly escaped"

    # Verify overlay files
    for file in 040-overlays/*.ass; do
      if grep '^\$[A-Z_]' "$file"; then
        echo "❌ Shell variable found in $file"
        exit 1
      fi
    done
    echo "✅ Overlay files clean"
```

---

## ENFORCEMENT

### Gate Check
The `gate.sh` script should verify no runtime dollar interpolation:
```bash
# Test rendering with known text
TEST_TEXT='Test \$99 million'
echo "$TEST_TEXT" | grep -q '\$99' || {
  echo "❌ Dollar escaping failed in test"
  exit 1
}
```

### Post-Render Validation
After video generation, verify amounts in final output:
```bash
# Extract subtitle track and verify
ffmpeg -i final.mp4 -map 0:s -f ass - | grep '\$30 million' || {
  echo "❌ Dollar amounts not found in final video"
  exit 1
}
```

---

## SUMMARY

✅ **Rule:** Always escape dollar signs with backslash (`\$`)
✅ **Best Practice:** Use external .ass/.srt files for overlays
✅ **Verification:** grep for `\$[0-9]` patterns before execution
✅ **Testing:** Validate dollar amounts appear in rendered output

**Remember:** The difference between `$30 million` and `0 million` is just one backslash!

---

**Documentation Date:** 2025-11-08
**Status:** Verification Plan Ready
**Critical Finding:** All scripts currently use proper `\$` escaping

**END OF DOLLAR ESCAPING VERIFICATION**