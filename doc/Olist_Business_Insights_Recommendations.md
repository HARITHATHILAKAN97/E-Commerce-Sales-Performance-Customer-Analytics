# Olist E-Commerce Analytics — Business Insights & Recommendations

## 1. Executive Summary

This project analyzes Olist e-commerce data using **Python, SQL, statistical analysis, and Power BI** to understand sales performance, customer behavior, product/category performance, seller performance, delivery, and customer satisfaction.

The main business lesson is that sales performance should not be viewed alone. **Revenue, order volume, customer behavior, seller quality, delivery performance, and reviews are connected.**

The analysis was therefore used to identify practical areas where the business can protect revenue, improve customer experience, and support sustainable growth.

---

## 2. Key Business Findings

### 2.1 Sales and Order Performance

Python and SQL analysis focused on:

- Total orders
- Total sales/order value
- Average Order Value (AOV)
- Monthly and yearly trends
- Category contribution
- Geographic contribution

**Finding:** Revenue should be understood through both **order volume and AOV**. An increase in revenue can come from more orders, higher-value orders, or both.

**Business meaning:** Management should not judge growth using revenue alone.

**Recommendation:**
- Track Revenue, Orders, and AOV together every month.
- Identify whether growth is volume-driven or value-driven.
- Investigate periods where orders increase but AOV falls.
- Focus on increasing basket size through cross-selling and relevant product recommendations.

---

### 2.2 Customer Performance

The analysis examined customer counts, order behavior, customer geography, and purchasing patterns.

**Finding:** Customer acquisition and customer retention are different business problems. A large customer base does not automatically mean strong long-term customer value.

**Recommendation:**
- Separate one-time and repeat customers.
- Identify high-value customers.
- Create post-purchase campaigns for one-time customers.
- Recommend related products to encourage a second purchase.
- Track repeat purchase rate and orders per customer.

**Priority KPI:** Repeat Customer %.

---

### 2.3 Product and Category Performance

Python, SQL, and Power BI were used to compare categories by order volume, sales, product price, freight, and customer experience.

**Finding:** The category with the highest order volume is not necessarily the category with the highest business value.

Categories should therefore be evaluated using:

**Sales + Orders + Average Price + Freight + Reviews + Delivery**

**Recommendation:**

- Protect high-volume/high-value categories.
- Identify high-volume but low-value categories and improve basket size.
- Investigate low-volume/high-value categories for targeted growth.
- Review weak categories before investing heavily in marketing.
- Use complementary-product recommendations to increase order value.

---

### 2.4 Seller Performance

SQL and Power BI analysis allow sellers to be compared by sales, order volume, reviews, and delivery performance.

**Finding:** Seller sales alone are not enough to measure seller quality. A high-sales seller with poor delivery or reviews can create a large customer-experience risk.

**Recommendation:**
Create a simple seller scorecard using:

- Sales
- Orders
- Average review score
- Late-delivery rate
- Customer impact

Classify sellers as:

- **Strategic:** high sales + strong service
- **Growth:** good service + room to grow
- **At Risk:** high sales + poor service
- **Low Contribution:** low sales + weak performance

**Action:** Prioritize high-sales, poor-performing sellers first because improvements there can affect more customers.

---

### 2.5 Delivery and Logistics

Delivery-related features were created during Python analysis and examined through SQL, statistics, and Power BI.

Important measures include:

- Delivery days
- Median delivery days
- Late-delivery rate
- Delivery performance by seller
- Delivery performance by region

**Finding:** Delivery is not only a logistics issue. It is part of the customer experience.

Long or unreliable delivery can contribute to poor customer feedback and can reduce confidence in the marketplace.

**Recommendation:**
- Identify sellers and regions with persistent delays.
- Separate seller handling delays from transportation delays.
- Prioritize high-volume problem areas.
- Create seller-level delivery targets.
- Monitor late deliveries weekly rather than waiting for monthly reporting.

**Priority KPIs:**
- On-time delivery %
- Average delivery days
- Median delivery days
- Late-delivery %

---

### 2.6 Delivery and Review Relationship

Statistical analysis can be used to examine the relationship between delivery performance and review scores.

**Finding:** If longer delivery times are associated with lower review scores, delivery should be treated as an important customer-experience driver.

The relationship should be interpreted as **association, not automatic proof of causation**, because reviews can also be influenced by product quality, seller service, and customer expectations.

**Recommendation:**
- Compare review scores for on-time and delayed orders.
- Identify seller/category/region combinations with both poor delivery and poor reviews.
- Prioritize these combinations for operational improvement.
- Measure whether review performance improves after delivery improvements.

---

### 2.7 Customer Reviews

Review scores were analyzed as an indicator of customer experience.

**Finding:** The average review score alone can hide specific problem areas. The proportion of low reviews is often more useful for identifying operational problems.

**Recommendation:**
- Monitor 1–2 star review rates.
- Analyze low reviews by seller, category, and region.
- Connect poor reviews with delivery performance.
- Use repeated low-review patterns to identify areas requiring investigation.

---

### 2.8 Geographic Performance

Customer and seller location data allow performance to be compared across regions.

**Finding:** A region with strong demand but weak delivery can represent both a problem and an opportunity.

**Recommendation:**

Use a simple regional decision framework:

| Situation | Recommended action |
|---|---|
| High demand + good delivery | Expand |
| High demand + poor delivery | Fix logistics first |
| Low demand + good delivery | Test targeted marketing |
| Low demand + poor delivery | Keep investment limited |

This prevents the business from spending heavily on demand generation where service capacity is weak.

---

### 2.9 Freight and Customer Cost

The analysis also considers product price and freight.

**Finding:** Customers experience the combined cost of the product and shipping, not product price alone.

A product with a low price can still become unattractive when freight is high.

**Recommendation:**
- Monitor freight-to-product-price ratio.
- Identify categories with unusually high freight burden.
- Investigate seller-region combinations with high shipping costs.
- Explore regional seller coverage and shipping optimization.
- Test sensible free-shipping thresholds where commercially viable.

---

## 3. Statistical Analysis — Business Value

Statistical analysis was used to understand the shape and variation of the data rather than relying only on totals.

Useful measures include:

- Mean
- Median
- Standard deviation
- Quartiles
- IQR
- Percentiles
- Correlation
- Outlier analysis

### Important findings

**Skewed transaction data:** A small number of high-value transactions can influence averages.

**Delivery variation:** Averages can hide a group of extremely delayed orders.

**Outliers:** High-value orders or unusually long deliveries should be investigated before being removed because they may represent genuine business cases or operational problems.

**Recommendation:**
Use **mean + median + percentiles** for important operational metrics instead of relying only on averages.

---

## 4. SQL Analysis — Business Value

SQL transformed the cleaned data into repeatable business analysis.

The most useful SQL analyses covered:

- Overall KPIs
- Monthly performance
- Category rankings
- Seller rankings
- State/geographic performance
- Customer/order analysis
- Delivery performance
- Review performance

**Business value:** SQL makes the analysis reproducible and allows management questions to be answered directly from the database rather than through manual calculations.

---

## 5. Python Analysis — Business Value

Python was mainly used to:

- Inspect and validate the datasets
- Clean the data
- Integrate related tables
- Engineer analytical features
- Explore distributions
- Analyze KPIs
- Identify patterns and anomalies

**Business value:** Python provided the analytical foundation and helped prepare reliable data for SQL, statistics, and Power BI.

---

# 6.  Recommendations

##  1 — Improve Delivery Reliability

**Action:**
1. Identify high-volume sellers with high late-delivery rates.
2. Identify regions with persistent delays.
3. Determine whether delays occur during seller handling or transportation.
4. Set improvement targets.
5. Review performance weekly.



---

##  2 — Manage Seller Quality

**Action:**
1. Build seller scorecards.
2. Combine sales with reviews and delivery.
3. Prioritize high-sales/poor-service sellers.
4. Create improvement plans.
5. Reward consistently strong sellers.

**Measure:** Seller review score, delivery performance, and sales.

---

## 3 — Increase Repeat Purchases

**Action:**
1. Identify one-time customers.
2. Launch second-purchase campaigns.
3. Recommend related products.
4. Segment high-value customers.
5. Track repeat purchasing.

**Measure:** Repeat Customer % and orders/customer.

---

##  4 — Optimize Categories

**Action:**
1. Rank categories by sales and orders.
2. Compare price, freight, delivery, and reviews.
3. Protect strong categories.
4. Improve weak but promising categories.
5. Use cross-selling to increase AOV.

**Measure:** Category sales, orders, AOV, and growth.

---

##  5 — Improve Regional Performance

**Action:**
1. Compare demand with delivery performance.
2. Identify high-demand/poor-delivery regions.
3. Improve seller coverage and logistics there.
4. Expand marketing only after service reliability improves.

**Measure:** Regional sales, orders, delivery rate, and review score.

---

##  6 — Monitor Customer Experience

**Action:**
1. Track low-review rates.
2. Connect poor reviews with delivery and seller performance.
3. Investigate repeated problem patterns.
4. Measure customer-experience improvement after corrective action.

**Measure:** Average review score and low-review %.

---


# 7. Final Business Story

The analysis shows that the marketplace should not focus on **sales growth alone**.

The strongest management approach is to connect:

**Sales → Customers → Products → Sellers → Delivery → Reviews**

A practical strategy is therefore:

1. **Protect revenue** by monitoring orders and AOV.
2. **Improve customer retention** by increasing repeat purchases.
3. **Improve seller quality** by combining sales with service performance.
4. **Fix delivery problems** in high-impact areas.
5. **Use reviews as an early warning signal.**
6. **Optimize categories and freight** using multiple KPIs.
7. **Prioritize regions based on both demand and service capability.**

The overall objective is to move from simply reporting business performance to **finding problems, understanding their likely drivers, prioritizing the highest-impact opportunities, and taking measurable action.**

---


