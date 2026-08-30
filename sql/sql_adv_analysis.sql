USE OlistAnalytics;
GO


/* =========================================================
   1. MONTHLY SALES VIEW
   Shows monthly orders and revenue
   ========================================================= */

CREATE VIEW vw_MonthlySales AS

SELECT
    YEAR(o.order_purchase_timestamp) AS OrderYear,
    MONTH(o.order_purchase_timestamp) AS OrderMonth,
    COUNT(DISTINCT o.order_id) AS TotalOrders,
    SUM(oi.price + oi.freight_value) AS Revenue
FROM dbo.orders o
JOIN dbo.order_items oi
    ON o.order_id = oi.order_id
GROUP BY
    YEAR(o.order_purchase_timestamp),
    MONTH(o.order_purchase_timestamp);
GO


/* =========================================================
   2. PRODUCT CATEGORY VIEW
   Shows category sales performance
   ========================================================= */

CREATE VIEW vw_CategoryPerformance AS

SELECT
    p.product_category_name AS Category,
    COUNT(*) AS ItemsSold,
    SUM(oi.price) AS Revenue
FROM dbo.order_items oi
JOIN dbo.products p
    ON oi.product_id = p.product_id
GROUP BY
    p.product_category_name;
GO


/* =========================================================
   3. SELLER PERFORMANCE VIEW
   Shows top seller performance
   ========================================================= */

CREATE VIEW vw_SellerPerformance AS

SELECT
    oi.seller_id,
    COUNT(DISTINCT oi.order_id) AS TotalOrders,
    SUM(oi.price) AS Revenue
FROM dbo.order_items oi
GROUP BY
    oi.seller_id;
GO


/* =========================================================
   4. STATE PERFORMANCE VIEW
   Shows sales by customer state
   ========================================================= */

CREATE VIEW vw_StatePerformance AS

SELECT
    c.customer_state AS State,
    COUNT(DISTINCT o.order_id) AS TotalOrders,
    SUM(oi.price + oi.freight_value) AS Revenue
FROM dbo.customers c
JOIN dbo.orders o
    ON c.customer_id = o.customer_id
JOIN dbo.order_items oi
    ON o.order_id = oi.order_id
GROUP BY
    c.customer_state;
GO


/* =========================================================
   5. PAYMENT PERFORMANCE VIEW
   Shows payment method performance
   ========================================================= */

CREATE VIEW vw_PaymentPerformance AS

SELECT
    payment_type,
    COUNT(*) AS NumberOfPayments,
    SUM(payment_value) AS TotalPaymentValue,
    AVG(payment_value) AS AveragePayment
FROM dbo.payments
GROUP BY
    payment_type;
GO


/* =========================================================
   6. DELIVERY PERFORMANCE VIEW
   Shows on-time and late deliveries
   ========================================================= */

CREATE VIEW vw_DeliveryPerformance AS

SELECT
    CASE
        WHEN order_delivered_customer_date >
             order_estimated_delivery_date
        THEN 'Late'
        ELSE 'On Time'
    END AS DeliveryStatus,
    COUNT(*) AS NumberOfOrders
FROM dbo.orders
WHERE order_delivered_customer_date IS NOT NULL
GROUP BY
    CASE
        WHEN order_delivered_customer_date >
             order_estimated_delivery_date
        THEN 'Late'
        ELSE 'On Time'
    END;
GO


/* =========================================================
   7. REVIEW PERFORMANCE VIEW
   Shows customer review distribution
   ========================================================= */

CREATE VIEW vw_ReviewPerformance AS

SELECT
    review_score,
    COUNT(*) AS NumberOfReviews
FROM dbo.reviews
GROUP BY
    review_score;
GO


/* =========================================================
   CHECK ALL VIEWS
   ========================================================= */

SELECT * FROM vw_MonthlySales;

SELECT * FROM vw_CategoryPerformance;

SELECT * FROM vw_SellerPerformance;

SELECT * FROM vw_StatePerformance;

SELECT * FROM vw_PaymentPerformance;

SELECT * FROM vw_DeliveryPerformance;

SELECT * FROM vw_ReviewPerformance;
GO