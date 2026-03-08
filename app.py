import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

st.title("AI Insight Dashboard")

st.write("Upload Excel or CSV dataset to generate charts and AI insights.")

uploaded_file = st.file_uploader("Upload dataset", type=["csv", "xlsx"])

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

        if st.button("Generate AI Insights"):

            try:

                dataset_sample = df.head(20).to_string()

                prompt = f"""
                Analyze the dataset below and provide business insights.

                Dataset:
                {dataset_sample}

                Provide:
                1. Key insights
                2. Trends in the data
                3. Business recommendations
                """

                url = "https://api.groq.com/openai/v1/chat/completions"

                headers = {
                    "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
                    "Content-Type": "application/json"
                }

                data = {
                    "model": "llama3-8b-8192",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }

                response = requests.post(url, headers=headers, json=data)

                result = response.json()

                st.subheader("AI Analysis")

                st.write(result["choices"][0]["message"]["content"])

            except Exception:
                st.error("AI service temporarily unavailable. Please try again later.")

    except Exception:
        st.error("Unable to process this dataset. Please upload a valid Excel or CSV file.")
