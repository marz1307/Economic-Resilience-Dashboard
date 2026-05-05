# Data Model Architecture

## Overview

The dashboard is built on a classic star-style schema with one fact table
and one dimension table. Power BI loads both via Power Query from the
`data/` directory.

## Tables

### Fact: `IMF_Complete`

Country-year observations after applying the complete-case filter.

| Column | Type | Description |
|---|---|---|
| ISO | text | World Bank three-letter ISO code (join key) |
| Country | text | Country display name |
| Year | integer | 2001 through 2020 |
| GDP_Current_USD | decimal | GDP at current prices, USD |
| GDP_Growth_Pct | decimal | GDP growth, annual % |
| Inflation_Pct | decimal | End-of-period CPI, % change |
| Unemployment_Pct | decimal | Unemployment, % of labour force |
| Gov_Gross_Debt_Pct_GDP | decimal | General government gross debt, % of GDP |
| Current_Account_Pct_GDP | decimal | Current account balance, % of GDP |
| GDP_Per_Capita_USD | decimal | GDP per capita at current prices, USD |
| Output_Gap_Pct | decimal | Output gap, % of potential GDP |

Cardinality: 26 countries x 20 years = 520 rows after filtering.

### Dimension: `CountryGroupings`

| Column | Type | Description |
|---|---|---|
| Code | text | ISO three-letter code (join key) |
| Economy | text | Country / economy display name |
| Region | text | World Bank region |
| Income group | text | World Bank income classification |

## Relationships

```
+----------------------+              +-----------------------+
|     IMF_Complete     |  many-to-1   |    CountryGroupings   |
|                      |------------->|                       |
|  ISO  (FK)           |   on ISO     |  Code  (PK)           |
|  Year                |              |  Region               |
|  8 indicator columns |              |  Income group         |
+----------------------+              +-----------------------+
```

- Cardinality: many (`IMF_Complete`) to one (`CountryGroupings`)
- Cross-filter direction: both
- Active relationship

## Field parameter

A field parameter named `Metric Selector` exposes the eight core indicators
as a single dropdown that drives the trend line and the top-10 bar chart.

## Refresh notes

- All sources are local Excel files; refresh runs in under 2 seconds on a
  modest laptop.
- The Power Query step set (helper-query, inner-join filter, null check,
  column reduction) is documented in `docs/methodology.md`.
