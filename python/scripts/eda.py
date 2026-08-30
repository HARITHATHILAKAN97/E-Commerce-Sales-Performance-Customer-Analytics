# ============================================================
# OLIST E-COMMERCE PROJECT
# EDA ANALYSIS
# Beginner -> Intermediate
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# 1. FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DATA = BASE_DIR / "data" / "processed"
OUTPUT_FOLDER = BASE_DIR / "outputs" / "eda"

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 2. LOAD PROCESSED DATA
# ============================================================

def load_data():

    orders = pd.read_csv(
        PROCESSED_DATA / "orders_features.csv"
    )

    order_items = pd.read_csv(
        PROCESSED_DATA / "order_items_features.csv"
    )

    payments = pd.read_csv(
        PROCESSED_DATA / "payments_features.csv"
    )

    reviews = pd.read_csv(
        PROCESSED_DATA / "reviews_features.csv"
    )

    products = pd.read_csv(
        PROCESSED_DATA / "products_features.csv"
    )

    order_summary = pd.read_csv(
        PROCESSED_DATA / "order_summary.csv"
    )

    customer_summary = pd.read_csv(
        PROCESSED_DATA / "customer_summary.csv"
    )

    seller_summary = pd.read_csv(
        PROCESSED_DATA / "seller_summary.csv"
    )

    product_summary = pd.read_csv(
        PROCESSED_DATA / "product_summary.csv"
    )

    print("Processed datasets loaded.")

    return (
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


# ============================================================
# 3. BASIC DATA OVERVIEW
# ============================================================

def basic_overview(
    orders,
    order_items,
    payments,
    reviews,
    products,
    customer_summary,
    seller_summary,
    product_summary
):

    print("\n")
    print("=" * 60)
    print("BASIC DATA OVERVIEW")
    print("=" * 60)

    print("\nOrders:")
    print(orders.shape)

    print("\nOrder Items:")
    print(order_items.shape)

    print("\nPayments:")
    print(payments.shape)

    print("\nReviews:")
    print(reviews.shape)

    print("\nProducts:")
    print(products.shape)

    print("\nCustomers:")
    print(customer_summary.shape)

    print("\nSellers:")
    print(seller_summary.shape)

    print("\nProduct Summary:")
    print(product_summary.shape)


# ============================================================
# 4. DATE RANGE
# ============================================================

def analyze_date_range(orders):

    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"]
    )

    first_date = orders[
        "order_purchase_timestamp"
    ].min()

    last_date = orders[
        "order_purchase_timestamp"
    ].max()

    print("\n")
    print("=" * 60)
    print("ORDER DATE RANGE")
    print("=" * 60)

    print("First order:", first_date)
    print("Last order:", last_date)


# ============================================================
# 5. DESCRIPTIVE STATISTICS
# ============================================================

def descriptive_statistics(
    order_items,
    order_summary,
    customer_summary
):

    print("\n")
    print("=" * 60)
    print("DESCRIPTIVE STATISTICS")
    print("=" * 60)

    print("\nOrder Item Statistics:")
    print(
        order_items[
            [
                "price",
                "freight_value",
                "item_total_value"
            ]
        ].describe()
    )

    print("\nOrder Value Statistics:")
    print(
        order_summary[
            ["total_order_value"]
        ].describe()
    )

    print("\nCustomer Spending Statistics:")
    print(
        customer_summary[
            [
                "total_orders",
                "total_spend",
                "average_order_value"
            ]
        ].describe()
    )


# ============================================================
# 6. MONTHLY ORDERS
# ============================================================

def monthly_orders(orders):

    monthly = (
        orders
        .groupby(
            [
                "order_year",
                "order_month"
            ]
        )
        .size()
        .reset_index(
            name="number_of_orders"
        )
    )

    monthly["year_month"] = (
        monthly["order_year"].astype(str)
        + "-"
        + monthly["order_month"].astype(str).str.zfill(2)
    )

    print("\nMonthly Orders:")
    print(monthly)

    plt.figure(figsize=(10, 5))

    plt.plot(
        monthly["year_month"],
        monthly["number_of_orders"]
    )

    plt.title("Monthly Order Trend")
    plt.xlabel("Month")
    plt.ylabel("Number of Orders")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "monthly_orders.png"
    )

    plt.show()

    return monthly


# ============================================================
# 7. MONTHLY REVENUE
# ============================================================

def monthly_revenue(
    orders,
    order_summary
):

    data = orders.merge(
        order_summary[
            [
                "order_id",
                "total_order_value"
            ]
        ],
        on="order_id",
        how="left"
    )

    monthly = (
        data
        .groupby(
            [
                "order_year",
                "order_month"
            ]
        )["total_order_value"]
        .sum()
        .reset_index()
    )

    monthly["year_month"] = (
        monthly["order_year"].astype(str)
        + "-"
        + monthly["order_month"].astype(str).str.zfill(2)
    )

    print("\nMonthly Revenue:")
    print(monthly)

    plt.figure(figsize=(10, 5))

    plt.plot(
        monthly["year_month"],
        monthly["total_order_value"]
    )

    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "monthly_revenue.png"
    )

    plt.show()

    return monthly


# ============================================================
# 8. TOP PRODUCT CATEGORIES
# ============================================================

def top_product_categories(products):

    if "product_category_name_english" in products.columns:

        categories = (
            products
            .groupby(
                "product_category_name_english"
            )
            .size()
            .sort_values(
                ascending=False
            )
            .head(10)
        )

    else:

        categories = (
            products
            .groupby(
                "product_category_name"
            )
            .size()
            .sort_values(
                ascending=False
            )
            .head(10)
        )

    print("\nTop Product Categories:")
    print(categories)

    categories.plot(
        kind="bar",
        figsize=(10, 5)
    )

    plt.title(
        "Top 10 Product Categories"
    )

    plt.xlabel("Product Category")
    plt.ylabel("Number of Products")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "top_product_categories.png"
    )

    plt.show()

    return categories


# ============================================================
# 9. TOP PRODUCTS BY SALES
# ============================================================

def top_products(product_summary):

    top_products = (
        product_summary
        .sort_values(
            "revenue",
            ascending=False
        )
        .head(10)
    )

    print("\nTop 10 Products by Revenue:")
    print(top_products)

    top_products.plot(
        x="product_id",
        y="revenue",
        kind="bar",
        figsize=(10, 5)
    )

    plt.title(
        "Top 10 Products by Revenue"
    )

    plt.xlabel("Product")
    plt.ylabel("Revenue")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "top_products_revenue.png"
    )

    plt.show()

    return top_products


# ============================================================
# 10. TOP SELLERS
# ============================================================

def top_sellers(seller_summary):

    top_sellers = (
        seller_summary
        .sort_values(
            "revenue",
            ascending=False
        )
        .head(10)
    )

    print("\nTop 10 Sellers:")
    print(top_sellers)

    top_sellers.plot(
        x="seller_id",
        y="revenue",
        kind="bar",
        figsize=(10, 5)
    )

    plt.title(
        "Top 10 Sellers by Revenue"
    )

    plt.xlabel("Seller")
    plt.ylabel("Revenue")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "top_sellers.png"
    )

    plt.show()

    return top_sellers


# ============================================================
# 11. REVIEW SCORE ANALYSIS
# ============================================================

def review_analysis(reviews):

    review_counts = (
        reviews["review_score"]
        .value_counts()
        .sort_index()
    )

    print("\nReview Score Distribution:")
    print(review_counts)

    review_counts.plot(
        kind="bar",
        figsize=(8, 5)
    )

    plt.title(
        "Customer Review Score Distribution"
    )

    plt.xlabel("Review Score")
    plt.ylabel("Number of Reviews")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "review_score_distribution.png"
    )

    plt.show()

    return review_counts


# ============================================================
# 12. DELIVERY ANALYSIS
# ============================================================

def delivery_analysis(orders):

    delivery = (
        orders[
            [
                "delivery_days",
                "delivery_delay_days"
            ]
        ]
        .describe()
    )

    print("\nDelivery Statistics:")
    print(delivery)

    late_orders = (
        orders["late_delivery"]
        .value_counts()
    )

    print("\nLate Delivery Count:")
    print(late_orders)

    late_orders.plot(
        kind="bar",
        figsize=(7, 5)
    )

    plt.title(
        "On-Time vs Late Deliveries"
    )

    plt.xlabel("Late Delivery")
    plt.ylabel("Number of Orders")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "late_delivery.png"
    )

    plt.show()

    return late_orders


# ============================================================
# 13. PAYMENT METHOD ANALYSIS
# ============================================================

def payment_analysis(payments):

    payment_methods = (
        payments["payment_type"]
        .value_counts()
    )

    print("\nPayment Methods:")
    print(payment_methods)

    payment_methods.plot(
        kind="bar",
        figsize=(8, 5)
    )

    plt.title(
        "Payment Method Usage"
    )

    plt.xlabel("Payment Method")
    plt.ylabel("Number of Payments")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "payment_methods.png"
    )

    plt.show()

    return payment_methods


# ============================================================
# 14. CUSTOMER ANALYSIS
# ============================================================

def customer_analysis(customer_summary):

    print("\nCustomer Analysis:")

    print(
        "\nCustomers with more than one order:"
    )

    repeat_customers = customer_summary[
        customer_summary["total_orders"] > 1
    ]

    print(
        "Number of repeat customers:",
        len(repeat_customers)
    )

    print(
        "\nTop 10 customers by spending:"
    )

    top_customers = (
        customer_summary
        .sort_values(
            "total_spend",
            ascending=False
        )
        .head(10)
    )

    print(top_customers)

    return top_customers


# ============================================================
# 15. FREIGHT VS PRICE
# ============================================================

def freight_analysis(order_items):

    print("\nFreight vs Product Price:")

    print(
        order_items[
            [
                "price",
                "freight_value"
            ]
        ].corr()
    )

    plt.figure(figsize=(8, 5))

    plt.scatter(
        order_items["price"],
        order_items["freight_value"],
        alpha=0.3
    )

    plt.title(
        "Product Price vs Freight Value"
    )

    plt.xlabel("Product Price")
    plt.ylabel("Freight Value")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "price_vs_freight.png"
    )

    plt.show()


# ============================================================
# 16. MAIN PROGRAM
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("OLIST EDA STARTED")
    print("=" * 60)

    # Load data
    (
        orders,
        order_items,
        payments,
        reviews,
        products,
        order_summary,
        customer_summary,
        seller_summary,
        product_summary
    ) = load_data()


    # Basic overview
    basic_overview(
        orders,
        order_items,
        payments,
        reviews,
        products,
        customer_summary,
        seller_summary,
        product_summary
    )


    # Date range
    analyze_date_range(
        orders
    )


    # Descriptive statistics
    descriptive_statistics(
        order_items,
        order_summary,
        customer_summary
    )


    # Business analysis
    monthly_orders(
        orders
    )

    monthly_revenue(
        orders,
        order_summary
    )

    top_product_categories(
        products
    )

    top_products(
        product_summary
    )

    top_sellers(
        seller_summary
    )

    review_analysis(
        reviews
    )

    delivery_analysis(
        orders
    )

    payment_analysis(
        payments
    )

    customer_analysis(
        customer_summary
    )

    freight_analysis(
        order_items
    )


    print("\n")
    print("=" * 60)
    print("EDA COMPLETED")
    print("=" * 60)

    print("\nCharts saved in:")
    print(OUTPUT_FOLDER)


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()