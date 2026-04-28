# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Welcome message
print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Create a seed for reproducibility
np.random.seed(42)

# Generate dates for 8 quarters (Q1 2022 - Q4 2023)
quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022',
                 'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

# Store locations
locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']

# Product categories
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

# Generate quarterly sales data for each location and category
quarterly_data = []

for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            # Base sales with seasonal pattern (Q4 higher, Q1 lower)
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.0
            if quarter.quarter == 4:  # Q4 (holiday boost)
                seasonal_factor = 1.3
            elif quarter.quarter == 1:  # Q1 (post-holiday dip)
                seasonal_factor = 0.8

            # Location effect
            location_factor = {
                'Tampa': 1.0,
                'Miami': 1.2,
                'Orlando': 0.9,
                'Jacksonville': 0.8
            }[location]

            # Category effect
            category_factor = {
                'Electronics': 1.5,
                'Clothing': 1.0,
                'Home Goods': 0.8,
                'Sporting Goods': 0.7,
                'Beauty': 0.9
            }[category]

            # Growth trend over time (5% per year, quarterly compounded)
            growth_factor = (1 + 0.05/4) ** quarter_idx

            # Calculate sales with some randomness
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)  # Add noise

            # Advertising spend (correlated with sales but with diminishing returns)
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)

            # Record
            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

# Create customer data
customer_data = []
total_customers = 2000

# Age distribution parameters for each location
age_params = {
    'Tampa': (45, 15),      # Older demographic
    'Miami': (35, 12),      # Younger demographic
    'Orlando': (38, 14),    # Mixed demographic
    'Jacksonville': (42, 13)  # Middle-aged demographic
}

for location in locations:
    # Generate ages based on location demographics
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {
        'Tampa': 0.3,
        'Miami': 0.35,
        'Orlando': 0.2,
        'Jacksonville': 0.15
    }[location])

    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)  # Ensure ages are between 18-80

    # Generate purchase amounts
    for age in ages:
        # Younger and older customers spend differently across categories
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])

        # Purchase amount based on age and category
        base_amount = np.random.gamma(shape=5, scale=20)

        # Product tier (budget, mid-range, premium)
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'],
                                     p=[0.3, 0.5, 0.2])

        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]

        purchase_amount = base_amount * tier_factor

        customer_data.append({
            'Location': location,
            'Age': age,
            'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2),
            'PriceTier': price_tier
        })

# Create DataFrames
sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

# Add some calculated columns
sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

# Print data info
print("\nSales Data Sample:")
print(sales_df.head())
print("\nCustomer Data Sample:")
print(customer_df.head())
print("\nDataFrames created successfully. Ready for visualization!")
# ----- END OF DATA CREATION -----


# TODO 1: Time Series Visualization - Sales Trends
# 1.1 Create a line chart showing overall quarterly sales trends
# REQUIRED: Function must create and return a matplotlib figure
def plot_quarterly_sales_trend():
    """
    Create a line chart showing total sales for each quarter.
    REQUIRED: Return the figure object
    """
    quarterly_sales = sales_df.groupby("QuarterLabel")["Sales"].sum()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(quarterly_sales.index, quarterly_sales.values, marker='o', linewidth=2)
    ax.set_title("Overall Quarterly Sales Trend")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Total Sales ($)")
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)

    max_idx = quarterly_sales.idxmax()
    max_val = quarterly_sales.max()
    max_pos = list(quarterly_sales.index).index(max_idx)
    ax.annotate(f"Peak: ${max_val:,.0f}",
                xy=(max_pos, max_val),
                xytext=(0, 10),
                textcoords="offset points",
                ha='center')

    plt.tight_layout()
    return fig

# 1.2 Create a multi-line chart comparing sales trends across locations
# REQUIRED: Function must create and return a matplotlib figure
def plot_location_sales_comparison():
    """
    Create a multi-line chart comparing quarterly sales across different locations.
    REQUIRED: Return the figure object
    """
    location_sales = sales_df.groupby(["QuarterLabel", "Location"])["Sales"].sum().unstack()

    fig, ax = plt.subplots(figsize=(10, 5))
    markers = ['o', 's', '^', 'D']

    for i, location in enumerate(location_sales.columns):
        ax.plot(location_sales.index, location_sales[location], marker=markers[i], linewidth=2, label=location)

    ax.set_title("Quarterly Sales Trends by Location")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales ($)")
    ax.legend(title="Location")
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)

    plt.tight_layout()
    return fig


# TODO 2: Categorical Comparison - Product Performance by Location
# 2.1 Create a grouped bar chart comparing category performance by location
# REQUIRED: Function must create and return a matplotlib figure
def plot_category_performance_by_location():
    """
    Create a grouped bar chart showing how each product category performs in different locations.
    REQUIRED: Return the figure object
    """
    recent_quarter = sales_df["QuarterLabel"].iloc[-1]
    recent_data = sales_df[sales_df["QuarterLabel"] == recent_quarter]
    category_location = recent_data.groupby(["Location", "Category"])["Sales"].sum().unstack()

    fig, ax = plt.subplots(figsize=(11, 6))
    category_location.plot(kind="bar", ax=ax)

    ax.set_title(f"Category Performance by Location ({recent_quarter})")
    ax.set_xlabel("Location")
    ax.set_ylabel("Sales ($)")
    ax.legend(title="Category", bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=0)

    plt.tight_layout()
    return fig

# 2.2 Create a stacked bar chart showing the composition of sales in each location
# REQUIRED: Function must create and return a matplotlib figure
def plot_sales_composition_by_location():
    """
    Create a stacked bar chart showing the composition of sales across categories for each location.
    REQUIRED: Return the figure object
    """
    recent_quarter = sales_df["QuarterLabel"].iloc[-1]
    recent_data = sales_df[sales_df["QuarterLabel"] == recent_quarter]
    category_location = recent_data.groupby(["Location", "Category"])["Sales"].sum().unstack()
    category_percent = category_location.div(category_location.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    category_percent.plot(kind="bar", stacked=True, ax=ax)

    ax.set_title(f"Sales Composition by Location ({recent_quarter})")
    ax.set_xlabel("Location")
    ax.set_ylabel("Percentage of Total Sales (%)")
    ax.legend(title="Category", bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=0)

    plt.tight_layout()
    return fig


# TODO 3: Relationship Analysis - Advertising and Sales
# 3.1 Create a scatter plot to examine the relationship between ad spend and sales
# REQUIRED: Function must create and return a matplotlib figure
def plot_ad_spend_vs_sales():
    """
    Create a scatter plot to visualize the relationship between advertising spend and sales.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(sales_df["AdSpend"], sales_df["Sales"], alpha=0.7)

    x = sales_df["AdSpend"]
    y = sales_df["Sales"]
    m, b = np.polyfit(x, y, 1)
    x_sorted = np.sort(x)
    ax.plot(x_sorted, m * x_sorted + b, linewidth=2, label="Best-Fit Line")

    top_outliers = sales_df.nlargest(3, "Sales")
    for _, row in top_outliers.iterrows():
        ax.annotate(f"{row['Location']} - {row['Category']}",
                    (row["AdSpend"], row["Sales"]),
                    xytext=(5, 5),
                    textcoords="offset points",
                    fontsize=8)

    ax.set_title("Advertising Spend vs. Sales")
    ax.set_xlabel("Advertising Spend ($)")
    ax.set_ylabel("Sales ($)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

# 3.2 Create a line chart showing sales per dollar spent on advertising over time
# REQUIRED: Function must create and return a matplotlib figure
def plot_ad_efficiency_over_time():
    """
    Create a line chart showing how efficient advertising spend has been over time.
    REQUIRED: Return the figure object
    """
    efficiency = sales_df.groupby("QuarterLabel")["SalesPerDollarSpent"].mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(efficiency.index, efficiency.values, marker='o', linewidth=2)

    best_quarter = efficiency.idxmax()
    best_value = efficiency.max()
    best_pos = list(efficiency.index).index(best_quarter)
    ax.annotate(f"Best: {best_value:.2f}",
                xy=(best_pos, best_value),
                xytext=(0, 10),
                textcoords="offset points",
                ha='center')

    ax.set_title("Advertising Efficiency Over Time")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales Per Dollar Spent")
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)

    plt.tight_layout()
    return fig


# TODO 4: Distribution Analysis - Customer Demographics
# 4.1 Create histograms of customer age distribution
# REQUIRED: Function must create and return a matplotlib figure with subplots
def plot_customer_age_distribution():
    """
    Create histograms showing the age distribution of customers, both overall and by location.
    REQUIRED: Return the figure object
    """
    fig, axes = plt.subplots(3, 2, figsize=(12, 12))
    axes = axes.flatten()

    overall_ages = customer_df["Age"]
    axes[0].hist(overall_ages, bins=20, alpha=0.8)
    axes[0].axvline(overall_ages.mean(), linestyle='--', linewidth=2, label=f"Mean: {overall_ages.mean():.1f}")
    axes[0].axvline(overall_ages.median(), linestyle=':', linewidth=2, label=f"Median: {overall_ages.median():.1f}")
    axes[0].set_title("Overall Age Distribution")
    axes[0].set_xlabel("Age")
    axes[0].set_ylabel("Frequency")
    axes[0].legend()

    for i, location in enumerate(locations, start=1):
        loc_ages = customer_df[customer_df["Location"] == location]["Age"]
        axes[i].hist(loc_ages, bins=15, alpha=0.8)
        axes[i].axvline(loc_ages.mean(), linestyle='--', linewidth=2, label=f"Mean: {loc_ages.mean():.1f}")
        axes[i].axvline(loc_ages.median(), linestyle=':', linewidth=2, label=f"Median: {loc_ages.median():.1f}")
        axes[i].set_title(f"{location} Age Distribution")
        axes[i].set_xlabel("Age")
        axes[i].set_ylabel("Frequency")
        axes[i].legend(fontsize=8)

    fig.delaxes(axes[5])

    fig.suptitle("Customer Age Distributions", fontsize=16)
    plt.tight_layout()
    return fig

# 4.2 Create box plots comparing purchase amounts by age groups
# REQUIRED: Function must create and return a matplotlib figure
def plot_purchase_by_age_group():
    """
    Create box plots showing purchase amounts across different age groups.
    REQUIRED: Return the figure object
    """
    df = customer_df.copy()
    bins = [18, 30, 45, 60, 100]
    labels = ["18-30", "31-45", "46-60", "61+"]
    df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels, right=True, include_lowest=True)

    grouped_data = [df[df["AgeGroup"] == label]["PurchaseAmount"] for label in labels]

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.boxplot(grouped_data, tick_labels=labels, patch_artist=True)

    ax.set_title("Purchase Amount by Age Group")
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Purchase Amount ($)")
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return fig


# TODO 5: Sales Distribution - Pricing Tiers
# 5.1 Create a histogram of purchase amounts
# REQUIRED: Function must create and return a matplotlib figure
def plot_purchase_amount_distribution():
    """
    Create a histogram showing the distribution of purchase amounts.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(customer_df["PurchaseAmount"], bins=25, alpha=0.8)

    ax.set_title("Distribution of Purchase Amounts")
    ax.set_xlabel("Purchase Amount ($)")
    ax.set_ylabel("Frequency")
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return fig

# 5.2 Create a pie chart showing sales breakdown by price tier
# REQUIRED: Function must create and return a matplotlib figure
def plot_sales_by_price_tier():
    """
    Create a pie chart showing the breakdown of sales by price tier.
    REQUIRED: Return the figure object
    """
    tier_order = ["Budget", "Mid-range", "Premium"]
    tier_sales = customer_df.groupby("PriceTier")["PurchaseAmount"].sum().reindex(tier_order)

    explode = [0.1 if tier == tier_sales.idxmax() else 0 for tier in tier_sales.index]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(tier_sales.values,
           labels=tier_sales.index,
           autopct='%1.1f%%',
           startangle=90,
           explode=explode,
           shadow=True)

    ax.set_title("Sales Breakdown by Price Tier")
    return fig


# TODO 6: Market Share Analysis
# 6.1 Create a pie chart showing sales breakdown by category
# REQUIRED: Function must create and return a matplotlib figure
def plot_category_market_share():
    """
    Create a pie chart showing the market share of each product category.
    REQUIRED: Return the figure object
    """
    category_sales = sales_df.groupby("Category")["Sales"].sum().reindex(categories)

    explode = [0.1 if category == category_sales.idxmax() else 0 for category in category_sales.index]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(category_sales.values,
           labels=category_sales.index,
           autopct='%1.1f%%',
           startangle=90,
           explode=explode,
           shadow=True)

    ax.set_title("Market Share by Product Category")
    return fig

# 6.2 Create a pie chart showing sales breakdown by location
# REQUIRED: Function must create and return a matplotlib figure
def plot_location_sales_distribution():
    """
    Create a pie chart showing the distribution of sales across different store locations.
    REQUIRED: Return the figure object
    """
    location_sales = sales_df.groupby("Location")["Sales"].sum().reindex(locations)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(location_sales.values,
           labels=location_sales.index,
           autopct='%1.1f%%',
           startangle=90,
           shadow=True)

    ax.set_title("Sales Distribution by Location")
    return fig


# TODO 7: Comprehensive Dashboard
# REQUIRED: Function must create and return a matplotlib figure with at least 4 subplots
def create_business_dashboard():
    """
    Create a comprehensive dashboard with multiple subplots highlighting key business insights.
    REQUIRED: Return the figure object with at least 4 subplots
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    quarterly_sales = sales_df.groupby("QuarterLabel")["Sales"].sum()
    axes[0, 0].plot(quarterly_sales.index, quarterly_sales.values, marker='o', linewidth=2)
    axes[0, 0].set_title("Overall Sales Trend")
    axes[0, 0].set_xlabel("Quarter")
    axes[0, 0].set_ylabel("Sales ($)")
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(True, alpha=0.3)

    location_totals = sales_df.groupby("Location")["Sales"].sum().reindex(locations)
    axes[0, 1].bar(location_totals.index, location_totals.values)
    axes[0, 1].set_title("Total Sales by Location")
    axes[0, 1].set_xlabel("Location")
    axes[0, 1].set_ylabel("Sales ($)")
    axes[0, 1].grid(axis='y', alpha=0.3)

    axes[1, 0].scatter(sales_df["AdSpend"], sales_df["Sales"], alpha=0.7)
    axes[1, 0].set_title("Ad Spend vs Sales")
    axes[1, 0].set_xlabel("Ad Spend ($)")
    axes[1, 0].set_ylabel("Sales ($)")
    axes[1, 0].grid(True, alpha=0.3)

    category_sales = sales_df.groupby("Category")["Sales"].sum().reindex(categories)
    axes[1, 1].pie(category_sales.values, labels=category_sales.index, autopct='%1.1f%%', startangle=90)
    axes[1, 1].set_title("Category Market Share")

    fig.suptitle("SunCoast Retail Business Dashboard", fontsize=16)
    plt.tight_layout()
    return fig


# Main function to execute all visualizations
# REQUIRED: Do not modify this function name
def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)

    # REQUIRED: Call all visualization functions and store figures
    # Store each figure in a variable for potential saving/display

    # Time Series Analysis
    fig1 = plot_quarterly_sales_trend()
    fig2 = plot_location_sales_comparison()

    # Categorical Comparison
    fig3 = plot_category_performance_by_location()
    fig4 = plot_sales_composition_by_location()

    # Relationship Analysis
    fig5 = plot_ad_spend_vs_sales()
    fig6 = plot_ad_efficiency_over_time()

    # Distribution Analysis
    fig7 = plot_customer_age_distribution()
    fig8 = plot_purchase_by_age_group()

    # Sales Distribution
    fig9 = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()

    # Market Share Analysis
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()

    # Comprehensive Dashboard
    fig13 = create_business_dashboard()

    # REQUIRED: Add business insights summary
    print("\nKEY BUSINESS INSIGHTS:")
    print("- Overall sales trend upward across the two-year period, with the strongest results in Q4, showing clear seasonal demand.")
    print("- Miami appears to be the top-performing location, while Jacksonville tends to be the weakest overall performer.")
    print("- Electronics hold the largest market share, making them the strongest revenue driver.")
    print("- Advertising spend has a positive relationship with sales, suggesting marketing contributes to revenue growth.")
    print("- Advertising efficiency changes over time, meaning some quarters generate stronger returns on ad spending.")
    print("- Customer age distributions vary by location, so local demographic differences matter.")
    print("- Mid-range products make up the largest share of purchase value, while premium items form a smaller but important segment.")
    print("- Purchase behavior differs across age groups, which suggests opportunities for more targeted promotions.")

    print("\nRECOMMENDATIONS:")
    print("- Increase investment in top-performing categories such as Electronics.")
    print("- Study Miami’s sales strategy and apply similar ideas in weaker locations.")
    print("- Prepare extra inventory and advertising support before Q4 to maximize seasonal demand.")
    print("- Shift advertising budget toward periods and locations with better efficiency.")
    print("- Tailor promotions and product mix to the age profile of each store location.")

    # Display all figures
    plt.show()

# Run the main function
if __name__ == "__main__":
    main()