USE OlistAnalytics;
GO


-- ============================================================
-- 1. CUSTOMERS
-- ============================================================

CREATE TABLE customers
(
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state VARCHAR(10)
);
GO


-- ============================================================
-- 2. ORDERS
-- ============================================================

CREATE TABLE orders
(
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_status VARCHAR(30),
    order_purchase_timestamp DATETIME,
    order_approved_at DATETIME,
    order_delivered_carrier_date DATETIME,
    order_delivered_customer_date DATETIME,
    order_estimated_delivery_date DATETIME
);
GO


-- ============================================================
-- 3. ORDER ITEMS
-- ============================================================

CREATE TABLE order_items
(
    order_id VARCHAR(50),
    order_item_id INT,
    product_id VARCHAR(50),
    seller_id VARCHAR(50),
    shipping_limit_date DATETIME,
    price DECIMAL(10,2),
    freight_value DECIMAL(10,2),

    PRIMARY KEY (order_id, order_item_id)
);
GO


-- ============================================================
-- 4. PRODUCTS
-- ============================================================

CREATE TABLE products
(
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_weight_g DECIMAL(10,2),
    product_length_cm DECIMAL(10,2),
    product_height_cm DECIMAL(10,2),
    product_width_cm DECIMAL(10,2)
);
GO


-- ============================================================
-- 5. SELLERS
-- ============================================================

CREATE TABLE sellers
(
    seller_id VARCHAR(50) PRIMARY KEY,
    seller_zip_code_prefix INT,
    seller_city VARCHAR(100),
    seller_state VARCHAR(10)
);
GO


-- ============================================================
-- 6. PAYMENTS
-- ============================================================

CREATE TABLE payments
(
    order_id VARCHAR(50),
    payment_sequential INT,
    payment_type VARCHAR(30),
    payment_installments INT,
    payment_value DECIMAL(10,2)
);
GO


-- ============================================================
-- 7. REVIEWS
-- ============================================================

CREATE TABLE reviews
(
    review_id VARCHAR(50),
    order_id VARCHAR(50),
    review_score INT,
    review_comment_title VARCHAR(500),
    review_comment_message VARCHAR(MAX),
    review_creation_date DATETIME,
    review_answer_timestamp DATETIME
);
GO