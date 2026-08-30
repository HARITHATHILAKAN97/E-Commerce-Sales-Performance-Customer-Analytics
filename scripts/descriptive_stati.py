# ============================================================
# OLIST E-COMMERCE PROJECT
# STATISTICAL ANALYSIS
# Beginner -> Intermediate
# ============================================================

import pandas as pd
from pathlib import Path
from scipy.stats import ttest_ind


# ============================================================
# 1. FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DATA = BASE_DIR / "data" / "processed"
OUTPUT_FOLDER = BASE_DIR / "outputs" / "statistics"

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 2. LOAD DATA
# ============================================================

def load_data():

    orders = pd.read_csv(
        PROCESSED_DATA / "orders_features.csv"
    )

    order_items = pd.read_csv(
        PROCESSED_DATA / "order_items_features.csv"
    )

    order_summary = pd.read_csv(
        PROCESSED_DATA / "order_summary.csv"
    )

    customer_summary = pd.read_csv(
        PROCESSED_DATA / "customer_summary.csv"
    )

    reviews = pd.read_csv(
        PROCESSED_DATA / "reviews_features.csv"
    )

    print("Data loaded successfully.")

    return (
        orders,
        order_items,
        order_summary,
        customer_summary,
        reviews
    )


# ============================================================
# 3. CREATE REPORT
# ============================================================

report = []


def write_report(text):

    print(text)
    report.append(text)


# ============================================================
# 4. DESCRIPTIVE STATISTICS
# ============================================================

def descriptive_statistics(
    order_items,
    order_summary,
    customer_summary
):

    write_report("\n")
    write_report("=" * 60)
    write_report("1. DESCRIPTIVE STATISTICS")
    write_report("=" * 60)

    # --------------------------------------------------------
    # Product price
    # --------------------------------------------------------

    price = order_items["price"].dropna()

    write_report("\nPRODUCT PRICE")

    write_report(
        f"Mean: {price.mean():.2f}"
    )

    write_report(
        f"Median: {price.median():.2f}"
    )

    write_report(
        f"Standard deviation: {price.std():.2f}"
    )

    write_report(
        f"Minimum: {price.min():.2f}"
    )

    write_report(
        f"Maximum: {price.max():.2f}"
    )

    # --------------------------------------------------------
    # Order value
    # --------------------------------------------------------

    order_value = (
        order_summary["total_order_value"]
        .dropna()
    )

    write_report("\nORDER VALUE")

    write_report(
        f"Mean: {order_value.mean():.2f}"
    )

    write_report(
        f"Median: {order_value.median():.2f}"
    )

    write_report(
        f"Standard deviation: {order_value.std():.2f}"
    )

    write_report(
        f"Minimum: {order_value.min():.2f}"
    )

    write_report(
        f"Maximum: {order_value.max():.2f}"
    )

    # --------------------------------------------------------
    # Customer spending
    # --------------------------------------------------------

    spending = (
        customer_summary["total_spend"]
        .dropna()
    )

    write_report("\nCUSTOMER SPENDING")

    write_report(
        f"Mean: {spending.mean():.2f}"
    )

    write_report(
        f"Median: {spending.median():.2f}"
    )

    write_report(
        f"Standard deviation: {spending.std():.2f}"
    )


# ============================================================
# 5. CORRELATION ANALYSIS
# ============================================================

def correlation_analysis(order_items):

    write_report("\n")
    write_report("=" * 60)
    write_report("2. CORRELATION ANALYSIS")
    write_report("=" * 60)

    data = order_items[
        [
            "price",
            "freight_value"
        ]
    ].dropna()

    correlation = data[
        "price"
    ].corr(
        data["freight_value"]
    )

    write_report(
        f"\nPrice vs Freight correlation: "
        f"{correlation:.3f}"
    )

    # Simple interpretation

    if correlation >= 0.7:

        write_report(
            "Interpretation: Strong positive relationship."
        )

    elif correlation >= 0.4:

        write_report(
            "Interpretation: Moderate positive relationship."
        )

    elif correlation >= 0.2:

        write_report(
            "Interpretation: Weak positive relationship."
        )

    elif correlation <= -0.7:

        write_report(
            "Interpretation: Strong negative relationship."
        )

    elif correlation <= -0.4:

        write_report(
            "Interpretation: Moderate negative relationship."
        )

    elif correlation <= -0.2:

        write_report(
            "Interpretation: Weak negative relationship."
        )

    else:

        write_report(
            "Interpretation: Very weak or no linear relationship."
        )


# ============================================================
# 6. OUTLIER ANALYSIS
# ============================================================

def find_outliers(data):

    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)

    IQR = Q3 - Q1

    lower_limit = Q1 - (1.5 * IQR)
    upper_limit = Q3 + (1.5 * IQR)

    outliers = data[
        (data < lower_limit)
        |
        (data > upper_limit)
    ]

    return outliers


def outlier_analysis(
    order_items,
    order_summary,
    customer_summary
):

    write_report("\n")
    write_report("=" * 60)
    write_report("3. OUTLIER ANALYSIS")
    write_report("=" * 60)

    # Product price

    price_outliers = find_outliers(
        order_items["price"].dropna()
    )

    write_report(
        f"\nProduct price outliers: "
        f"{len(price_outliers)}"
    )

    # Order value

    order_outliers = find_outliers(
        order_summary[
            "total_order_value"
        ].dropna()
    )

    write_report(
        f"Order value outliers: "
        f"{len(order_outliers)}"
    )

    # Customer spending

    customer_outliers = find_outliers(
        customer_summary[
            "total_spend"
        ].dropna()
    )

    write_report(
        f"Customer spending outliers: "
        f"{len(customer_outliers)}"
    )

    write_report(
        "\nNote: Outliers are identified for investigation."
    )

    write_report(
        "They are not automatically removed."
    )


# ============================================================
# 7. LATE DELIVERY VS REVIEW SCORE
# ============================================================

def delivery_vs_review(
    orders,
    reviews
):

    write_report("\n")
    write_report("=" * 60)
    write_report("4. LATE DELIVERY VS REVIEW SCORE")
    write_report("=" * 60)

    # Connect orders with reviews

    data = orders[
        [
            "order_id",
            "late_delivery"
        ]
    ].merge(
        reviews[
            [
                "order_id",
                "review_score"
            ]
        ],
        on="order_id",
        how="inner"
    )

    data = data.dropna(
        subset=["review_score"]
    )

    # On-time orders

    on_time = data[
        data["late_delivery"] == False
    ]["review_score"]

    # Late orders

    late = data[
        data["late_delivery"] == True
    ]["review_score"]

    write_report(
        f"\nOn-time orders: {len(on_time)}"
    )

    write_report(
        f"Late orders: {len(late)}"
    )

    write_report(
        f"\nAverage review - On time: "
        f"{on_time.mean():.2f}"
    )

    write_report(
        f"Average review - Late: "
        f"{late.mean():.2f}"
    )

    # --------------------------------------------------------
    # T-test
    # --------------------------------------------------------

    t_stat, p_value = ttest_ind(
        on_time,
        late,
        equal_var=False
    )

    write_report(
        f"\nT-statistic: {t_stat:.3f}"
    )

    write_report(
        f"P-value: {p_value:.5f}"
    )

    if p_value < 0.05:

        write_report(
            "Result: The difference is statistically significant."
        )

    else:

        write_report(
            "Result: The difference is not statistically significant."
        )


# ============================================================
# 8. REPEAT VS ONE-TIME CUSTOMERS
# ============================================================

def repeat_customer_analysis(
    customer_summary
):

    write_report("\n")
    write_report("=" * 60)
    write_report("5. REPEAT VS ONE-TIME CUSTOMERS")
    write_report("=" * 60)

    # One-time customers

    one_time = customer_summary[
        customer_summary["total_orders"] == 1
    ]["total_spend"].dropna()

    # Repeat customers

    repeat = customer_summary[
        customer_summary["total_orders"] > 1
    ]["total_spend"].dropna()

    write_report(
        f"\nOne-time customers: {len(one_time)}"
    )

    write_report(
        f"Repeat customers: {len(repeat)}"
    )

    write_report(
        f"\nAverage spend - One-time: "
        f"{one_time.mean():.2f}"
    )

    write_report(
        f"Average spend - Repeat: "
        f"{repeat.mean():.2f}"
    )

    # --------------------------------------------------------
    # T-test
    # --------------------------------------------------------

    t_stat, p_value = ttest_ind(
        one_time,
        repeat,
        equal_var=False
    )

    write_report(
        f"\nT-statistic: {t_stat:.3f}"
    )

    write_report(
        f"P-value: {p_value:.5f}"
    )

    if p_value < 0.05:

        write_report(
            "Result: Spending difference is statistically significant."
        )

    else:

        write_report(
            "Result: Spending difference is not statistically significant."
        )


# ============================================================
# 9. DELIVERY DELAY VS REVIEW CORRELATION
# ============================================================

def delivery_delay_correlation(
    orders,
    reviews
):

    write_report("\n")
    write_report("=" * 60)
    write_report("6. DELIVERY DELAY VS REVIEW SCORE")
    write_report("=" * 60)

    data = orders[
        [
            "order_id",
            "delivery_delay_days"
        ]
    ].merge(
        reviews[
            [
                "order_id",
                "review_score"
            ]
        ],
        on="order_id",
        how="inner"
    )

    data = data.dropna()

    correlation = data[
        "delivery_delay_days"
    ].corr(
        data["review_score"]
    )

    write_report(
        f"\nCorrelation: {correlation:.3f}"
    )

    if correlation < -0.4:

        write_report(
            "Interpretation: Strong negative relationship."
        )

    elif correlation < -0.2:

        write_report(
            "Interpretation: Weak negative relationship."
        )

    elif correlation > 0.4:

        write_report(
            "Interpretation: Strong positive relationship."
        )

    elif correlation > 0.2:

        write_report(
            "Interpretation: Weak positive relationship."
        )

    else:

        write_report(
            "Interpretation: Very weak or no linear relationship."
        )


# ============================================================
# 10. SAVE REPORT
# ============================================================

def save_report():

    report_file = (
        OUTPUT_FOLDER
        / "statistical_analysis_report.txt"
    )

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n".join(report)
        )

    print(
        "\nReport saved successfully:"
    )

    print(report_file)


# ============================================================
# 11. MAIN PROGRAM
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("OLIST STATISTICAL ANALYSIS")
    print("=" * 60)

    # Load data

    (
        orders,
        order_items,
        order_summary,
        customer_summary,
        reviews
    ) = load_data()

    # 1. Descriptive statistics

    descriptive_statistics(
        order_items,
        order_summary,
        customer_summary
    )

    # 2. Correlation

    correlation_analysis(
        order_items
    )

    # 3. Outliers

    outlier_analysis(
        order_items,
        order_summary,
        customer_summary
    )

    # 4. Delivery vs review

    delivery_vs_review(
        orders,
        reviews
    )

    # 5. Customer behavior

    repeat_customer_analysis(
        customer_summary
    )

    # 6. Delivery delay correlation

    delivery_delay_correlation(
        orders,
        reviews
    )

    # Save report

    save_report()

    print("\n")
    print("=" * 60)
    print("STATISTICAL ANALYSIS COMPLETED")
    print("=" * 60)


# ============================================================
# 12. RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()