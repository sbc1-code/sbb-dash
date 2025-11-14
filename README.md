# 🌴 Santa Barbara Business Dashboard (SBB-Dash)

**Free, automated demand forecasting for Santa Barbara businesses**

Live at: **[sbc1-code.github.io/sbb-dash](https://sbc1-code.github.io/sbb-dash)**

---

## 🎯 Mission

Help Santa Barbara businesses make smarter staffing and inventory decisions by providing free, data-driven demand forecasts.

No signups. No costs. No BS. Just helpful data for the community.

---

## 📊 What It Does

### [Business Forecast Tool](https://sbc1-code.github.io/sbb-dash/forecast.html)

**7-Day Demand Predictions** with:
- Smart scoring algorithm (0-100 demand score)
- Real weather data integration
- Local event tracking (concerts, cruise ships, farmers markets)
- Actionable daily recommendations

**Example Output:**
```
Friday 11/15 → HIGH (85/100)
🌡️ Perfect weather 75°F
🎵 Concert at SB Bowl (+25)
💡 Staff up, extend hours, maximize capacity
```

---

## 🤖 Automation

### Fully Automated Daily Updates

The forecast auto-updates **every day at 6 AM Pacific** via GitHub Actions:

1. Scrapes latest weather data (Open-Meteo API)
2. Checks cruise ship schedules (CruiseMapper)
3. Looks for SB Bowl concerts
4. Adds recurring events (Farmers Markets)
5. Calculates demand scores with quality checks
6. Commits updated forecast to GitHub
7. GitHub Pages auto-deploys (live in ~2 min)

### Quality Assurance Features

✅ **Retry logic** - 3 attempts on network failures
✅ **Graceful degradation** - Falls back to static events if scraping fails
✅ **Data validation** - Ensures 7 days of forecast before publishing
✅ **Error reporting** - Logs all failures for debugging

---

## 🛠️ Technical Stack

### 100% Free Tier
- **Hosting:** GitHub Pages (free static hosting)
- **Weather API:** Open-Meteo (free, unlimited for non-commercial)
- **Automation:** GitHub Actions (2,000 minutes/month free)
- **Storage:** Git repository (data as JSON)

### Zero Dependencies
- Pure Python 3 (stdlib only - `urllib`, `json`, `re`)
- Vanilla JavaScript (no frameworks)
- No databases, no servers, no costs

**Monthly Cost:** $0.00

---

## 📁 Project Structure

```
/SBusiness/
├── index.html              # Landing page for email signups
├── dashboard.html          # Original prototype dashboard
├── forecast.html           # Live business forecast tool ⭐
├── forecast_data.json      # Generated forecast data (auto-updated)
├── scraper_v2.py          # Enhanced data scraper with quality checks
├── .github/workflows/
│   └── update-forecast.yml # GitHub Actions automation
├── DEVELOPMENT_LOG.md      # Full project history and roadmap
└── README.md              # This file
```

---

## 🚀 How to Run Locally

### Generate Fresh Forecast

```bash
python3 scraper_v2.py
```

Output:
- `forecast_data.json` - 7 days of forecast data
- Console summary with quality metrics

### View Forecast Locally

```bash
open forecast.html
```

Or use any local web server:
```bash
python3 -m http.server 8000
# Visit: http://localhost:8000/forecast.html
```

---

## 📈 Data Sources

### Weather (Primary)
- **Open-Meteo API** - 7-day forecast for Santa Barbara
- Updates: Hourly
- Reliability: 99.9%+
- Cost: Free

### Events (Scraped)
1. **Cruise Ships** - CruiseMapper.com
   - Arrival dates, ship names, estimated passengers
   - Impact: +25 demand score

2. **SB Bowl Concerts** - sbbowl.com
   - Concert dates, artists
   - Impact: +25 demand score (4,500 capacity)

3. **Farmers Markets** - Static schedule
   - Tuesday & Saturday (recurring)
   - Impact: +15 demand score

### Fallback Strategy
If scraping fails:
- Weather: Required (forecast won't publish without it)
- Events: Optional (uses static recurring events only)

---

## 🧮 Demand Scoring Algorithm

### Base Score: 50/100

### Modifiers:
| Factor | Impact | Reasoning |
|--------|--------|-----------|
| Weekend | +30 | Tourist traffic peaks |
| Friday evening | +20 | Start of weekend rush |
| Perfect weather (65-85°F) | +15 | Ideal for outdoor activities |
| Hot weather (>85°F) | -5 | Reduces foot traffic |
| Cool weather (<60°F) | -10 | Fewer visitors |
| Rain >50% | -20 | Major traffic reducer |
| Rain 30-50% | -10 | Moderate impact |
| Major event (concert, cruise) | +25 | 2,000-4,500 visitors |
| Medium event (farmers market) | +15 | 500-1,000 visitors |

### Demand Levels:
- **HIGH** (75-100): "Staff up, extend hours, maximize capacity"
- **MEDIUM** (55-74): "Normal staffing, run targeted promotions"
- **LOW** (0-54): "Minimal staff, push deals to locals"

---

## 🔄 Manual Updates

### Trigger Forecast Update Manually

**Via GitHub Actions:**
1. Go to: https://github.com/sbc1-code/sbb-dash/actions
2. Select "Update Business Forecast"
3. Click "Run workflow" → "Run workflow"

**Via Terminal:**
```bash
cd /Users/sebastianbecerra/SBusiness
python3 scraper_v2.py
git add forecast_data.json
git commit -m "data: manual forecast update"
git push origin main
```

Live site updates in 1-2 minutes.

---

## 📊 Business Model

### Current Phase: Community Value
- **Price:** FREE
- **Goal:** Help 50+ local businesses
- **Strategy:** Build trust and goodwill first

### Future Monetization (Optional)
Once 30-50 businesses rely on the free tool:

**Premium Tier ($49/mo):**
- Custom SMS/email alerts
- Integration with POS systems
- Historical data analysis
- Promotion distribution platform

**Target:** 35 paying customers = $1,715 MRR (year 1 goal: $3,465 MRR)

---

## 🎯 Roadmap

### ✅ Phase 1: Free Community Tool (DONE)
- [x] Real weather data integration
- [x] Smart demand scoring
- [x] Event scraping (cruises, concerts, markets)
- [x] Automated daily updates
- [x] Quality assurance & error handling
- [x] Professional UI with actionable insights

### 🔄 Phase 2: Distribution & Feedback (IN PROGRESS)
- [ ] Share in local SB business Facebook groups
- [ ] Post on Downtown SB association boards
- [ ] Gather feedback from 10-20 businesses
- [ ] Refine scoring algorithm based on real results

### 📋 Phase 3: Enhanced Features (NEXT)
- [ ] Add more event sources (festivals, conferences)
- [ ] Historical accuracy tracking
- [ ] Weekly email digest option
- [ ] Business-specific customization

### 💰 Phase 4: Premium Features (FUTURE)
- [ ] User authentication
- [ ] Custom alerts (SMS/email)
- [ ] Promotion engine
- [ ] Payment integration (Stripe)

---

## 🤝 Contributing

This is a community project. Improvements welcome!

### Priority Enhancements:
1. Better event scraping (more reliable parsers)
2. More event sources (hotels, convention center)
3. Historical validation (compare predictions to actual traffic)
4. Mobile-optimized UI

---

## 📜 License

MIT License - Free to use, modify, distribute

---

## 📞 Contact

Built with ❤️ for Santa Barbara businesses

Questions or feedback? Open an issue on GitHub.

---

**Last Updated:** November 13, 2025
**Status:** ✅ Live and auto-updating daily
