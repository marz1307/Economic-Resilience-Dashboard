# Reading the Dashboard

The `.pbix` is the primary deliverable. The notes below help a reader
navigate the report when they open it in Power BI Desktop.

## Layout

A single-screen layout with five regions:

1. **Left rail.** Slicers for Year, Country, Region, Income group, and
   Metric Selector.
2. **Top centre.** Trend line, driven by the metric selector, covering
   2001 to 2020 with a five-year forecast overlay.
3. **Right rail.** Five KPI cards: GDP, GDP per Capita, GDP Growth,
   Inflation, Unemployment. Cards 3 to 5 use conditional colouring.
4. **Bottom centre.** Inflation vs Unemployment scatter, with bubble size
   = GDP and a play-axis on Year.
5. **Bottom right.** Top 10 countries bar chart, also driven by the metric
   selector.

## What to look for

The dashboard is descriptive, not causal. Suggested explorations for a
reader:

- Step the year slicer across the **2008 to 2010** window and watch the
  scatter plot. Most economies move up the unemployment axis with little
  inflation movement; a deflationary cluster appears in 2009.
- Switch the metric selector to **Government Gross Debt** and step through
  years to see the post-crisis fiscal expansion across most economies.
- Use the country slicer to isolate **Greece, Ireland, Portugal, Spain**
  and step through years to see the sovereign debt period.
- Switch the metric to **Output Gap** and observe the synchronised swing
  in 2020.

Specific point estimates have been deliberately omitted from this README.
The trend line, KPI cards, and bar chart all read directly off the Power
BI model, so the report itself is the source of truth.

## Limitations

- 26 advanced economies only. No emerging markets, no fragile states.
- Annual granularity. Within-year shocks are not visible.
- Correlations only. The scatter plot does not establish causation.
- No structural drivers (demographics, productivity, policy regime).
