# Issues & Fixes Log

This document tracks all issues discovered and their resolutions.

---

## Issue #1: Non-Functional Email Form on Landing Page

**Date:** November 13, 2025
**Reported by:** User
**Severity:** Medium (UX confusion)

### Problem

The main landing page (`index.html`) at https://sbc1-code.github.io/sbb-dash/ contained:
- A "Join the Beta" email signup form
- Form had no backend integration (non-functional)
- Misleading messaging about "private beta for first 50 businesses"
- Created confusion - users couldn't actually sign up

### Root Cause

During Session 1 (Nov 10), we created a landing page with email capture as part of the original product roadmap (paid beta launch strategy).

During Session 2 (Nov 13), we pivoted to a **community-first approach** with a free automated forecast tool. We built `forecast.html` but forgot to update `index.html` to reflect the new strategy.

### File Structure
```
index.html      ← Landing page (had broken email form) ❌
forecast.html   ← Working forecast tool ✅
dashboard.html  ← Old static prototype (not used)
```

### Fix Applied

**Commit:** `a8b5b69` - "fix: remove non-functional email form, link to working forecast tool"

**Changes to `index.html`:**

1. **Removed email signup form** entirely
2. **Updated hero CTA:**
   - Old: "Request Early Access" → Broken form
   - New: "View Free Forecast" → forecast.html

3. **Updated bottom CTA section:**
   - Old: "Get Your First 30 Days Free" with email form
   - New: "100% Free - Available Now" with link to forecast

4. **Updated messaging:**
   - Removed "private beta" language
   - Added "No signup required. No credit card. Just bookmark the page"
   - Direct link to working forecast tool

### Verification

After fix deployment:
- ✅ Landing page now directs users to working forecast
- ✅ No misleading signup forms
- ✅ Clear messaging about free tool
- ✅ All links functional

### Lessons Learned

1. **Update all pages when pivoting strategy** - We built forecast.html but didn't audit existing pages
2. **Remove non-functional features immediately** - Don't ship placeholders
3. **Keep messaging consistent** - Landing page didn't match actual product

### Future Prevention

- [ ] Create checklist for strategy pivots
- [ ] Audit all HTML files before major deploys
- [ ] Add TODO comments for incomplete features

---

## Page Inventory (Current State)

### ✅ Production Pages
- **forecast.html** - Main product, fully functional, auto-updating daily
- **index.html** - Landing page, now correctly points to forecast.html

### 🗄️ Deprecated/Archive
- **dashboard.html** - Old static prototype from Session 1
  - Status: Not linked from anywhere
  - Action: Keep for reference, may delete later

---

**Last Updated:** November 13, 2025
