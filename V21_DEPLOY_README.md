# V21 Scheduled Crawler Pack

## What changes
- Crawlers run in **GitHub Actions**, not inside Streamlit page requests.
- Public data is written to `data/processed/` and committed back to the repo.
- Streamlit reads only versioned processed evidence.
- Crawler failure is fail-closed: previous VERIFIED data remains; only `crawler_status.csv` shows the error.
- Phase 1 covers South Africa: naamsa monthly sales, Stats SA P7162 freight demand, Foton/Maxus EV-CV competitor specs and prices, plus change detection.

## Deploy
1. Copy **all files/folders** in this pack into the root of your GitHub repo (not only app.py).
2. Commit/push.
3. GitHub → Actions → **Market Data Daily** → Run workflow.
4. Then run **Competitor Monitor Weekly** once manually.
5. Streamlit will redeploy automatically after the Actions commit refreshed CSVs.

## Required GitHub setting
The workflow uses `GITHUB_TOKEN` with `contents: write`. If your repo/branch blocks bot pushes, enable:
`Settings → Actions → General → Workflow permissions → Read and write permissions`, or allow the workflow on the protected branch.

## Schedules
- Market Data Daily: 02:15 UTC every day. Sources publish less frequently, but the collector only commits when data changes.
- Competitor Monitor Weekly: Monday 02:45 UTC.

## Data flow
`official website → collector → validation → data/processed → change detector → GitHub commit → Streamlit`

## Phase 1 source scope
- naamsa official monthly vehicle-sales release
- Statistics South Africa P7162
- Foton South Africa official EV commercial-vehicle pages
- Maxus South Africa official eDeliver 3 page

## Important
Crawler-collected data is public evidence. Internal dealer assessments and manual field data stay in your private Google Sheets layer from V20.
