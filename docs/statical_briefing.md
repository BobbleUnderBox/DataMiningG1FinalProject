## 統計方法 Briefing

### Chi-Square（類別變數）
- 只有 `employment_type` 與 `default_flag` 達顯著（p < 0.05），Cramér’s V 約 0.20，屬小到中等關聯。
- Student、Unemployed 的違約比例較高；Salaried、Self-Employed 較低。
- `product_category`、`location`、`transaction_year_onehot`、`transaction_is_weekend` 皆不顯著，關聯接近 0。

### Ordinal 分布差異（視覺化後結論）
| 變數 | 分布差異 | 解讀 |
| --- | --- | --- |
| `customer_segment` | Very different | 違約組高度集中在 segment 2 |
| `transaction_month` | Similar | 兩組月份分布接近 |
| `transaction_day` | Similar | 兩組日期分布接近 |
| `transaction_dayofweek` | Similar | 兩組星期分布接近 |
| `bnpl_installments` | Similar | 兩組分期數分布接近 |
| `missed_payments` | Very different | 違約組 missed payments 明顯較高 |

### Mann-Whitney U（Ordinal/非正態連續）
- 顯著差異：`customer_segment`、`credit_score_log1p`、`repayment_delay_days_log1p`、`missed_payments`、`monthly_income_log1p`、`debt_to_income_ratio_log1p`、`purchase_amount_log1p`、`age_log1p`。
- 不顯著：`bnpl_installments`、`transaction_month`、`transaction_day`、`transaction_dayofweek`、`app_usage_frequency_log1p`。
- 解讀：非違約組的 `credit_score_log1p`、`monthly_income_log1p` 較高；違約組的 `repayment_delay_days_log1p`、`missed_payments`、`debt_to_income_ratio_log1p` 較高。`customer_segment` 與 `missed_payments` 雖中位數相同，但分布形狀差異明顯。

### Welch’s t-test（`risk_score`）
- 兩組平均數顯著不同（p < 0.05）。
- 非違約組平均約 -0.3197，違約組平均約 0.4989。
- Cohen’s d 約 -0.893，效果量大，表示 `risk_score` 對違約區分能力強。

### Spearman 相關（|ρ| > 0.75）
1. `credit_score_log1p` 與 `monthly_income_log1p`：強正相關  
2. `credit_score_log1p` 與 `risk_score`：強負相關  
3. `missed_payments` 與 `repayment_delay_days_log1p`：強正相關  
4. `monthly_income_log1p` 與 `debt_to_income_ratio_log1p`：強負相關  

結論：風險相關變數之間存在資訊重疊，後續建模需注意共線性與特徵冗餘。
