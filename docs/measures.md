# Key DAX Measures

The dashboard exposes nine measures: eight indicator measures plus a
parameter-driven selector.

## Convention

Stock metrics (GDP, GDP per capita) use `SUM` because they aggregate
meaningfully across countries. Rate metrics (growth, inflation,
unemployment, debt %, current account %, output gap) use `AVERAGE` because
summing rates is meaningless.

## 1. GDP Current USD

```DAX
GDP Current USD =
    SUM ( IMF_Complete[GDP_Current_USD] )
```
Format: currency, 0 decimals.

## 2. GDP Growth %

```DAX
GDP Growth Pct =
    AVERAGE ( IMF_Complete[GDP_Growth_Pct] )
```
Format: percentage, 1 decimal.

## 3. Inflation %

```DAX
Inflation Pct =
    AVERAGE ( IMF_Complete[Inflation_Pct] )
```
Format: percentage, 1 decimal.

## 4. Unemployment %

```DAX
Unemployment Pct =
    AVERAGE ( IMF_Complete[Unemployment_Pct] )
```
Format: percentage, 1 decimal.

## 5. Government Gross Debt % of GDP

```DAX
Gov Gross Debt Pct GDP =
    AVERAGE ( IMF_Complete[Gov_Gross_Debt_Pct_GDP] )
```

## 6. Current Account % of GDP

```DAX
Current Account Pct GDP =
    AVERAGE ( IMF_Complete[Current_Account_Pct_GDP] )
```

## 7. GDP per Capita USD

```DAX
GDP Per Capita USD =
    AVERAGE ( IMF_Complete[GDP_Per_Capita_USD] )
```
Format: currency, displayed in thousands.

## 8. Output Gap %

```DAX
Output Gap Pct =
    AVERAGE ( IMF_Complete[Output_Gap_Pct] )
```

## 9. Selected Metric Value

The dynamic measure that backs the `Metric Selector` field parameter and
drives the trend line / top-10 bar chart from a single dropdown.

```DAX
Selected Metric Value =
    VAR Pick = SELECTEDVALUE ( 'Metric Selector'[Metric Order] )
    RETURN
        SWITCH (
            Pick,
            1, [GDP Current USD],
            2, [GDP Growth Pct],
            3, [Inflation Pct],
            4, [Unemployment Pct],
            5, [Gov Gross Debt Pct GDP],
            6, [Current Account Pct GDP],
            7, [GDP Per Capita USD],
            8, [Output Gap Pct],
            [GDP Current USD]   /* fallback */
        )
```

This pattern collapses what would otherwise be eight near-duplicate visuals
into a single configurable one.
