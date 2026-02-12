# Fundamentals Reference 基本面參考

## Contents
- Financial Statement 綜合損益表
- Balance Sheet 資產負債表
- Cash Flow Statement 現金流量表
- Monthly Revenue 月營收
- Dividend 股利
- PER / PBR 本益比 / 股價淨值比

## Financial Statement 綜合損益表

`dl.taiwan_stock_financial_statement()` returns long-format data. Each row is one metric for one quarter.

### Columns

| Column | Description |
|--------|-------------|
| `date` | Quarter end date (e.g., `2024-03-31`) |
| `stock_id` | Stock code |
| `type` | Metric name (English key) |
| `value` | Metric value |
| `origin_name` | Original Chinese name |

### All `type` Values

| type | 中文 | Description |
|------|------|-------------|
| `Revenue` | 營業收入 | Total revenue |
| `CostOfGoodsSold` | 營業成本 | Cost of goods sold |
| `GrossProfit` | 毛利 | Gross profit |
| `OperatingExpenses` | 營業費用 | Operating expenses |
| `OperatingIncome` | 營業利益 | Operating income |
| `IncomeBeforeTax` | 稅前淨利 | Pre-tax income |
| `IncomeAfterTaxes` | 稅後淨利 | Net income |
| `EPS` | 每股盈餘 | Earnings per share |
| `OperatingExpenseRate` | 營業費用率 | OpEx ratio |

### Analysis Patterns

#### Pivot to Wide Format

```python
fs = dl.taiwan_stock_financial_statement(stock_id="2330", start_date="2024-01-01", end_date="2024-12-31")
pivot = fs.pivot_table(index="date", columns="type", values="value", aggfunc="first")
print(pivot[["EPS", "Revenue", "GrossProfit", "OperatingIncome", "IncomeAfterTaxes"]])
```

#### Annual EPS

```python
eps_df = fs[fs["type"] == "EPS"]
annual = eps_df.groupby(eps_df["date"].str[:4])["value"].sum()
```

#### Gross Margin Trend

```python
pivot["GrossMargin%"] = pivot["GrossProfit"] / pivot["Revenue"] * 100
pivot["OperatingMargin%"] = pivot["OperatingIncome"] / pivot["Revenue"] * 100
pivot["NetMargin%"] = pivot["IncomeAfterTaxes"] / pivot["Revenue"] * 100
```

#### Cross-Company EPS Comparison

```python
all_fs = dl.taiwan_stock_financial_statement(
    stock_id_list=["2330", "2317", "2454"],
    start_date="2024-01-01", end_date="2024-12-31"
)
eps_compare = all_fs[all_fs["type"] == "EPS"].pivot_table(
    index="date", columns="stock_id", values="value"
)
```

---

## Balance Sheet 資產負債表

`dl.taiwan_stock_balance_sheet()` — same long format as financial statements.

### Key `type` Values

| type | 中文 |
|------|------|
| `TotalAssets` | 資產總計 |
| `TotalLiabilities` | 負債總計 |
| `Equity` | 股東權益 |
| `CurrentAssets` | 流動資產 |
| `CurrentLiabilities` | 流動負債 |
| `CashAndCashEquivalents` | 現金及約當現金 |
| `RetainedEarnings` | 保留盈餘 |
| `Inventories` | 存貨 |
| `AccountsReceivable` | 應收帳款 |

### Debt Ratio

```python
bs = dl.taiwan_stock_balance_sheet(stock_id="2330", start_date="2024-01-01", end_date="2024-12-31")
pivot = bs.pivot_table(index="date", columns="type", values="value", aggfunc="first")
pivot["DebtRatio%"] = pivot["TotalLiabilities"] / pivot["TotalAssets"] * 100
pivot["CurrentRatio"] = pivot["CurrentAssets"] / pivot["CurrentLiabilities"]
```

---

## Cash Flow Statement 現金流量表

`dl.taiwan_stock_cash_flows_statement()` — same long format.

### Key `type` Values

| type | 中文 |
|------|------|
| `OperatingCashFlow` | 營業活動現金流量 |
| `InvestingCashFlow` | 投資活動現金流量 |
| `FinancingCashFlow` | 籌資活動現金流量 |
| `FreeCashFlow` | 自由現金流量 |
| `DepreciationExpense` | 折舊費用 |

### Free Cash Flow

```python
cf = dl.taiwan_stock_cash_flows_statement(stock_id="2330", start_date="2024-01-01", end_date="2024-12-31")
pivot = cf.pivot_table(index="date", columns="type", values="value", aggfunc="first")
pivot["FCF"] = pivot["OperatingCashFlow"] + pivot["InvestingCashFlow"]
```

---

## Monthly Revenue 月營收

`dl.taiwan_stock_month_revenue()` — one row per month.

### Columns

| Column | Description |
|--------|-------------|
| `date` | Report date |
| `stock_id` | Stock code |
| `revenue` | Monthly revenue in TWD |
| `revenue_month` | Revenue month (1-12) |
| `revenue_year` | Revenue year |

### YoY / MoM Growth

```python
rev = dl.taiwan_stock_month_revenue(stock_id="2330", start_date="2023-01-01", end_date="2025-01-01")
rev["YoY%"] = rev["revenue"].pct_change(periods=12) * 100
rev["MoM%"] = rev["revenue"].pct_change(periods=1) * 100
```

---

## Dividend 股利

`dl.taiwan_stock_dividend()` — dividend policy per period.

### Key Columns

| Column | Description |
|--------|-------------|
| `date` | Record date |
| `stock_id` | Stock code |
| `year` | Fiscal year/period (民國年) |
| `CashEarningsDistribution` | Cash dividend per share 現金股利 |
| `StockEarningsDistribution` | Stock dividend per share 股票股利 |
| `CashExDividendTradingDate` | Ex-dividend date 除息日 |
| `CashDividendPaymentDate` | Payment date 發放日 |

### Annual Dividend Yield

```python
div = dl.taiwan_stock_dividend(stock_id="2330", start_date="2024-01-01", end_date="2025-12-31")
annual_cash = div["CashEarningsDistribution"].sum()
# Compare with current price for yield
```

---

## PER / PBR 本益比 / 股價淨值比

`dl.taiwan_stock_per_pbr()` — daily valuation metrics.

### Columns

| Column | Description |
|--------|-------------|
| `date` | Date |
| `stock_id` | Stock code |
| `PER` | Price-to-Earnings Ratio 本益比 |
| `PBR` | Price-to-Book Ratio 股價淨值比 |
| `dividend_yield` | Dividend yield % 殖利率 |

```python
val = dl.taiwan_stock_per_pbr(stock_id="2330", start_date="2024-01-01", end_date="2024-12-31")
print(f"PER range: {val['PER'].min():.1f} ~ {val['PER'].max():.1f}")
print(f"Average PBR: {val['PBR'].mean():.2f}")
```
