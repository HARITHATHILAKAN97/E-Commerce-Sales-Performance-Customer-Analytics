# ============================================================
# OLIST E-COMMERCE PROJECT
# PYTHON DATA CLEANING

# ============================================================

import pandas as pd
from pathlib import Path

# SET PROJECT FOLDERS
# ============================================================

CLEAN_DATA = Path(__file__).resolve().parent.parent

RAW_DATA = CLEAN_DATA / "data" / "raw"
CLEANED_DATA = CLEAN_DATA / "data" / "cleaned"
OUTPUT_DATA = CLEAN_DATA / "outputs"

# Create folders if they don't exist
CLEANED_DATA.mkdir(parents=True, exist_ok=True)
OUTPUT_DATA.mkdir(parents=True, exist_ok=True)


# CREATE A CLEANING REPORT TITLE
# ============================================================

report = []

report.append("OLIST DATA CLEANING REPORT")
report.append("=" * 60)
report.append("")


#  COMMON CLEANING FUNCTION
# ============================================================

def cleaning(df, table_name):
    report.append(f"\n{table_name}")
    report.append("-" * 60)

    # Original row count
    original_rows = len(df)

    report.append(
        f"Original rows: {original_rows}"
    )

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Clean text columns
    text_columns = df.select_dtypes(
        include="object"
    ).columns

    for column in text_columns:

        df[column] = (
            df[column]
            .str.strip()
        )
        # Convert empty strings to missing values
        df[column] = df[column].replace(
            "",
            pd.NA
        )

    # Check exact duplicate rows
   

    duplicate_rows = df.duplicated().sum()

    report.append(
        f"Exact duplicate rows found: {duplicate_rows}"
    )

    # Remove only exact duplicates
    if duplicate_rows > 0:
        df = df.drop_duplicates()

    report.append(
        f"Rows after duplicate removal: {len(df)}"
    )

     # Missing values
   
    missing_values = df.isna().sum().sum()

    report.append(
        f"Missing cells remaining: {missing_values}"
    )

    return df

# CUSTOMERS
# ============================================================

customers = pd.read_csv(
    RAW_DATA / "olist_customers_dataset.csv"
)

customers = cleaning(
    customers,
    "CUSTOMERS"
)

# Check customer_id duplicates
customer_id_duplicates = (
    customers["customer_id"]
    .duplicated()
    .sum()
)

# Check customer_unique_id duplicates
customer_unique_duplicates = (
    customers["customer_unique_id"]
    .duplicated()
    .sum()
)

report.append(
    f"Duplicate customer_id: "
    f"{customer_id_duplicates}"
)

report.append(
    f"Duplicate customer_unique_id: "
    f"{customer_unique_duplicates}"
)

# Save
customers.to_csv(
    CLEANED_DATA / "customers_clean.csv",
    index=False
)

print("Customers completed.")


#  ORDERS
# ============================================================

print("\nCleaning Orders...")

orders = pd.read_csv(
    RAW_DATA / "olist_orders_dataset.csv"
)

orders = cleaning(
    orders,
    "ORDERS"
)

# ------------------------------------------------------------
# Convert date columns
# ------------------------------------------------------------

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:

    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )

report.append(
    "Order date columns converted to datetime."
)


# Check order_id uniqueness


order_id_duplicates = (
    orders["order_id"]
    .duplicated()
    .sum()
)

report.append(
    f"Duplicate order_id: {order_id_duplicates}"
)


# Check delivery date problems


delivered_before_purchase = (
    orders["order_delivered_customer_date"]
    < orders["order_purchase_timestamp"]
).sum()

report.append(
    f"Delivered before purchase date: "
    f"{delivered_before_purchase}"
)

# Save
orders.to_csv(
    CLEANED_DATA/ "orders_clean.csv",
    index=False
)

print("Orders completed.")


#  ORDER ITEMS
# ============================================================

print("\nCleaning Order Items...")

order_items = pd.read_csv(
    RAW_DATA / "olist_order_items_dataset.csv"
)

order_items = cleaning(
    order_items,
    "ORDER ITEMS"
)

# Convert date
order_items["shipping_limit_date"] = pd.to_datetime(
    order_items["shipping_limit_date"],
    errors="coerce"
)

# Check negative values


negative_price = (
    order_items["price"] < 0
).sum()

negative_freight = (
    order_items["freight_value"] < 0
).sum()

report.append(
    f"Negative price values: {negative_price}"
)

report.append(
    f"Negative freight values: {negative_freight}"
)

# Save
order_items.to_csv(
    CLEANED_DATA / "order_items_clean.csv",
    index=False
)

print("Order items completed.")



# PAYMENTS


print("\nCleaning Payments...")

payments = pd.read_csv(
    RAW_DATA / "olist_order_payments_dataset.csv"
)

payments = cleaning(
    payments,
    "PAYMENTS"
)


# Check payment values


negative_payment = (
    payments["payment_value"] < 0
).sum()

invalid_installments = (
    payments["payment_installments"] <= 0
).sum()

report.append(
    f"Negative payment values: {negative_payment}"
)

report.append(
    f"Invalid installment values: "
    f"{invalid_installments}"
)

# Save
payments.to_csv(
    CLEANED_DATA / "payments_clean.csv",
    index=False
)

print("Payments completed.")


# REVIEWS


print("\nCleaning Reviews...")

reviews = pd.read_csv(
    RAW_DATA / "olist_order_reviews_dataset.csv"
)

reviews = cleaning(
    reviews,
    "REVIEWS"
)


# Convert dates


reviews["review_creation_date"] = pd.to_datetime(
    reviews["review_creation_date"],
    errors="coerce"
)

reviews["review_answer_timestamp"] = pd.to_datetime(
    reviews["review_answer_timestamp"],
    errors="coerce"
)

# Review score validation


invalid_scores = (
    ~reviews["review_score"].between(1, 5)
).sum()

report.append(
    f"Invalid review scores: {invalid_scores}"
)


duplicate_review_ids = (
    reviews["review_id"]
    .duplicated()
    .sum()
)

report.append(
    f"Duplicate review_id values: "
    f"{duplicate_review_ids}"
)

report.append(
    "Duplicate review_id values retained "
    "for further investigation."
)

# Save
reviews.to_csv(
    CLEANED_DATA / "reviews_clean.csv",
    index=False
)

print("Reviews completed.")



#  PRODUCTS


print("\nCleaning Products...")

products = pd.read_csv(
    RAW_DATA / "olist_products_dataset.csv"
)

products = cleaning(
    products,
    "PRODUCTS"
)

# Convert numeric columns


numeric_columns = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

for column in numeric_columns:

    if column in products.columns:

        products[column] = pd.to_numeric(
            products[column],
            errors="coerce"
        )

# ------------------------------------------------------------
# Check negative product values
# ------------------------------------------------------------

report.append(
    "Product numeric columns converted."
)

for column in numeric_columns:

    if column in products.columns:

        negative_values = (
            products[column] < 0
        ).sum()

        if negative_values > 0:

            report.append(
                f"{column} negative values: "
                f"{negative_values}"
            )

# Save
products.to_csv(
    CLEANED_DATA / "products_clean.csv",
    index=False
)

print("Products completed.")



#  SELLERS


print("\nCleaning Sellers...")

sellers = pd.read_csv(
    RAW_DATA / "olist_sellers_dataset.csv"
)

sellers = cleaning(
    sellers,
    "SELLERS"
)

seller_id_duplicates = (
    sellers["seller_id"]
    .duplicated()
    .sum()
)

report.append(
    f"Duplicate seller_id: "
    f"{seller_id_duplicates}"
)

# Save
sellers.to_csv(
    CLEANED_DATA / "sellers_clean.csv",
    index=False
)

print("Sellers completed.")



#  GEOLOCATION


print("\nCleaning Geolocation...")

geolocation = pd.read_csv(
    RAW_DATA / "olist_geolocation_dataset.csv"
)

geolocation = cleaning(
    geolocation,
    "GEOLOCATION"
)

original_geo_rows = len(geolocation)


# create a unique location reference.


location_columns = [
    "geolocation_zip_code_prefix",
    "geolocation_lat",
    "geolocation_lng",
    "geolocation_city",
    "geolocation_state"
]

geolocation = geolocation.drop_duplicates(
    subset=location_columns
)

report.append(
    f"Geolocation rows before "
    f"location deduplication: "
    f"{original_geo_rows}"
)

report.append(
    f"Geolocation rows after "
    f"location deduplication: "
    f"{len(geolocation)}"
)

# Save
geolocation.to_csv(
    CLEANED_DATA / "geolocation_clean.csv",
    index=False
)




# CATEGORY TRANSLATION



category_translation = pd.read_csv(
    RAW_DATA / "product_category_name_translation.csv"
)

category_translation = cleaning(
    category_translation,
    "CATEGORY TRANSLATION"
)

# Check missing translations
missing_translations = (
    category_translation[
        "product_category_name_english"
    ].isna()
).sum()

report.append(
    f"Missing English translations: "
    f"{missing_translations}"
)

# Save
category_translation.to_csv(
    CLEANED_DATA /
    "category_translation_clean.csv",
    index=False
)

print("Category translation completed.")



#  SAVE CLEANING REPORT


report_path = (
    OUTPUT_DATA /
    "cleaning_report.txt"
)

with open(
    report_path,
    "w",
    encoding="utf-8"
) as file:

    for line in report:

        file.write(
            line + "\n"
        )



#  FINAL MESSAGE
# ============================================================

print("\n")
print("=" * 60)
print("OLIST DATA CLEANING COMPLETED")
print("=" * 60)

print("\nCleaned files saved in:")

print(CLEANED_DATA)

print("\nCleaning report saved in:")

print(report_path)


