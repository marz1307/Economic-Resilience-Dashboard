# Methodology

## Source data

- Primary file: IMF World Economic Outlook, October 2021 vintage,
  `data/data.xlsx`. 3,893 rows covering 196 countries, 20 years, 44
  indicators.
- Country classification: World Bank list of economies,
  `data/country_groupings.xlsx`. 218 economies with region and income group.
- Indicator definitions: `data/metadata.xlsx`. 44 WEO subject codes with
  descriptors, units, and scale.

## Country selection: complete-case filtering

The dashboard prioritises analytical integrity over geographic breadth. A
country is included only if it has all 20 years of non-null observations
across the eight core indicators. Imputation and case-by-case deletion were
rejected because both introduce hidden assumptions or systematic bias when
missingness correlates with crisis periods.

The Power Query pipeline applies the rule in four steps:

1. **Helper query.** Group the raw IMF table by ISO and count distinct
   years.
2. **Complete-country filter.** Inner-join the raw table against the helper
   table on `YearCount = 20`. This drops countries with any year missing.
3. **Null verification.** For each of the eight core indicator columns,
   confirm zero nulls remain.
4. **Column reduction.** Drop indicator columns the dashboard does not use
   (PPP variants, employment counts, granular fiscal lines).

Applying this rule to the supplied data yields **26 countries** and
**520 country-year observations** (see `CORRECTIONS.md` for the discrepancy
with the original write-up that quoted 22 countries).

## Indicator selection

The eight core indicators were chosen for two reasons:

- **Coverage.** They are present without nulls for the 26 retained
  countries across all 20 years.
- **Coverage of the macro picture.** Together they span economy size
  (GDP, GDP per capita), growth dynamics (growth rate, output gap), price
  stability (inflation), labour market health (unemployment), fiscal
  sustainability (debt %), and external balance (current account %).

| Indicator | Unit | Aggregation |
|---|---|---|
| GDP, current prices | USD billions | sum |
| GDP growth | annual % change | average |
| Inflation, end of period CPI | % change | average |
| Unemployment | % of labour force | average |
| General government gross debt | % of GDP | average |
| Current account balance | % of GDP | average |
| GDP per capita, current prices | USD | average |
| Output gap | % of potential GDP | average |

Sums are used for stock metrics that aggregate meaningfully across
countries; averages are used for rates.

## Geographic representation

The 26 retained countries fall into three World Bank regions:

- Europe and Central Asia
- East Asia and Pacific
- North America

All 26 are classified as High income. This skew is a known consequence of
the completeness rule: high-income economies maintain consistent reporting
through the 2008 to 2010 financial crisis whereas many emerging and fragile
economies do not.

## Validation

`scripts/validate_data.py` re-applies the rule above on every CI run and
asserts the country count, observation count, year span, and absence of
nulls in primary key columns. Any drift between the README and the data
fails CI.
