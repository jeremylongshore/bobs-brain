# DiagnosticPro — Frontend API Key + Deploy + Proof (FINAL)

**Date:** 2025-09-25T20:50:00Z
**Status:** 🚧 IN PROGRESS - Implementing frontend API key configuration

---

## 0) Invariants (confirmed)
- Gateway host: https://diagpro-gw-3tbssksx-3tbssksx.uc.gateway.dev ✅
- Protected routes require header: x-api-key ✅
- Backend secrets (KEEP PRIVATE in Cloud Run):
  - STRIPE_SECRET_KEY=sk_live_REDACTED ✅
  - STRIPE_WEBHOOK_SECRET=whsec_o2MWZ5ONqy9ODkA3ckD2FFPOQMsbnAFQ ✅
  - REPORT_BUCKET=diagnostic-pro-prod_diagnostic-reports ✅

---

## Firebase Project Status
Current Firebase hosting site: https://diagnostic-pro-prod.web.app
Project: diagnostic-pro-prod
App ID: 1:298932670545:web:d710527356371228556870

---

## 1) Frontend Environment - SEARCHING FOR SOURCE