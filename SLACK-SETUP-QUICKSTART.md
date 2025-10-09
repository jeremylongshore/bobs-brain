# Bob's Brain - Slack Setup Quickstart

**Created:** 2025-10-08
**Status:** ✅ Ready to Connect

---

## 🎯 Current Status

- ✅ Bob running at: `http://localhost:8080`
- ✅ Public tunnel active: `https://editor-steering-width-innovation.trycloudflare.com`
- ✅ All features enabled (conversation memory, caching, knowledge bases)
- ⏳ **Slack needs URL update** (1 minute task)

---

## ⚡ Connect to Slack (30 seconds)

**1. Open Slack App Settings:**
```
https://api.slack.com/apps/A099YKLCM1N/event-subscriptions
```

**2. Update Request URL:**
```
https://editor-steering-width-innovation.trycloudflare.com/slack/events
```

**3. Subscribe to events:** (if not already done)
- `message.channels`
- `message.im`
- `app_mention`

**4. Save Changes**

**5. Test in Slack:**
- Mention @Bob in any channel
- Send a DM to Bob
- Bob will respond with full context awareness!

---

## 📚 Documentation References

**Main Setup Guide (Complete Details):**
`~/security/bobs-brain-cloudflare-tunnel-setup.md`

**Project Docs:**
- Main README: `/home/jeremy/projects/bobs-brain/README.md`
- CLAUDE.md: `/home/jeremy/projects/bobs-brain/CLAUDE.md`
- Slack Credentials: `/home/jeremy/projects/bobs-brain/01-Docs/035-aar-slack-credentials-setup.md`

---

## 🔧 Quick Commands

```bash
# Check if Bob is running
curl http://localhost:8080/health

# Check public tunnel
curl https://editor-steering-width-innovation.trycloudflare.com/health

# View tunnel logs
tail -f /tmp/cloudflared.log

# View Bob logs
tail -f ~/projects/bobs-brain/bob.log

# Restart tunnel if needed
pkill cloudflared
nohup cloudflared tunnel --url http://localhost:8080 > /tmp/cloudflared.log 2>&1 &
```

---

## 🎉 What Bob Can Do in Slack

- **Remember conversations** (last 10 messages per user)
- **Cache responses** (instant replies to repeated questions)
- **Access knowledge bases** (653MB Knowledge DB + Analytics)
- **Smart routing** (uses optimal LLM for each query)
- **Learning** (Circle of Life improves over time)

---

**That's it! Update Slack and start chatting with Bob!** 🚀
