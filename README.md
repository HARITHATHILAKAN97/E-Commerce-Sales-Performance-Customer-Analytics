
# E-Commerce Sales Performance & Customer Analytics

End-to-end analytics project on the **Olist Brazilian E-Commerce public dataset** — Python data validation & cleaning, a normalized SQL Server data model with reusable business views, statistical analysis, and a 3-page interactive Power BI dashboard, translated into concrete business recommendations.

🔗 Repo: [E-Commerce-Sales-Performance-Customer-Analytics](https://github.com/HARITHATHILAKAN97/E-Commerce-Sales-Performance-Customer-Analytics)

---

## 📌 Project Overview

Olist is a Brazilian e-commerce marketplace connecting small businesses to major online sales channels. This project uses Olist's public dataset to answer one central business case:

> **How can Olist improve sustainable marketplace growth by understanding its revenue drivers, customer value, operational performance, and customer experience?**

**Key questions answered:**
- What are total sales, orders, and average order value — and how are they trending?
- Which categories, sellers, and states drive the most revenue?
- How many customers are repeat buyers, and who are the highest-value customers?
- What is the average delivery time, what share of orders arrive late, and does that relate to review scores?
- Which payment methods dominate, and how much does freight cost customers relative to product price?

**Headline finding:** revenue is concentrated in a handful of states (top 5 states = 73% of revenue) and product categories, the repeat customer rate is critically low (3.01%), and delivery time shows a clear negative relationship with review scores — meaning logistics performance is shaping customer satisfaction directly, not just operational cost.

---

## 🧰 Tech Stack

| Layer | Tools |
|---|---|
| Data validation & cleaning | Python (pandas) |
| Data model & business analysis | SQL Server (T-SQL), reusable views |
| Statistical analysis | Python (descriptive stats, correlation, outlier analysis) |
| Dashboard & reporting | Power BI, DAX |
| Schema design | dbdiagram.io (ERD) |
| Final deliverables | Word (.docx), Markdown (.md) |

---

## 📁 Project Structure

```
├── raw_data/
│   └── olist_*.csv                          # 9 source tables (customers, orders, order_items,
│                                             #   order_payments, order_reviews, products, sellers,
│                                             #   geolocation, product_category_name_translation)
│
├── scripts/
│   ├── 01_data_validation.py                 # Structural, type, missing-value, duplicate & rule checks
│   ├── 02_data_cleaning.py                    # Timestamp casting, dedup, category/key fixes
│   └── 03_feature_engineering.py              # Delivery days, late-delivery flag, repeat-customer flag
│
├── sql/
│   ├── table_creation_sql.sql                 # Schema: customers, orders, order_items, products,
│   │                                           #   sellers, payments, reviews (PK/FK enforced)
│   ├── sql_analysis.sql                       # Core business queries (e.g. state-level revenue)
│   └── sql_adv_analysis.sql                   # 7 reusable analytical views (see below)
│
├── docs/
│   ├── Bussiness_understanding.md             # Business problem, objectives, KPIs, scope
│   ├── Data_Validation.md                     # Full data-quality & validation report
│   └── Olist_Business_Insights_Recommendations.md
│
├── outputs/
│   ├── erd_diagram.png                        # Entity relationship diagram (dbdiagram.io)
│   └── dashboard.pdf                          # 3-page Power BI dashboard export
│
└── reports/
    ├── Olist_Ecommerce_Sales_Performance_Customer_Analytics_Project_Report.docx
    └── README.md
```

> File names reflect the logical project layout; some working files may carry upload-timestamp prefixes.

---

## 🗄️ Data Model

The dataset is fully relational across **9 tables** (~1.52M total rows), spanning **2016-09-04 to 2018-10-17**.

| # | Table | Rows | Grain |
|---|---|---|---|
| 1 | customers | 99,441 | 1 row / customer-order |
| 2 | geolocation | 1,000,163 | Multiple rows / zip prefix |
| 3 | order_items | 112,650 | 1 row / order item |
| 4 | order_payments | 103,886 | 1+ rows / order |
| 5 | order_reviews | 99,224 | 1 row / review |
| 6 | orders | 99,441 | 1 row / order |
| 7 | products | 32,951 | 1 row / product |
| 8 | sellers | 3,095 | 1 row / seller |
| 9 | product_category_name_translation | 71 | 1 row / category |

**Relationships:** `customers → orders → order_items → products / sellers`, with `order_payments` and `order_reviews` attached at the order level, and `geolocation` linked via zip code prefix.

See [`outputs/erd_diagram.png`](outputs/erd_diagram.png) for the full entity relationship diagram.

---

## ✅ Data Validation Summary

All 9 tables were validated for structure, types, missing values, duplicates, referential integrity, and business rules before analysis. Full detail in [`docs/Data_Validation.md`](docs/Data_Validation.md).

| Check | Result |
|---|---|
| Structural integrity (columns, headers, delimiters) | Pass |
| Primary key integrity | 8 / 9 Pass (`order_reviews` needs a surrogate key — 814 duplicate `review_id`s) |
| Foreign key integrity | Pass (>99.7% across all relationships) |
| Largest data-quality issue | 261,831 duplicate rows in `geolocation` (26% of the table) |
| Timestamp columns | Stored as text — required `datetime` casting |
| Overall data quality | Good — usable after targeted cleaning |

**SQL readiness required:** (1) datetime casting on all timestamp columns, (2) `geolocation` deduplication, (3) a `review_id` surrogate key / dedup strategy, (4) resolving 13 unmatched product categories.

---

## 🔄 Workflow

```
Raw Olist Dataset (9 CSVs)
   ↓
Python: Structural / Type / Missing-Value / Duplicate / Business-Rule Validation
   ↓
Python: Cleaning (datetime casting, dedup, key fixes) → Feature Engineering
   ↓
SQL Server: Schema Creation (PK/FK enforced) → 7 Analytical Views
   ↓
Statistical Analysis (descriptive stats, correlation, outlier analysis)
   ↓
Power BI: Data Model → DAX Measures → 3-Page Dashboard
   ↓
Business Insights → Prioritized Recommendations
```

---

## 🧮 SQL Views

Seven reusable views were built directly on the relational schema so any recurring business question can be answered without rewriting logic:

| View | Purpose |
|---|---|
| `vw_MonthlySales` | Monthly order count and revenue trend |
| `vw_CategoryPerformance` | Items sold and revenue by product category |
| `vw_SellerPerformance` | Orders and revenue by seller |
| `vw_StatePerformance` | Orders and revenue by customer state |
| `vw_PaymentPerformance` | Payment count, total value, and average by payment type |
| `vw_DeliveryPerformance` | On-time vs. late delivery order counts |
| `vw_ReviewPerformance` | Distribution of review scores (1–5) |

---

## ▶️ How to Run

### 1. Validate & clean the data
```bash
pip install pandas numpy
python scripts/01_data_validation.py
python scripts/02_data_cleaning.py
python scripts/03_feature_engineering.py
```

### 2. Load into SQL Server
```sql
-- In SQL Server Management Studio / Azure Data Studio:
:r sql/table_creation_sql.sql      -- Create schema (PK/FK enforced)
-- Bulk-load the cleaned CSVs into the created tables, then:
:r sql/sql_adv_analysis.sql        -- Create the 7 analytical views
:r sql/sql_analysis.sql            -- Run core business queries
```

### 3. Open the dashboard
Open the Power BI file in Power BI Desktop and point the data source at your SQL Server database (or the cleaned CSVs). `outputs/dashboard.pdf` is a static 3-page export for quick reference.

---

## 🔑 Key Findings

- **Scale:** ~99K customers, ~99K orders, R$15.84M total revenue, R$159.33 average order value.
- **Geographic concentration:** the top 5 states generate 73.2% of revenue; São Paulo alone accounts for 37.4%.
- **Retention gap:** repeat customer rate is just 3.01% — roughly 97 of every 100 customers never return for a second order.
- **Category mismatch:** the categories that drive the most revenue (`beleza_saude`, `relogios_presentes`) are not the same categories with the highest repeat-purchase rate (`cama_mesa_banho`, `moveis_decoracao`).
- **Delivery ↔ reviews:** average delivery time improved from 50+ days (2016) to ~10–15 days (2018); orders with longer delivery times show a visibly lower average review score.
- **Late-delivery concentration:** SP, RJ, and MG — the top revenue states — also account for the majority of late-delivery volume, giving delivery problems there outsized customer-experience impact.
- **Payment concentration:** credit card dominates payment value (R$13M) over boleto (R$3M) and all other methods combined.

Full findings, dashboard walkthrough, and the complete recommendation set are in:
- [`docs/Olist_Business_Insights_Recommendations.md`](docs/Olist_Business_Insights_Recommendations.md) — narrative insights & recommendations
- [`reports/Olist_Ecommerce_Sales_Performance_Customer_Analytics_Project_Report.docx`](reports/Olist_Ecommerce_Sales_Performance_Customer_Analytics_Project_Report.docx) — full 11-section project report (Word), including the ERD and dashboard screenshots

---

## ✅ Recommendations Summary

| Priority | Focus Area | Primary KPI | Action |
|---|---|---|---|
| 1 — Highest urgency | Delivery in SP / RJ / MG | Late delivery %, avg. delivery days | Root-cause delays; move to weekly monitoring |
| 2 — Protect experience | Seller quality | Review score, late-delivery rate | Seller scorecard; prioritize at-risk, high-sales sellers |
| 3 — Fix the leak | Customer retention | Repeat customer % | Second-purchase campaigns, loyalty incentives |
| 4 — Grow value | Category portfolio | Category sales, AOV | Cross-sell on strong categories, revive weak ones |
| 5 — Prioritize expansion | Regional investment | Demand vs. delivery rate | Apply demand/delivery decision framework before spend |
| 6 — Early warning system | Review monitoring | Low-review % (1–2 star) | Track and investigate patterns by seller/region |

**Regional investment framework:**

| Situation | Recommended Action |
|---|---|
| High demand + good delivery | Expand |
| High demand + poor delivery | Fix logistics first |
| Low demand + good delivery | Test targeted marketing |
| Low demand + poor delivery | Keep investment limited |

---

## ⚠️ Limitations

- Correlation is not causation — the delivery-time / review-score relationship is a strong association, not proof that delivery alone drives reviews.
- True profit cannot be calculated; the public dataset has no complete cost structure, so findings are revenue-based, not margin-based.
- The apparent revenue decline near the end of the dataset (late 2018) most likely reflects the dataset's cut-off date, not genuine business decline.
- Minor residual data-quality issues remain after cleaning (13 unmatched product categories, some `review_id` duplicates, ~0.3% unmatched geolocation zip prefixes).
- Findings reflect a historical window (Sept 2016 – Oct 2018) and may not directly generalize to current marketplace conditions.

---

## 📄 License / Usage

Educational / portfolio analytics project. Built on the publicly available Olist Brazilian E-Commerce dataset.
