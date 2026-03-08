import streamlit as st
import pandas as pd
from openai import OpenAI

st.title("AI Insight Generator")

st.write("Upload your Excel or CSV dataset and get AI-generated insights.")

uploaded_file = st.file_uploader("Upload dataset", type=["csv","xlsx"])

if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write("Dataset Preview")
    st.dataframe(df.head())

    if st.button("Generate Insights"):

        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        dataset_sample = df.head(20).to_string()

        prompt = f"""
        Analyze the dataset below and provide business insights.

        Dataset:
        {dataset_sample}

        Provide:
        1. Key insights
        2. Patterns or trends
        3. Recommendations
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        st.subheader("AI Insights")

        st.write(response.choices[0].message.content)
