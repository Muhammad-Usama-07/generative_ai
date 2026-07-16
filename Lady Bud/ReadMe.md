# 🌸 Female Health Care Chatbot

A women's health platform designed to follow someone through every life stage — childhood education, cycle tracking, pregnancy, postpartum, and menopause — instead of switching between a different app for each phase.

This repo currently contains the **frontend**, built as small, standalone pieces and shipped one at a time.

## Live pieces

| Feature | File | Status |
|---|---|---|
| Marketing / landing page | `landing.html` | ✅ Live |
| Cycle tracker | `index.html` | ✅ Live |
| Pregnancy tracker | `index.html` | ✅ Live |
| Symptom & appointment log | `index.html` | ✅ Live |
| Age-appropriate education module | — | 🔜 Next |
| Accounts & persistent storage (backend) | — | 🔜 Next |
| AI health assistant (educational only) | — | 🔜 Next |

## Project structure

```
bloom/
├── landing.html   # Marketing page — explains the product, links into the app
├── index.html     # The actual tracker app (cycle + pregnancy)
└── README.md
```

Keep both HTML files in the same folder — `landing.html` links to `index.html` via the "Open the tracker" button.

## Running it

No build step, no dependencies. Just open the file in a browser:

```bash
open landing.html   # or index.html to go straight to the tracker
```

Or serve it locally if you prefer:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000/landing.html
```

## What's inside `index.html`

**Onboarding**
- First-visit modal to select a life stage (childhood, adolescence, reproductive years, pregnant, postpartum, perimenopause/menopause). Editable anytime via the stage pill in the header.

**Cycle tracker**
- Circular "cycle wheel" showing current cycle day and phase (menstrual / follicular / ovulation / luteal), driven by average cycle length
- Log period start/end
- Daily symptom chips (cramps, mood swings, fatigue, etc.)
- Monthly calendar highlighting logged and predicted period days
- Cycle history list

**Pregnancy tracker**
- Toggle between "I know my last period date" or "I know my due date" — only one field is active at a time to avoid conflicting inputs
- Week/trimester progress arc with due date estimate
- Animated "growth" visual — an abstract shape (not a literal illustration) that changes animation style across the three trimesters: a soft pulsing seed, a gently floating bud, and a heartbeat-style pulse with small "kick" animations
- Weekly milestone notes
- Pregnancy-specific symptom chips
- Appointment list (add/remove)

## Design system

- **Palette:** warm wine (`#7A2E4D`), gold (`#C9932B`), coral (`#D9776B`), sage (`#6B8F71`) on a warm greige background — deliberately avoiding the generic pink/clinical-white look common in health apps
- **Type:** [Fraunces](https://fonts.google.com/specimen/Fraunces) for display/headings, Work Sans for body text, IBM Plex Mono for numeric data (cycle day, dates)
- **Signature motif:** circular/arc progress shared between the cycle wheel and pregnancy arc, tying the two trackers together visually

## Data & privacy notes

- All data currently lives **in memory only** (JS state) — it resets on page refresh. Persistence lands with the backend.
- No diagnosis is ever given — content is educational, and anything symptom-specific should point to a professional.
- Nothing is sent to a third party; there's no network call in the current version at all.

## Roadmap

1. **Education module** — short, age-appropriate explainers per life stage, starting with childhood/teen content on what periods are
2. **Backend** — FastAPI + database so logs, symptoms, and appointments persist across sessions and devices
3. **AI assistant** — an educational chatbot with guardrails: no diagnosis, always redirects anything symptom-specific to a professional

## Tech

Vanilla HTML/CSS/JS — no framework, no build tools. Kept deliberately simple so each new feature can be built and tested as its own small project before being wired into the main app.
