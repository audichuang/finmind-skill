***

name: finmind
description: |
FinMind Taiwan historical financial data & analytics API. Use for: querying historical stock prices (daily/weekly/monthly/tick/kbar), financial statements (EPS/revenue/balance sheet/cash flow), dividends, chip data (三大法人買賣超/融資融券/股權分散表/八大行庫/分點進出), valuation (PER/PBR/市值), derivatives (futures/options historical), and macro economics (景氣指標/恐懼貪婪指數). Returns pandas DataFrame.
NOT for: placing orders, real-time streaming quotes, account balance/margin queries, or any live trading operations — use the「shioaji」skill instead.
----------------------------------------------------------------------------------------------------------------------------------------------------

# FinMind Taiwan Financial Data API

FinMind is an open-source Python API for **Taiwan historical financial data** (fundamentals, prices, chip data, derivatives, macro). All methods return `pandas.DataFrame`.

**IMPORTANT:** FinMind provides historical/delayed data only. It is NOT a real-time trading system or live quote feed. Do not use for real-time price monitoring or automated trading.

## Quick Start

```python
from finmind_client import get_loader

dl = get_loader()  # auto token auth + load balancing

# Stock price
df = dl.taiwan_stock_daily(stock_id="2330", start_date="2024-01-01", end_date="2024-12-31")

# Financial statements (EPS, profit)
fs = dl.taiwan_stock_financial_statement(stock_id="2330", start_date="2024-01-01", end_date="2024-12-31")

# Monthly revenue
rev = dl.taiwan_stock_month_revenue(stock_id="2330", start_date="2024-01-01", end_date="2024-12-31")

# Dividend
div = dl.taiwan_stock_dividend(stock_id="2330", start_date="2024-01-01", end_date="2024-12-31")

# Institutional investors (三大法人)
inst = dl.taiwan_stock_institutional_investors(stock_id="2330", start_date="2024-01-01", end_date="2024-12-31")
```

## Authentication & Rate Limits

### Dependencies

```bash
pip install FinMind
```

### Architecture

`finmind_client.py` wraps FinMind SDK authentication. It reads tokens from `finmind_tokens.json` and automatically handles single-token auth or multi-token round-robin load balancing.

```
Your code  →  finmind_client.py (read tokens + load balance)  →  FinMind API
```

| File | Role |
|------|------|
| `finmind_tokens.json` | Stores API tokens (user-created, not in git) |
| `finmind_client.py` | Reads tokens, wraps DataLoader, handles load balancing |

### Token Config

Copy `finmind_tokens.json.example` to `finmind_tokens.json` and fill in real tokens:

```json
{
  "tokens": ["TOKEN_1", "TOKEN_2"]
}
```

| Status | Behavior |
|--------|----------|
| No config file | Anonymous ~600 req/hr |
| 1 token | Authenticated ~1,800 req/hr |
| N tokens | Round-robin N x 1,800 req/hr |

### Code Generation Rule (IMPORTANT)

**Always use `finmind_client.get_loader()` when generating FinMind code. Never use `DataLoader()` directly.**

```python
# CORRECT
from finmind_client import get_loader
dl = get_loader()

# WRONG — bypasses token management
from FinMind.data import DataLoader
dl = DataLoader()
```

On rate limit (HTTP 402), remind user to create `finmind_tokens.json` or add more tokens.

### Doppler Integration (Recommended)

Secrets are managed centrally via [Doppler](https://doppler.com). No local config files needed.

```bash
# 確認是否已登入
doppler me

# 如果未登入，執行登入（Mac 或 Ubuntu VM 都一樣，只需一次）
doppler login

# 執行程式（secrets 自動注入為環境變數）
doppler run -p finmind -c dev -- python my_script.py
```

Environment variables used:

* `FINMIND_TOKEN_1` — primary API token
* `FINMIND_TOKEN_2`, `FINMIND_TOKEN_3`, ... — additional tokens for load balancing

## Common Parameters

Most methods share: `stock_id` (str), `start_date` (str, "YYYY-MM-DD"), `end_date` (str), `timeout` (int, default 60), `stock_id_list` (List\[str] for batch), `use_async` (bool for large queries).

## Common Workflow: Stock Analysis

```
Analysis Checklist:
- [ ] Get stock info: taiwan_stock_info()
- [ ] Check price trend: taiwan_stock_daily()
- [ ] Review financials: taiwan_stock_financial_statement()
- [ ] Check valuation: taiwan_stock_per_pbr()
- [ ] Analyze chip data: taiwan_stock_institutional_investors()
- [ ] Review dividend history: taiwan_stock_dividend()
```

## Task Categories

### 1. Fundamentals 基本面

**Financial statements** — Use `taiwan_stock_financial_statement()`. Returns long-format data with `type` column containing: `EPS`, `Revenue`, `GrossProfit`, `OperatingIncome`, `IncomeAfterTaxes`, `IncomeBeforeTax`, `OperatingExpenses`.

```python
fs = dl.taiwan_stock_financial_statement(stock_id="2330", start_date="2024-01-01", end_date="2024-12-31")
# Pivot to wide format
pivot = fs.pivot_table(index="date", columns="type", values="value", aggfunc="first")
# Annual EPS
eps = fs[fs["type"] == "EPS"].groupby(fs["date"].str[:4])["value"].sum()
```

**Balance sheet** — `taiwan_stock_balance_sheet()`. Key types: `TotalAssets`, `TotalLiabilities`, `Equity`, `CurrentAssets`, `CashAndCashEquivalents`.

**Cash flow** — `taiwan_stock_cash_flows_statement()`. Key types: `OperatingCashFlow`, `InvestingCashFlow`, `FinancingCashFlow`.

**Monthly revenue** — `taiwan_stock_month_revenue()`. Columns: `date`, `stock_id`, `revenue`, `revenue_month`, `revenue_year`.

For detailed column definitions and analysis patterns, see [references/fundamentals.md](references/fundamentals.md).

### 2. Stock Price 股價

| Method | Description |
|--------|-------------|
| `taiwan_stock_daily()` | Daily OHLCV — `open`, `max`, `min`, `close`, `Trading_Volume` |
| `taiwan_stock_daily_adj()` | Adjusted prices (for backtesting) |
| `taiwan_stock_tick()` | Intraday tick — `deal_price`, `volume`, `Time`, `TickType` |
| `taiwan_stock_kbar()` | Minute K-bar — `Open`, `High`, `Low`, `Close`, `Volume` |
| `taiwan_stock_weekly()` | Weekly OHLCV |
| `taiwan_stock_monthly()` | Monthly OHLCV |
| `taiwan_stock_tick_snapshot()` | Real-time snapshot (accepts str or List\[str]) |

### 3. Dividend 股利

| Method | Description |
|--------|-------------|
| `taiwan_stock_dividend()` | Dividend policy — `CashEarningsDistribution`, `StockEarningsDistribution`, `CashExDividendTradingDate` |
| `taiwan_stock_dividend_result()` | Ex-dividend fill rate results |

### 4. Chip Data 籌碼面

| Method | Description |
|--------|-------------|
| `taiwan_stock_institutional_investors()` | Per-stock institutional buy/sell (三大法人個股) |
| `taiwan_stock_institutional_investors_total()` | Market-wide institutional totals |
| `taiwan_stock_margin_purchase_short_sale()` | Per-stock margin/short (個股融資融券) |
| `taiwan_stock_margin_purchase_short_sale_total()` | Market-wide margin totals |
| `taiwan_stock_shareholding()` | Foreign/institutional shareholding % |
| `taiwan_stock_holding_shares_per()` | Shareholder concentration (股權分散表) |
| `taiwan_stock_securities_lending()` | Securities lending |
| `taiwan_stock_government_bank_buy_sell()` | Government bank trades (八大行庫) |
| `taiwan_stock_trading_daily_report()` | Broker-level trades (分點進出) |

For full column definitions, see [references/chip\_data.md](references/chip_data.md).

### 5. Valuation 估值

| Method | Description |
|--------|-------------|
| `taiwan_stock_per_pbr()` | PER, PBR, dividend yield |
| `taiwan_stock_market_value()` | Market capitalization |
| `taiwan_stock_market_value_weight()` | Market cap weight in index |

### 6. Derivatives 衍生商品

Futures: `taiwan_futures_daily()`, `taiwan_futures_tick()`, `taiwan_futures_snapshot()`, `taiwan_futures_institutional_investors()`, `taiwan_futures_open_interest_large_traders()`.

Options: `taiwan_option_daily()`, `taiwan_option_tick()`, `taiwan_options_snapshot()`, `taiwan_option_institutional_investors()`, `taiwan_option_open_interest_large_traders()`.

Convertible bonds: `taiwan_stock_convertible_bond_daily()`, `taiwan_stock_convertible_bond_info()`.

For full derivatives reference, see [references/derivatives.md](references/derivatives.md).

### 7. Market Info 市場資訊

| Method | Description |
|--------|-------------|
| `taiwan_stock_info()` | All stock listing (code, name, industry) |
| `taiwan_stock_news()` | Stock-specific news |
| `taiwan_stock_trading_date()` | Trading calendar |
| `taiwan_stock_day_trading()` | Day trading statistics |
| `taiwan_stock_book_and_trade()` | Order book statistics |
| `taiwan_securities_trader_info()` | Broker info |
| `tse()` | Full market data for a date |

### 8. Macro 總體經濟

```python
dl.us_stock_price(stock_id="AAPL", start_date="2024-01-01")
dl.cnn_fear_greed_index(start_date="2024-01-01")
dl.taiwan_business_indicator(start_date="2024-01-01")
```

## Common Issues

* **Empty DataFrame**: Stock may be delisted or date range has no data. Verify stock\_id with `taiwan_stock_info()`.
* **Rate limit error (HTTP 402)**: Add `time.sleep(0.5)` between calls, use `dl.login_by_token()`, or use multi-token pool.
* **`stock_id` vs `futures_id`**: Futures methods use `futures_id` (e.g., `"TX"`), not `stock_id`.
* **Long-format data**: Financial statements return one row per metric. Use `pivot_table()` to convert to wide format.

## Out of Scope 不在本 Skill 範圍

The following are **NOT** available in FinMind:
以下功能 FinMind **不提供**：

* Placing, modifying, or canceling orders (下單/改單/刪單)
* Real-time streaming tick/bidask quotes (即時逐筆/五檔串流行情)
* Account balance, margin, or position queries (帳戶餘額/保證金/持倉查詢)
* CA certificate management (憑證管理)
* Automated trade execution (自動交易執行)

**Use the `shioaji` skill for these tasks.**
**請使用 `shioaji` skill 進行以上操作。**

***

## References

* **Fundamentals details**: [references/fundamentals.md](references/fundamentals.md) — column definitions, analysis patterns, pivot examples
* **Chip data details**: [references/chip\_data.md](references/chip_data.md) — institutional, margin, shareholding columns
* **Derivatives details**: [references/derivatives.md](references/derivatives.md) — futures/options methods and columns
