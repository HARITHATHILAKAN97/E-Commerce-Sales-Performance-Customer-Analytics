# Data Validation File
## Olist E-Commerce Dataset

---

## 1. Dataset Overview

| Item | Detail |
|---|---|
| Source | Olist Brazilian E-Commerce Public Dataset |
| Tables | 9 CSV files |
| Grain | Order / item / customer / product / seller / review / payment level (relational) |
| Time span | 2016-09-04 to 2018-10-17 |
| Total rows (all tables) | 1,521,321 |

---

## 2. Dataset / File Inventory

| # | File | Rows | Columns | Grain |
|---|---|---|---|---|
| 1 | olist_customers_dataset.csv | 99,441 | 5 | 1 row/customer-order |
| 2 | olist_geolocation_dataset.csv | 1,000,163 | 5 | Multi row/zip prefix |
| 3 | olist_order_items_dataset.csv | 112,650 | 7 | 1 row/order item |
| 4 | olist_order_payments_dataset.csv | 103,886 | 5 | 1+ row/order |
| 5 | olist_order_reviews_dataset.csv | 99,224 | 7 | 1 row/review |
| 6 | olist_orders_dataset.csv | 99,441 | 8 | 1 row/order |
| 7 | olist_products_dataset.csv | 32,951 | 9 | 1 row/product |
| 8 | olist_sellers_dataset.csv | 3,095 | 4 | 1 row/seller |
| 9 | product_category_name_translation.csv | 71 | 2 | 1 row/category |

---

## 3. Data Structure Validation

| Check | Result |
|---|---|
| Consistent column count per file | Pass |
| Header row present in all files | Pass |
| Encoding issues (BOM) | `product_category_name_translation.csv` header has BOM (`﻿`) — Minor |
| Delimiter consistency (comma) | Pass |
| Row count matches expected file size | Pass |

---

## 4. Data Type Validation

| Table | Column | Expected Type | Actual Type | Status |
|---|---|---|---|---|
| orders | order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date | datetime | object (string) | Needs conversion |
| order_items | shipping_limit_date | datetime | object (string) | Needs conversion |
| order_reviews | review_creation_date, review_answer_timestamp | datetime | object (string) | Needs conversion |
| order_items | price, freight_value | float | float | Pass |
| order_payments | payment_value | float | float | Pass |
| products | product_weight_g, dims | float | float | Pass |
| review_score | int (1–5) | int64 | Pass |
| All ID columns (order_id, customer_id, etc.) | string | object (string) | Pass |

---

## 5. Missing Value Validation

| Table | Column | Missing Count | Missing % |
|---|---|---|---|
| order_reviews | review_comment_title | 87,656 | 88.34% |
| order_reviews | review_comment_message | 58,247 | 58.70% |
| orders | order_delivered_customer_date | 2,965 | 2.98% |
| orders | order_delivered_carrier_date | 1,783 | 1.79% |
| products | product_category_name / name_length / desc_length / photos_qty | 610 | 1.85% |
| orders | order_approved_at | 160 | 0.16% |
| products | weight_g / length_cm / height_cm / width_cm | 2 | 0.01% |
| customers, geolocation, order_items, order_payments, sellers, category_translation | — | 0 | 0% |

---

## 6. Duplicate Record Validation

| Table | Duplicate Type | Count |
|---|---|---|
| geolocation | Full-row duplicates | 261,831 |
| order_reviews | Duplicate `review_id` | 1,603 rows (across 814 IDs) |
| order_reviews | Duplicate `order_id` (multiple reviews/order) | 1,098 rows |
| customers | Full-row duplicates | 0 |
| order_items | Full-row duplicates | 0 |
| order_payments | Full-row duplicates | 0 |
| orders | Full-row duplicates | 0 |
| products | Full-row duplicates | 0 |
| sellers | Full-row duplicates | 0 |

---

## 7. Primary Key, Foreign Key, Child Table Summary

| Table (Child) | Primary Key | Status | Foreign Key(s) | Parent Table | Referential Integrity |
|---|---|---|---|---|---|
| customers | customer_id | Unique — Pass | — | — | — |
| orders | order_id | Unique — Pass | customer_id | customers | 100% match |
| order_items | order_id + order_item_id | Unique (composite) — Pass | order_id | orders | 100% match |
| order_items | — | — | product_id | products | 100% match |
| order_items | — | — | seller_id | sellers | 100% match |
| order_payments | order_id + payment_sequential | Unique (composite) — Pass | order_id | orders | 100% match |
| order_reviews | review_id | Not unique — Fail (814 dup IDs) | order_id | orders | 100% match |
| products | product_id | Unique — Pass | product_category_name | category_translation | 13 unmatched categories |
| sellers | seller_id | Unique — Pass | — | — | — |
| geolocation | none (no natural PK) | N/A | zip_code_prefix | customers/sellers | 99.7% match both |

---

## 8. Relationship Validation

| Relationship | Expected Cardinality | Validated | Notes |
|---|---|---|---|
| customers → orders | 1 : M | Pass | 1 customer_id per order (unique per row) |
| orders → order_items | 1 : M | Pass | 775 orders have zero items |
| orders → order_payments | 1 : M | Pass | 1 order missing payment record |
| orders → order_reviews | 1 : M (expected 1:1) | Partial | 768 orders missing review; 1,098 orders have >1 review |
| order_items → products | M : 1 | Pass | Full match |
| order_items → sellers | M : 1 | Pass | Full match |
| products → category_translation | M : 1 | Partial | 13 products reference an untranslated category |
| customers/sellers → geolocation | M : 1 (via zip prefix) | Partial | ~0.3% zip prefixes unmatched |

---

## 9. Business Rule Validation

| Rule | Result |
|---|---|
| `price` > 0 | Pass (0 violations) |
| `freight_value` >= 0 | Pass (0 violations) |
| `payment_value` > 0 | Fail — 9 rows with value ≤ 0 |
| `payment_installments` >= 1 | Fail — 2 rows with 0 installments |
| `payment_type` in defined set | Pass, incl. `not_defined` category (3 rows) |
| `review_score` between 1–5 | Pass (0 violations) |
| `order_status` = delivered ⇒ delivered_customer_date not null | Fail — 8 rows violate |
| product weight/dimensions > 0 | Fail — 4 rows with 0 weight |
| `customer_state` / `seller_state` valid Brazilian UF codes | Pass (27 / 23 states) |

---

## 10. Date / Time Validation

| Check | Violations |
|---|---|
| `order_approved_at` >= `order_purchase_timestamp` | 0 |
| `order_delivered_carrier_date` >= `order_approved_at` | 1,359 |
| `order_delivered_customer_date` >= `order_delivered_carrier_date` | 23 |
| `order_delivered_customer_date` >= `order_purchase_timestamp` | 0 |
| Delivered after `order_estimated_delivery_date` (late orders) | 7,827 (7.87% of orders) |
| Date range sanity (2016-09 to 2018-10) | Pass |

---

## 11. Data Quality Issues Identified

| # | Issue | Table | Severity |
|---|---|---|---|
| 1 | Timestamp columns stored as text, not datetime | orders, order_items, order_reviews | Medium |
| 2 | High missing % in review comment fields | order_reviews | Low (expected — optional field) |
| 3 | 261,831 duplicate rows | geolocation | High |
| 4 | Duplicate review_id / order_id combinations | order_reviews | Medium |
| 5 | 775 orders with no line items (mostly canceled/unavailable) | orders / order_items | Low (expected by status) |
| 6 | 13 product categories missing from translation table | products | Medium |
| 7 | Carrier date earlier than approval date (sequence violation) | orders | Medium |
| 8 | 9 payments with value ≤ 0; 2 with 0 installments | order_payments | Low |
| 9 | 4 products with 0 weight/dimensions | products | Low |
| 10 | 8 "delivered" orders missing delivery date | orders | Medium |
| 11 | BOM character in category translation header | category_translation | Low |

---

## 12. Final Validation Summary

| Metric | Result |
|---|---|
| Tables validated | 9 / 9 |
| Structural integrity | Pass |
| Primary key integrity | 8/9 Pass (order_reviews fails on review_id uniqueness) |
| Foreign key integrity | Pass (>99.7% across all relationships) |
| Missing values | Present, mostly explainable/non-critical |
| Duplicates | Present — critical in geolocation |
| Business rule violations | Minor, low row-count (<20 rows per rule) |
| Date logic violations | Present — low volume, mostly in carrier/delivery sequencing |
| Overall data quality | Good — usable after targeted cleaning |

---

## 13. SQL Readiness Decision

| Criteria | Status |
|---|---|
| Unique/composite primary keys definable per table | Yes (review_id needs surrogate key) |
| Foreign key constraints enforceable | Yes, after minor cleanup (13 category, 1,603 review rows) |
| Data types SQL-compatible | Yes, after date column conversion |
| Duplicate rows removed | Required — geolocation to be deduplicated pre-load |
| **Decision** | **Ready for SQL load after: (1) datetime casting, (2) geolocation dedup, (3) review_id surrogate key/dedup strategy, (4) category translation gap fix** |
