# Chip Data Reference 籌碼面參考

## Contents
- Institutional Investors 三大法人
- Margin Trading 融資融券
- Foreign Shareholding 外資持股
- Shareholder Concentration 股權分散表
- Broker Trading 分點進出
- Securities Lending 借券
- Government Banks 八大行庫

## Institutional Investors 三大法人

### Per-Stock 個股三大法人

`dl.taiwan_stock_institutional_investors()`

| Column | Description |
|--------|-------------|
| `date` | Date |
| `stock_id` | Stock code |
| `name` | Institution name: `Foreign_Investor` (外資), `Investment_Trust` (投信), `Dealer_self` (自營商自行), `Dealer_Hedging` (自營商避險) |
| `buy` | Buy volume (shares) 買進股數 |
| `sell` | Sell volume (shares) 賣出股數 |

```python
inst = dl.taiwan_stock_institutional_investors(
    stock_id="2330", start_date="2024-01-01", end_date="2024-12-31"
)
# Net buy/sell per institution
inst["net"] = inst["buy"] - inst["sell"]
pivot = inst.pivot_table(index="date", columns="name", values="net", aggfunc="sum")
```

### Market-Wide Totals 三大法人總計

`dl.taiwan_stock_institutional_investors_total(start_date, end_date)` — no `stock_id` parameter.

---

## Margin Trading 融資融券

### Per-Stock 個股融資融券

`dl.taiwan_stock_margin_purchase_short_sale()`

| Column | Description |
|--------|-------------|
| `date` | Date |
| `stock_id` | Stock code |
| `MarginPurchaseBuy` | 融資買進 |
| `MarginPurchaseSell` | 融資賣出 |
| `MarginPurchaseCashRepayment` | 融資現金償還 |
| `MarginPurchaseYesterdayBalance` | 融資前日餘額 |
| `MarginPurchaseTodayBalance` | 融資今日餘額 |
| `ShortSaleBuy` | 融券買進 |
| `ShortSaleSell` | 融券賣出 |
| `ShortSaleCashRepayment` | 融券現券償還 |
| `ShortSaleYesterdayBalance` | 融券前日餘額 |
| `ShortSaleTodayBalance` | 融券今日餘額 |

```python
margin = dl.taiwan_stock_margin_purchase_short_sale(
    stock_id="2330", start_date="2024-01-01", end_date="2024-12-31"
)
# Margin balance trend
margin[["date", "MarginPurchaseTodayBalance", "ShortSaleTodayBalance"]]
```

### Market-Wide Totals 融資融券總計

`dl.taiwan_stock_margin_purchase_short_sale_total(start_date, end_date)`

---

## Foreign Shareholding 外資持股

`dl.taiwan_stock_shareholding()`

| Column | Description |
|--------|-------------|
| `date` | Date |
| `stock_id` | Stock code |
| `ForeignInvestmentRemainingShares` | Foreign holding shares 外資持有股數 |
| `ForeignInvestmentSharesRatio` | Foreign holding ratio % 外資持股比例 |
| `ForeignInvestmentUpperLimitRatio` | Foreign holding limit % 外資持股上限 |

```python
fh = dl.taiwan_stock_shareholding(
    stock_id="2330", start_date="2024-01-01", end_date="2024-12-31"
)
```

---

## Shareholder Concentration 股權分散表

`dl.taiwan_stock_holding_shares_per()` — weekly shareholder distribution by holding size bracket.

| Column | Description |
|--------|-------------|
| `date` | Date |
| `stock_id` | Stock code |
| `HoldingSharesLevel` | Bracket (e.g., "1-999", "1,000-5,000") |
| `people` | Number of shareholders 股東人數 |
| `unit` | Units held 持有單位數 |
| `percent` | Holding percentage % 持股比例 |

```python
conc = dl.taiwan_stock_holding_shares_per(
    stock_id="2330", start_date="2024-01-01", end_date="2024-12-31"
)
# Large holders (1000+ units)
large = conc[conc["HoldingSharesLevel"].str.contains("1,000")]
```

---

## Broker Trading 分點進出

`dl.taiwan_stock_trading_daily_report()` — broker-level buy/sell per stock.

| Column | Description |
|--------|-------------|
| `date` | Date |
| `stock_id` | Stock code |
| `securities_trader_id` | Broker branch ID 券商分點代號 |
| `buy` | Buy volume 買進量 |
| `sell` | Sell volume 賣出量 |
| `price` | Average price 均價 |

```python
broker = dl.taiwan_stock_trading_daily_report(
    stock_id="2330", date="2024-12-20"
)
# Top buyers
top_buy = broker.nlargest(10, "buy")
```

### Aggregated by Broker 依券商彙總

`dl.taiwan_stock_trading_daily_report_secid_agg()` — aggregated over date range.

---

## Securities Lending 借券

`dl.taiwan_stock_securities_lending()`

| Column | Description |
|--------|-------------|
| `date` | Date |
| `stock_id` | Stock code |
| `transaction_type` | Lending type 交易類型 |
| `volume` | Lending volume 借券量 |
| `fee_rate` | Lending fee rate 費率 |

---

## Government Banks 八大行庫

`dl.taiwan_stock_government_bank_buy_sell(start_date)` — market-wide, no per-stock filter.

| Column | Description |
|--------|-------------|
| `date` | Date |
| `stock_id` | Stock code |
| `buy` | Buy amount 買進金額 |
| `sell` | Sell amount 賣出金額 |
