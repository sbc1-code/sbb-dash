# Santa Barbara Business Dashboard - Development Log

## Project Status: Landing Page Live ✅

**Live URLs:**
- Landing Page: https://sbc1-code.github.io/sbb-dash/
- Dashboard Prototype: https://sbc1-code.github.io/sbb-dash/dashboard.html

**GitHub Repository:** https://github.com/sbc1-code/sbb-dash

---

## Session 1: Project Kickoff & Deployment (Nov 10, 2025)

### Completed Tasks ✅
1. ✅ Read business analysis document - understood the micro-SaaS model ($99/mo, $3.5k MRR Year 1 target)
2. ✅ Initialized Git repository in `/Users/sebastianbecerra/SBusiness/`
3. ✅ Created `.gitignore` file for web project
4. ✅ Added all project files to repository
5. ✅ Made initial commit: "feat: v1.0 initial prototype and business analysis"
6. ✅ Created public GitHub repository `sbb-dash`
7. ✅ Set up SSH authentication (key: Macbook Air M1)
8. ✅ Linked local repository to remote GitHub repo
9. ✅ Pushed main branch to remote
10. ✅ Enabled GitHub Pages on main branch
11. ✅ Verified deployment - site is LIVE

---

## Current State Analysis

### What We Have:
- **index.html** - Public landing page with email capture form (currently non-functional)
- **dashboard.html** - Static prototype with hardcoded data showing:
  - 7-Day Demand Forecast (hardcoded)
  - Visitor Insights Chart (Chart.js doughnut chart)
  - Local Promotion Engine (UI only, no backend)
- **Business Analysis document** - Complete market sizing and revenue projections

### What's Missing (To Start Charging $99/mo):
1. Email collection backend (no leads being captured currently)
2. Real data integration for demand forecasting
3. Live TOT/sales tax data for visitor insights
4. Functional promotion engine with database
5. User authentication system
6. Payment/subscription system (Stripe)

---

## Next Steps - Development Roadmap

### Phase 1: Email Collection & Validation (PRIORITY)
**Goal:** Start capturing beta signups immediately
- [ ] Connect landing page email form to backend (Options: Google Sheets, Airtable, Firebase, or EmailOctopus)
- [ ] Add form submission confirmation message
- [ ] Set up notification when new signup happens
- [ ] Track conversion rate

**Estimated Time:** 2-4 hours
**Business Impact:** Start building waitlist immediately

---

### Phase 2: Core Product MVP (The "$99/mo Value")

#### 2.1 - 7-Day Demand Forecast Engine
**Goal:** Provide actual value that justifies $99/mo subscription
- [ ] Research and identify data sources:
  - Santa Barbara hotel booking data (Visit Santa Barbara API?)
  - Cruise ship schedules (Port of Santa Barbara)
  - Local events (SB Bowl, theaters, festivals)
  - Historical sales tax / TOT data
- [ ] Build data aggregation pipeline
- [ ] Create forecasting algorithm (weighted scoring system)
- [ ] Replace hardcoded forecast in dashboard.html with real data
- [ ] Add auto-refresh mechanism (daily updates)

**Estimated Time:** 2-3 weeks
**Technical Stack Suggestion:** Firebase Functions + Cloud Scheduler OR Vercel Serverless Functions

#### 2.2 - Visitor Insights Dashboard
**Goal:** Show real-time visitor composition (domestic vs international)
- [ ] Integrate with Santa Barbara TOT (Transient Occupancy Tax) data
- [ ] Connect to sales tax revenue reports (if accessible)
- [ ] Build API endpoint to serve visitor profile data
- [ ] Update Chart.js visualization with live data
- [ ] Add "Key Insight" AI-generated recommendations

**Estimated Time:** 1-2 weeks

#### 2.3 - Promotion Engine
**Goal:** Allow businesses to create and distribute promotions
- [ ] Set up database for promotions (Firebase Firestore or Supabase)
- [ ] Build promotion creation form with validation
- [ ] Create promotion display/distribution mechanism
- [ ] Add promotion analytics (views, clicks, redemptions)
- [ ] (Future) SMS/email distribution to opt-in visitors

**Estimated Time:** 1-2 weeks

---

### Phase 3: Business Infrastructure

#### 3.1 - User Authentication
- [ ] Implement user registration/login (Firebase Auth, Auth0, or Supabase Auth)
- [ ] Create user profile management
- [ ] Add business profile setup (business name, category, location)
- [ ] Build multi-tenant dashboard (each user sees their own data)

**Estimated Time:** 1 week

#### 3.2 - Payment & Subscription System
- [ ] Set up Stripe account
- [ ] Integrate Stripe Checkout for $99/mo subscription
- [ ] Build subscription management dashboard
- [ ] Implement trial period logic (30 days free)
- [ ] Add payment failure handling
- [ ] Create cancellation flow

**Estimated Time:** 1 week

#### 3.3 - Admin Panel
- [ ] Build admin dashboard to manage users
- [ ] Add subscription monitoring
- [ ] Create manual data override capability (for early customers)
- [ ] Add analytics dashboard (MRR, churn rate, active users)

**Estimated Time:** 3-5 days

---

## Product Development Strategy - Two Paths Forward

### Option A: "Concierge MVP" (Recommended for Speed)
**Timeline:** Launch in 1-2 weeks
**Approach:** Manual + Automated Hybrid

1. **Week 1:** Build email collection + basic auth + Stripe
2. **Week 2:** Sign up first 5-10 customers at $99/mo
3. **Manually create** weekly forecast reports (Google Sheets + email)
4. **Build automation** while getting paid by early customers
5. **Gradually replace manual work** with automated systems

**Pros:**
- Validate demand immediately
- Start generating revenue in 2 weeks
- Learn what customers actually want
- Build the right features based on feedback

**Cons:**
- Initial manual work (5-10 hours/week)
- Not scalable beyond ~20 customers

---

### Option B: "Full Product First"
**Timeline:** Launch in 6-8 weeks
**Approach:** Build everything before charging

1. **Weeks 1-2:** Data pipeline + forecast engine
2. **Weeks 3-4:** Visitor insights + promotion engine
3. **Weeks 5-6:** Auth + payments + admin panel
4. **Weeks 7-8:** Testing + refinement
5. Launch to beta list

**Pros:**
- Professional, polished product at launch
- Fully automated from day 1
- Scalable immediately

**Cons:**
- 2 months before first dollar
- Risk of building wrong features
- Higher upfront time investment

---

## Technical Stack Recommendations

### Free/Low-Cost Stack (Recommended for MVP):
- **Hosting:** GitHub Pages (free) - ✅ Already set up
- **Backend:** Firebase (free tier: 125k reads/day, 50k writes/day)
  - Authentication
  - Firestore database
  - Cloud Functions for serverless API
- **Payments:** Stripe (2.9% + 30¢ per transaction)
- **Email Collection:** EmailOctopus or Airtable (free tier)
- **Charts:** Chart.js (free) - ✅ Already integrated

**Monthly Cost for 0-35 customers:** ~$0-50/month
**Margin:** >90%

### Alternative Stack (If You Prefer):
- **Backend:** Vercel + Supabase
- **Auth:** Supabase Auth
- **Database:** Supabase PostgreSQL
- **Functions:** Vercel Serverless Functions

---

## Key Business Metrics to Track

### Year 1 Goals (from Business Analysis):
- **Target Customers:** 35 businesses
- **Target MRR:** $3,465/month
- **Target ARR:** $41,580/year
- **Price Point:** $99/month
- **Market Size (SAM):** 350 businesses in Santa Barbara
- **Total Market Potential:** $415,800 ARR (100% penetration)

### Metrics to Monitor:
1. **Email signups** (waitlist conversion rate)
2. **Beta → Paid conversion rate** (target: >50%)
3. **Churn rate** (target: <5%/month)
4. **Time to value** (how fast do customers see ROI?)
5. **Customer acquisition cost** (CAC)
6. **Lifetime value** (LTV)

---

## Data Sources to Research

### Critical Data Sources Needed:
1. **Hotel Booking Data**
   - Visit Santa Barbara (official tourism bureau)
   - STR (Smith Travel Research) - hotel data provider
   - Google Hotel Insights

2. **Cruise Ship Schedules**
   - Port of Santa Barbara public schedules
   - CruiseMapper API

3. **Local Events**
   - Santa Barbara Bowl event calendar
   - Downtown Santa Barbara events
   - City of Santa Barbara events API (if available)
   - Eventbrite API (for local events)

4. **Economic Data**
   - Santa Barbara TOT (Transient Occupancy Tax) reports
   - Sales tax revenue (City of Santa Barbara finance dept)
   - Visitor spending reports (Visit Santa Barbara)

5. **Weather Data**
   - OpenWeather API (free tier available)

---

## Questions to Resolve Before Next Session

1. **Which development path?** Concierge MVP (Option A) vs Full Product (Option B)?
2. **Email collection preference?** Google Sheets, Airtable, Firebase, or EmailOctopus?
3. **Backend preference?** Firebase or Supabase?
4. **Data access:** Do you have any connections to Santa Barbara tourism/city data sources?
5. **Timeline:** When do you want to start charging customers?

---

## Git Workflow Established

```bash
# Working directory
cd /Users/sebastianbecerra/SBusiness

# To make changes and deploy:
git add .
git commit -m "your message here"
git push origin main

# GitHub Pages auto-deploys from main branch
# Live site updates in ~1-2 minutes
```

---

## Notes for Next Session

- Landing page is live but email form is non-functional (no backend)
- Dashboard is pure frontend prototype with no real data
- Need to decide on MVP strategy before building
- Consider reaching out to 5-10 local businesses to validate demand before building
- SSH key configured and working (Macbook Air M1)

---

**Last Updated:** November 10, 2025
**Next Session Priority:** Email collection setup OR finalize MVP strategy
