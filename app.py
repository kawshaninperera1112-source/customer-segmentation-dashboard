
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="Customer Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown("""
<style>

    .main {
        background-color: #F8FAFC;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .dashboard-title {
        font-size: 32px;
        font-weight: 700;
        color: #0F172A;
    }

    .dashboard-subtitle {
        color: #64748B;
        font-size: 15px;
        margin-bottom: 25px;
    }

    .metric-card {
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        min-height: 120px;
    }

    .metric-label {
        color: #64748B;
        font-size: 14px;
    }

    .metric-value {
        color: #0F172A;
        font-size: 28px;
        font-weight: 700;
    }

    .section-title {
        color: #0F172A;
        font-size: 21px;
        font-weight: 600;
        margin-top: 25px;
    }

</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv("customer_segmentation.csv")

# -----------------------------
# HEADER
# -----------------------------

st.markdown(
    '<div class="dashboard-title">Customer Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Understand your customers and make smarter marketing decisions.'
    '</div>',
    unsafe_allow_html=True
)

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------

st.sidebar.title("Dashboard Filters")

st.sidebar.markdown(
    "Use the filters to explore customer segments."
)

selected_cluster = st.sidebar.selectbox(
    "Select Customer Segment",
    ["All"] + sorted(df["Cluster"].unique().tolist())
)

age_range = st.sidebar.slider(
    "Age Range",
    int(df["Age"].min()),
    int(df["Age"].max()),
    (
        int(df["Age"].min()),
        int(df["Age"].max())
    )
)

income_range = st.sidebar.slider(
    "Annual Income (k$)",
    int(df["Annual Income (k$)"].min()),
    int(df["Annual Income (k$)"].max()),
    (
        int(df["Annual Income (k$)"].min()),
        int(df["Annual Income (k$)"].max())
    )
)

# -----------------------------
# FILTER DATA
# -----------------------------

filtered_df = df[
    (df["Age"] >= age_range[0]) &
    (df["Age"] <= age_range[1]) &
    (df["Annual Income (k$)"] >= income_range[0]) &
    (df["Annual Income (k$)"] <= income_range[1])
]

if selected_cluster != "All":
    filtered_df = filtered_df[
        filtered_df["Cluster"] == selected_cluster
    ]

# -----------------------------
# SUMMARY CARDS
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Total Customers</div>
            <div class="metric-value">{len(filtered_df)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Customer Segments</div>
            <div class="metric-value">
                {filtered_df["Cluster"].nunique()}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    avg_income = filtered_df["Annual Income (k$)"].mean()

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Average Income</div>
            <div class="metric-value">{avg_income:.2f}k</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    avg_spending = filtered_df["Spending Score (1-100)"].mean()

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Average Spending</div>
            <div class="metric-value">{avg_spending:.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# CHARTS
# -----------------------------

st.markdown(
    '<div class="section-title">Customer Insights</div>',
    unsafe_allow_html=True
)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:

    st.subheader("Customer Segment Distribution")

    segment_counts = (
        filtered_df["Cluster"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    segment_counts.columns = ["Cluster", "Customers"]

    fig_bar = px.bar(
        segment_counts,
        x="Cluster",
        y="Customers",
        color="Cluster",
        title="Customers by Segment"
    )

    fig_bar.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

with chart_col2:

    st.subheader("Income vs Spending Score")

    fig_scatter = px.scatter(
        filtered_df,
        x="Annual Income (k$)",
        y="Spending Score (1-100)",
        color="Cluster",
        hover_data=["CustomerID", "Age", "Genre"],
        title="Customer Segments"
    )

    fig_scatter.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )

# -----------------------------
# CLUSTER SUMMARY
# -----------------------------

st.markdown(
    '<div class="section-title">Segment Summary</div>',
    unsafe_allow_html=True
)

summary = df.groupby("Cluster")[
    [
        "Age",
        "Annual Income (k$)",
        "Spending Score (1-100)"
    ]
].mean().round(2)

st.dataframe(
    summary,
    use_container_width=True
)

# -----------------------------
# CUSTOMER DETAILS
# -----------------------------

st.markdown(
    '<div class="section-title">Customer Details</div>',
    unsafe_allow_html=True
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# DOWNLOAD DATA
# -----------------------------

csv_data = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Customer Data",
    data=csv_data,
    file_name="filtered_customers.csv",
    mime="text/csv"
)
