import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Financial Chatbot", layout="wide")

# Load the dataset
df = pd.read_csv("combined_financial_data.csv")

# Main Title
st.title("💬 Financial Chatbot Prototype")
st.markdown("Welcome to the AI-powered financial assistant. Select a company, fiscal year, and ask a predefined question to get instant insights.")

# Sidebar for selections
with st.sidebar:
    st.header("🔍 Filter Options")
    selected_company = st.selectbox("🏢 Select a Company", sorted(df['Company'].unique()))
    selected_year = st.selectbox("📅 Select a Fiscal Year", sorted(df[df['Company'] == selected_company]['Fiscal Year'].unique(), reverse=True))

# Chatbot Function
def simple_chatbot(company, year, user_query):
    try:
        record = df[(df['Company'].str.lower() == company.lower()) & (df['Fiscal Year'] == int(year))].iloc[0]
    except IndexError:
        return "❌ Sorry, data not found for that company and year."

    if user_query == "What is the total revenue?":
        return f"💰 The total revenue is **${record['Total Revenue']:,}**."

    elif user_query == "How has net income changed over the last year?":
        previous_year = int(year) - 1
        try:
            prev_record = df[(df['Company'].str.lower() == company.lower()) & (df['Fiscal Year'] == previous_year)].iloc[0]
            change = int(record['Net Income']) - int(prev_record['Net Income'])
            direction = "increased" if change >= 0 else "decreased"
            return f"📈 The net income has **{direction} by ${abs(change):,}** compared to the previous year."
        except IndexError:
            return "⚠️ No previous year data available for comparison."

    elif user_query == "What are the total assets?":
        return f"🏦 The total assets are **${record['Total Assets']:,}**."

    elif user_query == "What are the total liabilities?":
        return f"📉 The total liabilities are **${record['Total Liabilities']:,}**."

    elif user_query == "What is the operating cash flow?":
        return f"💼 The operating cash flow is **${record['Operating Cash Flow']:,}**."

    else:
        return "❌ Sorry, I can only answer predefined questions."

# User selects a predefined question
queries = [
    "What is the total revenue?",
    "How has net income changed over the last year?",
    "What are the total assets?",
    "What are the total liabilities?",
    "What is the operating cash flow?"
]
selected_query = st.selectbox("💬 Ask a financial question:", queries)

# Submit button
if st.button("Ask"):
    st.markdown("---")
    st.subheader("🤖 Chatbot Response")
    response = simple_chatbot(selected_company, selected_year, selected_query)
    st.success(response)

# Optional: Financial Trend Chart
st.markdown("---")
with st.expander("📊 Show Financial Trends Over Time"):
    company_data = df[df['Company'].str.lower() == selected_company.lower()].sort_values("Fiscal Year")
    if not company_data.empty:
        chart_data = company_data[["Fiscal Year", "Total Revenue", "Net Income", "Total Assets", "Total Liabilities", "Operating Cash Flow"]]
        chart_data = chart_data.set_index("Fiscal Year")

        st.line_chart(chart_data)

        # Bar chart using matplotlib
        st.markdown("### 🔍 Metric Comparison (Bar Chart)")
        fig, ax = plt.subplots(figsize=(10, 4))
        chart_data.plot(kind='bar', ax=ax)
        st.pyplot(fig)
    else:
        st.warning("No historical data available to plot.")
