import streamlit as st
import pandas as pd
import numpy as np
import requests

st.set_page_config(
    page_title="InsightPilot AI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 InsightPilot AI")
st.write("Upload Excel or CSV data to generate advanced analytics and AI insights.")

uploaded_file = st.file_uploader("Upload dataset", type=["csv","xlsx"])


def generate_ai_response(prompt):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"API Error: {response.text}"


if uploaded_file:

    try:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("Dataset Preview")
        st.dataframe(df.head())

        measures = df.select_dtypes(include="number").columns.tolist()
        dimensions = df.select_dtypes(exclude="number").columns.tolist()

        col1, col2, col3 = st.columns(3)

        col1.metric("Rows", len(df))
        col2.metric("Columns", len(df.columns))
        col3.metric("Measures", len(measures))

        st.subheader("Measures")
        st.write(measures)

        st.subheader("Dimensions")
        st.write(dimensions)

        numeric_df = df[measures]

        # ----------------------------
        # KPI Detection
        # ----------------------------

        st.subheader("Detected KPIs")

        kpi_data = {}

        for col in measures:
            kpi_data[col] = {
                "Total": numeric_df[col].sum(),
                "Average": numeric_df[col].mean(),
                "Max": numeric_df[col].max(),
                "Min": numeric_df[col].min()
            }

        kpi_df = pd.DataFrame(kpi_data).T.round(2)

        st.dataframe(kpi_df)

        # ----------------------------
        # Anomaly Detection
        # ----------------------------

        st.subheader("Anomaly Detection")

        anomalies = {}

        for col in measures:

            mean = numeric_df[col].mean()
            std = numeric_df[col].std()

            upper = mean + 3 * std
            lower = mean - 3 * std

            anomaly_rows = numeric_df[(numeric_df[col] > upper) | (numeric_df[col] < lower)]

            anomalies[col] = len(anomaly_rows)

        anomaly_df = pd.DataFrame(list(anomalies.items()), columns=["Measure", "Anomaly Count"])

        st.dataframe(anomaly_df)

        # ----------------------------
        # Trend Analysis
        # ----------------------------

        st.subheader("Trend Analysis")

        trends = {}

        for col in measures:

            series = numeric_df[col].dropna()

            if len(series) > 5:

                trend = np.polyfit(range(len(series)), series, 1)[0]

                if trend > 0:
                    trends[col] = "Increasing Trend"
                elif trend < 0:
                    trends[col] = "Decreasing Trend"
                else:
                    trends[col] = "Stable"

        trend_df = pd.DataFrame(list(trends.items()), columns=["Measure", "Trend"])

        st.dataframe(trend_df)

        # ----------------------------
        # Forecasting
        # ----------------------------

        st.subheader("Simple Forecast")

        forecast_data = {}

        for col in measures:

            series = numeric_df[col].dropna()

            if len(series) > 5:

                coef = np.polyfit(range(len(series)), series, 1)

                next_value = coef[0] * (len(series)+1) + coef[1]

                forecast_data[col] = round(next_value,2)

        forecast_df = pd.DataFrame(list(forecast_data.items()), columns=["Measure", "Forecast Next Value"])

        st.dataframe(forecast_df)

        # ----------------------------
        # AI Insights
        # ----------------------------

        if st.button("Generate Advanced AI Insights"):

            prompt = f"""
            You are a senior data analyst.

            Dataset columns:
            Dimensions: {dimensions}
            Measures: {measures}

            KPI Table:
            {kpi_df.to_string()}

            Trend Analysis:
            {trend_df.to_string()}

            Anomaly Detection:
            {anomaly_df.to_string()}

            Forecast:
            {forecast_df.to_string()}

            Provide:

            1. Advanced business insights
            2. Key performance drivers
            3. Risks or anomalies
            4. Strategic recommendations
            5. Fact and Measure table
            """

            insights = generate_ai_response(prompt)

            st.subheader("Advanced AI Insights")

            st.write(insights)

        # ----------------------------
        # Chat with Dataset
        # ----------------------------

        st.subheader("Ask Questions About Your Data")

        question = st.text_input("Enter your question")

        if st.button("Ask AI") and question:

            prompt = f"""
            Dataset KPIs:
            {kpi_df.to_string()}

            Trends:
            {trend_df.to_string()}

            Forecast:
            {forecast_df.to_string()}

            User Question:
            {question}
            """

            answer = generate_ai_response(prompt)

            st.write(answer)

    except Exception as e:

        st.error(f"Error processing dataset: {e}")

else:

    st.info("Upload a dataset to start analysis.")
