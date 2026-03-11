import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="InsightPilot AI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 InsightPilot AI")
st.write("Upload Excel or CSV data to generate AI insights.")

uploaded_file = st.file_uploader("Upload dataset", type=["csv","xlsx"])

def generate_ai_response(prompt):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
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

        col1, col2, col3 = st.columns(3)

        col1.metric("Rows", len(df))
        col2.metric("Columns", len(df.columns))
        col3.metric(
            "Numeric Columns",
            len(df.select_dtypes(include="number").columns)
        )

        st.subheader("Dataset Summary")

        summary = df.describe(include="all")
        st.dataframe(summary)

        if st.button("Generate AI Insights"):

            prompt = f"""
            You are a data analyst.

            Dataset summary:
            {summary.to_string()}

            Provide:
            - Key insights
            - Trends
            - Business recommendations
            """

            insights = generate_ai_response(prompt)

            st.subheader("AI Insights")

            st.write(insights)

        st.subheader("Ask Questions About Your Data")

        user_question = st.text_input("Enter your question")

        if st.button("Ask AI") and user_question:

            prompt = f"""
            Dataset summary:
            {summary.to_string()}

            User question:
            {user_question}

            Answer based on the dataset.
            """

            answer = generate_ai_response(prompt)

            st.subheader("AI Answer")

            st.write(answer)

    except Exception as e:

        st.error(f"Error processing dataset: {e}")

else:

    st.info("Upload a dataset to start analysis.")
