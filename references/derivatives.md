# Derivatives Reference 衍生商品參考

## Contents
- Futures 期貨 (Daily, Tick, Snapshot, Institutional, Large Traders)
- Options 選擇權 (Daily, Tick, Snapshot, Institutional, Large Traders)
- Convertible Bonds 可轉債
- Futures/Options Overview 期選總覽

## Futures 期貨

### Daily Price 日資料

`dl.taiwan_futures_daily(futures_id, start_date, end_date)`

| Column | Description |
|--------|-------------|
| `date` | Date |
| `futures_id` | Futures code (e.g., `TX` 台指期, `MTX` 小台指) |
| `contract_date` | Contract month 合約月份 |
| `open` | Open 開盤 |
| `max` | High 最高 |
| `min` | Low 最低 |
| `close` | Close 收盤 |
| `spread` | Change 漲跌 |
| `volume` | Volume 成交量 |
| `settlement_price` | Settlement price 結算價 |
| `open_interest` | Open interest 未平倉量 |

```python
df = dl.taiwan_futures_daily(futures_id="TX", start_date="2024-01-01", end_date="2024-12-31")
```

### Tick Data 逐筆成交

`dl.taiwan_futures_tick(futures_id, date)` — single date only.

```python
df = dl.taiwan_futures_tick(futures_id="TX", date="2024-12-20")
```

### Real-Time Snapshot 即時快照

`dl.taiwan_futures_snapshot(futures_id)` — current market snapshot.

### Institutional Investors 三大法人

`dl.taiwan_futures_institutional_investors(futures_id, start_date, end_date)`

| Column | Description |
|--------|-------------|
| `name` | Institution name (外資, 投信, 自營商) |
| `long_deal_volume` | Long volume 多方交易口數 |
| `long_deal_amount` | Long amount 多方交易金額 |
| `short_deal_volume` | Short volume 空方交易口數 |
| `short_deal_amount` | Short amount 空方交易金額 |
| `long_open_interest_balance_volume` | Long OI 多方未平倉口數 |
| `short_open_interest_balance_volume` | Short OI 空方未平倉口數 |

After-hours version: `dl.taiwan_futures_institutional_investors_after_hours()`

### Large Traders 大額交易人

`dl.taiwan_futures_open_interest_large_traders(futures_id, start_date, end_date)`

### Settlement Price 結算價

`dl.taiwan_futures_final_settlement_price(futures_id, start_date, end_date)`

### Common Futures Codes 常用期貨代碼

| Code | Name |
|------|------|
| `TX` | 台指期 Taiwan Index Futures |
| `MTX` | 小台指 Mini Taiwan Index |
| `TE` | 電子期 Electronics Futures |
| `TF` | 金融期 Finance Futures |
| `ZEF` | 台積電期貨 TSMC Futures |

---

## Options 選擇權

### Daily Price 日資料

`dl.taiwan_option_daily(option_id, start_date, end_date)`

| Column | Description |
|--------|-------------|
| `date` | Date |
| `option_id` | Options code (e.g., `TXO` 台指選) |
| `contract_date` | Contract month |
| `strike_price` | Strike price 履約價 |
| `call_put` | `call` or `put` |
| `open` | Open |
| `max` | High |
| `min` | Low |
| `close` | Close |
| `volume` | Volume |
| `open_interest` | Open interest |
| `settlement_price` | Settlement price |

```python
df = dl.taiwan_option_daily(option_id="TXO", start_date="2024-01-01", end_date="2024-12-31")
# Filter calls only
calls = df[df["call_put"] == "call"]
```

### Tick Data 逐筆成交

`dl.taiwan_option_tick(option_id, date)`

### Real-Time Snapshot 即時快照

`dl.taiwan_options_snapshot(options_id)`

### Institutional Investors 三大法人

`dl.taiwan_option_institutional_investors(option_id, start_date, end_date)`

Same columns as futures institutional investors.

After-hours: `dl.taiwan_option_institutional_investors_after_hours()`

### Large Traders 大額交易人

`dl.taiwan_option_open_interest_large_traders(option_id, start_date, end_date)`

### Common Options Codes 常用選擇權代碼

| Code | Name |
|------|------|
| `TXO` | 台指選擇權 Taiwan Index Options |

---

## Convertible Bonds 可轉債

### Bond Info 資訊

`dl.taiwan_stock_convertible_bond_info()` — no parameters, returns full listing.

### Daily Price 日資料

`dl.taiwan_stock_convertible_bond_daily(cb_id, start_date, end_date)`

### Institutional Investors 三大法人

`dl.taiwan_stock_convertible_bond_institutional_investors(cb_id, start_date, end_date)`

---

## Futures/Options Overview 期選總覽

| Method | Description |
|--------|-------------|
| `taiwan_futopt_daily_info()` | All contracts overview 所有合約總覽 |
| `taiwan_futopt_tick_info()` | Tick contract info 逐筆合約資訊 |
| `taiwan_futopt_tick_realtime(data_id)` | Real-time tick 即時逐筆 |
| `taiwan_futures_dealer_trading_volume_daily()` | Dealer futures volume 自營商期貨成交量 |
| `taiwan_option_dealer_trading_volume_daily()` | Dealer options volume 自營商選擇權成交量 |
