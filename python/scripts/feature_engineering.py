# ============================================================
# OLIST E-COMMERCE PROJECT
# 02 - FEATURE ENGINEERING
# Beginner -> Intermediate
# ============================================================

import pandas as pd
from pathlib import Path


# ============================================================
# 1. FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CLEANED_DATA = BASE_DIR / "data" / "cleaned"
PROCESSED_DATA = BASE_DIR / "data" / "processed"

PROCESSED_DATA.mkdir(exist_ok=True)


# ============================================================
# 2. LOAD DATA
# ============================================================

def load_data():

    customers = pd.read_csv(
        CLEANED_DATA / "customers_clean.csv"
    )

    orders = pd.read_csv(
        CLEANED_DATA / "orders_clean.csv"
    )

    order_items = pd.read_csv(
        CLEANED_DATA / "order_items_clean.csv"
    )

    payments = pd.read_csv(
        CLEANED_DATA / "payments_clean.csv"
    )

    reviews = pd.read_csv(
        CLEANED_DATA / "reviews_clean.csv"
    )

    products = pd.read_csv(
        CLEANED_DATA / "products_clean.csv"
    )

    sellers = pd.read_csv(
        CLEANED_DATA / "sellers_clean.csv"
    )

    category_translation = pd.read_csv(
        CLEANED_DATA / "category_translation_clean.csv"
    )

    print("All datasets loaded.")

    return (
        customers,
        orders,
        order_items,
        payments,
        reviews,
        products,
        sellers,
        category_translation
    )


# ============================================================
# 3. CONVERT DATE COLUMNS
# ============================================================

def convert_dates(orders, reviews, order_items):

    order_dates = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for column in order_dates:

        orders[column] = pd.to_datetime(
            orders[column],
            errors="coerce"
        )

    review_dates = [
        "review_creation_date",
        "review_answer_timestamp"
    ]

    for column in review_dates:

        reviews[column] = pd.to_datetime(
            reviews[column],
            errors="coerce"
        )

    order_items["shipping_limit_date"] = pd.to_datetime(
        order_items["shipping_limit_date"],
        errors="coerce"
    )

    print("Date columns converted.")

    return orders, reviews, order_items


# ============================================================
# 4. ORDER DATE FEATURES
# ============================================================

def create_order_date_features(orders):

    orders["order_year"] = (
        orders["order_purchase_timestamp"].dt.year
    )

    orders["order_quarter"] = (
        orders["order_purchase_timestamp"].dt.quarter
    )

    orders["order_month"] = (
        orders["order_purchase_timestamp"].dt.month
    )

    orders["order_month_name"] = (
        orders["order_purchase_timestamp"].dt.month_name()
    )

    orders["order_day_name"] = (
        orders["order_purchase_timestamp"].dt.day_name()
    )

    print("Order date features created.")

    return orders


# ============================================================
# 5. DELIVERY FEATURES
# ============================================================

def create_delivery_features(orders):

    orders["delivery_days"] = (
        orders["order_delivered_customer_date"]
        - orders["order_purchase_timestamp"]
    ).dt.days

    orders["estimated_delivery_days"] = (
        orders["order_estimated_delivery_date"]
        - orders["order_purchase_timestamp"]
    ).dt.days

    orders["delivery_delay_days"] = (
        orders["order_delivered_customer_date"]
        - orders["order_estimated_delivery_date"]
    ).dt.days

    orders["late_delivery"] = (
        orders["delivery_delay_days"] > 0
    )

    print("Delivery features created.")

    return orders


# ============================================================
# 6. ORDER ITEM FEATURES
# ============================================================

def create_order_item_features(order_items):

    # Product price + freight
    order_items["item_total_value"] = (
        order_items["price"]
        + order_items["freight_value"]
    )

    # Freight as percentage of product price
    order_items["freight_percentage"] = (
        order_items["freight_value"]
        / order_items["price"]
        * 100
    )

    # Replace infinite values caused by price = 0
    order_items["freight_percentage"] = (
        order_items["freight_percentage"]
        .replace([float("inf"), -float("inf")], pd.NA)
    )

    print("Order item features created.")

    return order_items


# ============================================================
# 7. PAYMENT FEATURES
# ============================================================

def create_payment_features(payments):

    payments["installment_category"] = pd.cut(
        payments["payment_installments"],
        bins=[0, 1, 3, 6, float("inf")],
        labels=[
            "1 Installment",
            "2-3 Installments",
            "4-6 Installments",
            "7+ Installments"
        ]
    )

    print("Payment features created.")

    return payments


# ============================================================
# 8. REVIEW FEATURES
# ============================================================

def create_review_features(reviews):

    reviews["review_category"] = pd.cut(
        reviews["review_score"],
        bins=[0, 2, 3, 5],
        labels=[
            "Negative",
            "Neutral",
            "Positive"
        ]
    )

    reviews["review_response_days"] = (
        reviews["review_answer_timestamp"]
        - reviews["review_creation_date"]
    ).dt.days

    print("Review features created.")

    return reviews


# ============================================================
# 9. PRODUCT FEATURES
# ============================================================

def create_product_features(
    products,
    category_translation
):

    # Product volume
    products["product_volume_cm3"] = (
        products["product_length_cm"]
        * products["product_height_cm"]
        * products["product_width_cm"]
    )

    # Product size
    products["product_size"] = pd.qcut(
        products["product_volume_cm3"],
        3,
        labels=[
            "Small",
            "Medium",
            "Large"
        ],
        duplicates="drop"
    )

    # Product weight
    products["product_weight_category"] = pd.qcut(
        products["product_weight_g"],
        3,
        labels=[
            "Light",
            "Medium",
            "Heavy"
        ],
        duplicates="drop"
    )

    # Add English category
    products = products.merge(
        category_translation,
        on="product_category_name",
        how="left"
    )

    print("Product features created.")

    return products


# ============================================================
# 10. ORDER SALES SUMMARY
# ============================================================

def create_order_summary(order_items):

    order_summary = (
        order_items
        .groupby("order_id")
        .agg(
            total_product_value=("price", "sum"),

            total_freight=("freight_value", "sum"),

            total_order_value=(
                "item_total_value",
                "sum"
            ),

            number_of_items=(
                "order_item_id",
                "count"
            )
        )
        .reset_index()
    )

    print("Order summary created.")

    return order_summary


# ============================================================
# 11. CUSTOMER SUMMARY
# ============================================================

def create_customer_summary(
    orders,
    order_summary,
    customers
):

    # --------------------------------------------------------
    # Add order-level sales information
    # --------------------------------------------------------

    customer_orders = orders.merge(
        order_summary,
        on="order_id",
        how="left"
    )

    # --------------------------------------------------------
    # Add customer_unique_id
    #
    # orders contains customer_id
    # customers contains customer_id
    # and customer_unique_id
    # --------------------------------------------------------

    customer_orders = customer_orders.merge(
        customers[
            [
                "customer_id",
                "customer_unique_id"
            ]
        ],
        on="customer_id",
        how="left"
    )

    # --------------------------------------------------------
    # Create customer summary
    # --------------------------------------------------------

    customer_summary = (
        customer_orders
        .groupby("customer_unique_id")
        .agg(
            total_orders=(
                "order_id",
                "nunique"
            ),

            total_spend=(
                "total_order_value",
                "sum"
            ),

            average_order_value=(
                "total_order_value",
                "mean"
            ),

            first_order=(
                "order_purchase_timestamp",
                "min"
            ),

            last_order=(
                "order_purchase_timestamp",
                "max"
            )
        )
        .reset_index()
    )

    # --------------------------------------------------------
    # Customer lifetime
    # --------------------------------------------------------

    customer_summary["customer_lifetime_days"] = (
        customer_summary["last_order"]
        - customer_summary["first_order"]
    ).dt.days

    print("Customer summary created.")

    return customer_summary


# ============================================================
# 12. SELLER SUMMARY
# ============================================================

def create_seller_summary(order_items):

    seller_summary = (
        order_items
        .groupby("seller_id")
        .agg(
            items_sold=(
                "order_item_id",
                "count"
            ),

            revenue=(
                "price",
                "sum"
            ),

            average_price=(
                "price",
                "mean"
            ),

            average_freight=(
                "freight_value",
                "mean"
            )
        )
        .reset_index()
    )

    print("Seller summary created.")

    return seller_summary


# ============================================================
# 13. PRODUCT SUMMARY
# ============================================================

def create_product_summary(order_items):

    product_summary = (
        order_items
        .groupby("product_id")
        .agg(
            units_sold=(
                "order_item_id",
                "count"
            ),

            revenue=(
                "price",
                "sum"
            ),

            average_price=(
                "price",
                "mean"
            ),

            average_freight=(
                "freight_value",
                "mean"
            )
        )
        .reset_index()
    )

    print("Product summary created.")

    return product_summary

# ============================================================
# 14. SAVE PROCESSED DATA
# ============================================================

def save_data(
    orders,
    order_items,
    payments,
    reviews,
    products,
    order_summary,
    customer_summary,
    seller_summary,
    product_summary
):

    orders.to_csv(
        PROCESSED_DATA / "orders_features.csv",
        index=False
    )

    order_items.to_csv(
        PROCESSED_DATA / "order_items_features.csv",
        index=False
    )

    payments.to_csv(
        PROCESSED_DATA / "payments_features.csv",
        index=False
    )

    reviews.to_csv(
        PROCESSED_DATA / "reviews_features.csv",
        index=False
    )

    products.to_csv(
        PROCESSED_DATA / "products_features.csv",
        index=False
    )

    order_summary.to_csv(
        PROCESSED_DATA / "order_summary.csv",
        index=False
    )

    customer_summary.to_csv(
        PROCESSED_DATA / "customer_summary.csv",
        index=False
    )

    seller_summary.to_csv(
        PROCESSED_DATA / "seller_summary.csv",
        index=False
    )

    product_summary.to_csv(
        PROCESSED_DATA / "product_summary.csv",
        index=False
    )

    print("\nAll processed files saved.")


# ============================================================
# 15. MAIN PROGRAM
# ============================================================

def main():

    print("\nStarting feature engineering...\n")

    # --------------------------------------------------------
    # Load data
    # --------------------------------------------------------

    (
        customers,
        orders,
        order_items,
        payments,
        reviews,
        products,
        sellers,
        category_translation
    ) = load_data()

    # --------------------------------------------------------
    # Convert dates
    # --------------------------------------------------------

    orders, reviews, order_items = convert_dates(
        orders,
        reviews,
        order_items
    )

    # --------------------------------------------------------
    # Create features
    # --------------------------------------------------------

    orders = create_order_date_features(
        orders
    )

    orders = create_delivery_features(
        orders
    )

    order_items = create_order_item_features(
        order_items
    )

    payments = create_payment_features(
        payments
    )

    reviews = create_review_features(
        reviews
    )

    products = create_product_features(
        products,
        category_translation
    )

    # --------------------------------------------------------
    # Create summaries
    # --------------------------------------------------------

    order_summary = create_order_summary(
        order_items
    )

    customer_summary = create_customer_summary(
        orders,
        order_summary,
        customers
    )

    seller_summary = create_seller_summary(
        order_items
    )

    product_summary = create_product_summary(
        order_items
    )

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    save_data(
        orders,
        order_items,
        payments,
        reviews,
        products,
        order_summary,
        customer_summary,
        seller_summary,
        product_summary
    )

    print("\nFeature engineering completed successfully.")

    print("\nFiles created:")
    print("1. orders_features.csv")
    print("2. order_items_features.csv")
    print("3. payments_features.csv")
    print("4. reviews_features.csv")
    print("5. products_features.csv")
    print("6. order_summary.csv")
    print("7. customer_summary.csv")
    print("8. seller_summary.csv")
    print("9. product_summary.csv")

    print("\nNext step: Validate processed data.")


# ============================================================
# 16. RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main ()