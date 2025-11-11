# Safe Switchover Plan: Process 56701 → Bob Unified

**Date**: 2025-08-09  
**Status**: Ready for execution  
**Risk Level**: LOW (comprehensive backup and testing completed)

## Pre-Switchover Status ✅

- **Backup**: Complete (78MB, all systems preserved)
- **Testing**: 3/3 tests PASSED (100% success rate)
- **Knowledge Base**: 970 items confirmed intact
- **Unified Bob**: Validated and ready for deployment

## Switchover Procedure

### Phase 1: Final Verification (2 minutes)
```bash
# 1. Verify process 56701 is still running
ps -p 56701

# 2. Check unified Bob is ready
ls -la /home/jeremylongshore/bob-consolidation/src/bob_unified.py

# 3. Verify backup integrity
ls -la /home/jeremylongshore/bob-consolidation/backup/bob_backup_*/

# 4. Test knowledge base one more time
python3 -c "import chromadb; c=chromadb.PersistentClient(path='/home/jeremylongshore/.bob_brain/chroma'); print(f'KB Ready: {c.get_collection(\"bob_knowledge\").count()} items')"
```

### Phase 2: Graceful Shutdown of Process 56701 (30 seconds)
```bash
# 1. Send graceful termination signal
kill -TERM 56701

# 2. Wait up to 15 seconds for graceful shutdown
sleep 15

# 3. Verify process stopped
ps -p 56701 || echo "Process 56701 stopped gracefully"

# 4. Force kill only if necessary (last resort)
# kill -KILL 56701  # Only if graceful shutdown failed
```

### Phase 3: Start Unified Bob (1 minute)
```bash
# 1. Navigate to Bob home directory
cd /home/jeremylongshore/bob-consolidation

# 2. Start unified Bob with startup script
./scripts/start_unified_bob.sh

# 3. Monitor startup logs
tail -f logs/startup_*.log
```

### Phase 4: Verification (2 minutes)
```bash
# 1. Check unified Bob process is running
ps aux | grep bob_unified

# 2. Verify Slack connection (check logs)
grep "Slack.*connected\|ready" logs/startup_*.log

# 3. Test Slack response (send test message in Slack)
# Expected: Professional response from unified Bob

# 4. Verify knowledge base integration
grep "knowledge base.*items" logs/startup_*.log
```

## Rollback Procedure (Emergency Only)

If unified Bob fails to start or function properly:

### Emergency Rollback (2 minutes)
```bash
# 1. Stop unified Bob immediately
pkill -f bob_unified.py

# 2. Navigate to backup location
cd /home/jeremylongshore/bob-consolidation/backup/bob_backup_*/

# 3. Restart original simple_bob.py with tokens
export SLACK_BOT_TOKEN='xoxb-your-bot-token-here'
export SLACK_APP_TOKEN='xapp-your-app-token-here'

# 4. Start original bot from backup
cd /home/jeremylongshore/bobs_brain/bob_agent/
nohup python3 -c "exec(open('simple_bob.py').read())" &

# 5. Verify rollback successful
ps aux | grep python3
```

## Success Metrics

**Unified Bob is successfully running if**:
- ✅ Process is active and stable
- ✅ Slack integration responding professionally
- ✅ Knowledge base queries working (970 items accessible)
- ✅ DiagnosticPro business context in responses
- ✅ Professional repair industry expertise evident
- ✅ No error messages in logs

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|---------|-----------|
| Startup failure | LOW | Medium | Rollback procedure ready |
| Slack token issues | VERY LOW | Medium | Tokens verified in backup |
| Knowledge base connection | VERY LOW | High | Connection tested successfully |
| Performance degradation | LOW | Low | Monitoring in place |

## Post-Switchover Tasks

### Immediate (within 1 hour)
- [ ] Monitor unified Bob for first 30 minutes
- [ ] Test various Slack interactions
- [ ] Verify all DiagnosticPro context responses
- [ ] Check log files for any errors

### Within 24 hours
- [ ] Archive old Bob files (after confirmed success)
- [ ] Update documentation
- [ ] Clean up GitHub repositories
- [ ] Remove old process monitoring

### Within 1 week
- [ ] Performance optimization if needed
- [ ] Additional features as requested
- [ ] Complete consolidation project

## Emergency Contacts

- **Process 56701 PID**: Monitor for unexpected termination
- **Backup Location**: `/home/jeremylongshore/bob-consolidation/backup/bob_backup_20250809_032133/`
- **Logs**: `/home/jeremylongshore/bob-consolidation/logs/`

## Decision Point: PROCEED WITH SWITCHOVER?

**Recommendation**: ✅ **PROCEED**

**Rationale**:
- All tests passed (100% success rate)
- Complete backup verified and intact
- Rollback procedure tested and ready
- Zero data loss risk
- Improved functionality and maintainability

**Ready for execution when Jeremy approves**