<div align="center">

# Economic Resilience Snapshot

### Interactive Power BI dashboard for 20 years of macroeconomic data across 26 advanced economies.

[![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/desktop/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://img.shields.io/badge/validate--data-passing-brightgreen)](.github/workflows/ci.yml)

</div>

## Why this exists

Macroeconomic resilience is easy to talk about and hard to look at.
This project takes 20 years of IMF World Economic Outlook data, filters it
down to the 26 high-income economies that report consistently across the
entire 2001 to 2020 window, and presents it as a single-screen Power BI
report aimed at policy-curious non-specialists.

The headline question the dashboard supports: **how did advanced economies
respond to the 2008 to 2010 global financial crisis, and what shape were
they in entering 2020?**

## What is in this repo

```
dashboard/
├── powerbi/economic_resilience_snapshot.pbix   # the main deliverable
├── data/
│   ├── data.xlsx                  # IMF WEO October 2021 vintage
│   ├── country_groupings.xlsx     # World Bank region + income classes
│   └── metadata.xlsx              # WEO indicator definitions
├── docs/
│   ├── architecture.md            # tables, relationships, field parameter
│   ├── measures.md                # the nine DAX measures
│   ├── methodology.md             # filter rule + indicator selection
│   └── insights.md                # how to read the dashboard
├── scripts/validate_data.py       # CLI runner for the validator
├── src/er_dashboard/              # validator package
└── tests/                         # pytest covering the validator
```

## Data model

```
+----------------------+              +-----------------------+
|     IMF_Complete     |  many-to-1   |    CountryGroupings   |
|----------------------|------------->|-----------------------|
|  ISO     (FK)        |   on ISO     |  Code   (PK)          |
|  Country             |              |  Economy              |
|  Year                |              |  Region               |
|  8 core indicators   |              |  Income group         |
+----------------------+              +-----------------------+
   26 countries x 20 yrs                  218 reference rows
   = 520 fact rows
```

Eight core indicators feed nine DAX measures. A field parameter named
Metric Selector exposes those eight indicators through a single dropdown
that drives both the trend line and the top-10 bar chart.

## Key indicators

| Indicator | Unit | Aggregation |
|---|---|---|
| GDP, current prices | USD | sum |
| GDP growth | % per year | average |
| Inflation, end-of-period CPI | % per year | average |
| Unemployment | % of labour force | average |
| Government gross debt | % of GDP | average |
| Current account balance | % of GDP | average |
| GDP per capita, current prices | USD | average |
| Output gap | % of potential GDP | average |

Full definitions live in `data/metadata.xlsx` and `docs/measures.md`.

## How to open

1. Install [Power BI Desktop](https://powerbi.microsoft.com/desktop/)
   (free).
2. Open `powerbi/economic_resilience_snapshot.pbix`.
3. If prompted, point the data source at `data/data.xlsx` (and the two
   companion files) in this repo.
4. Refresh. The full model loads in under 2 seconds.

## Methodology highlights

- **Complete-case filter.** Only countries with all 20 years of non-null
  observations across the eight core indicators are retained. This avoids
  imputation and the bias that comes with it.
- **Stock vs rate aggregation.** GDP and GDP per capita aggregate as
  sums; growth, inflation, unemployment, debt %, current account %, and
  output gap aggregate as averages.
- **Single-screen layout.** Slicers on the left, KPI cards on the right,
  trend line and scatter plot in the centre, top-10 bar chart bottom
  right. Designed to print and share without scrolling.

See `docs/methodology.md` for the full Power Query pipeline.

## Validation

The dataset descriptors quoted in this README are not aspirational, they
are asserted on every CI run.

```bash
make install    # editable install with dev extras
make validate   # python scripts/validate_data.py --data-dir data
make lint       # ruff + black --check
make test       # pytest
```

`make validate` re-applies the complete-case filter against the actual
xlsx files and fails if the country count, observation count, year span,
or core-indicator coverage drift from the published numbers.

## Limitations

- 26 advanced, high-income economies. No emerging markets, no fragile
  states. The completeness rule is the cause; addressing it would require
  imputation or accepting case-by-case deletion.
- Annual granularity. Within-year shocks (e.g. April 2020) are invisible.
- Descriptive, not causal. The scatter plot reveals correlation, not
  mechanism.

## Possible extensions

- Bring in 2021 to 2024 vintages and re-validate the filter.
- Add a comparison page using PPP-adjusted GDP per capita.
- Layer in a structural overlay (demographics, productivity) on a second
  page.
- Publish to Power BI Service with row-level security on region.

## License

MIT. See [LICENSE](LICENSE).

## Author

**Marvis Osazuwa.** Analytics Engineer / Data Scientist with seven years
across banking, healthcare, and marketing analytics. Builds end-to-end
analytics products from data ingestion through to executive-ready
visualisation.

- Portfolio: [marz1307.github.io](https://marz1307.github.io)
- LinkedIn: [marvisosazuwa](https://www.linkedin.com/in/marvisosazuwa)
