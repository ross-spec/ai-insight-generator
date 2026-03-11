import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

st.title("AI Insight Dashboard")

st.write("Upload Excel or CSV dataset to generate charts and AI insights.")

uploaded_file = st.file_uploader("Upload dataset", type=["csv","xlsx"])

if uploaded_file:

    try:

        # Load dataset
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("Dataset Preview")
        st.dataframe(df.head())

        # Detect numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns

        if len(numeric_cols) > 0:

            st.subheader("Automatic Charts")

            for col in numeric_cols:
                fig, ax = plt.subplots()
                df[col].plot(kind="line", ax=ax)
                ax.set_title(f"{col} Trend")
                st.pyplot(fig)

        # AI Insights
        if st.button("Generate AI Insights"):

            dataset_sample = df.head(20).to_string()

            prompt = f"""
            You are a data analyst.

            Analyze the dataset below and provide:

            1. Key insights
            2. Important trends
            3. Business recommendations

            Dataset:
            {dataset_sample}
            """

            response = model.generate_content(prompt)

            st.subheader("AI Insights")

            st.write(response.text)

        # Chat with dataset
        st.subheader("Ask Questions About Your Dataset")

        user_question = st.text_input("Ask something about the data")

        if st.button("Ask AI") and user_question:

            dataset_sample = df.head(30).to_string()

            chat_prompt = f"""
            Dataset:
            {dataset_sample}

            User question:
            {user_question}

            Answer clearly based on the dataset.
            """

            response = model.generate_content(chat_prompt)

            st.subheader("AI Answer")

            st.write(response.text)

    except Exception as e:

        st.error(f"Error processing dataset: {e}")
