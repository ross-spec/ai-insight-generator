import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI

st.title("AI Insight Dashboard")

st.write("Upload Excel or CSV dataset to generate charts and AI insights.")

uploaded_file = st.file_uploader("Upload dataset", type=["csv","xlsx"])

if uploaded_file:

    # Load data
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Detect numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns

    if len(numeric_cols) > 0:

        st.subheader("Automatic Data Visualization")

        for col in numeric_cols:

            fig, ax = plt.subplots()
            df[col].plot(kind="line", ax=ax)
            ax.set_title(f"{col} Trend")

            st.pyplot(fig)

    if st.button("Generate AI Insights"):

        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        dataset_sample = df.head(20).to_string()

        prompt = f"""
        Analyze the dataset below and provide business insights.

        Dataset:
        {dataset_sample}

        Provide:
        1. Key insights
        2. Trends in the data
        3. Recommendations
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )

        st.subheader("AI Analysis")

        st.write(response.choices[0].message.content)
