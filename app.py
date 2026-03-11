import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(
    page_title="InsightPilot AI",
    page_icon="📊",
    layout="wide"
)

# Styling
st.markdown("""
<style>
.main {
    background-color: #0f172a;
}
h1,h2,h3 {
    color:white;
}
.stButton>button {
    background-color:#6366f1;
    color:white;
    border-radius:8px;
}
</style>
""", unsafe_allow_html=True)

# Configure Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-pro")

st.title("📊 InsightPilot AI")
st.write("Upload Excel or CSV to generate AI insights.")

uploaded_file = st.file_uploader("Upload dataset", type=["csv","xlsx"])

if uploaded_file:

    try:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("Dataset Preview")
        st.dataframe(df.head())

        # KPI metrics
        col1,col2,col3 = st.columns(3)

        col1.metric("Rows", len(df))
        col2.metric("Columns", len(df.columns))
        col3.metric(
            "Numeric Columns",
            len(df.select_dtypes(include="number").columns)
        )

        # Dataset statistics
        numeric_df = df.select_dtypes(include="number")

        if not numeric_df.empty:

            st.subheader("Numeric Summary")

            st.dataframe(numeric_df.describe())

        # AI Insights
        if st.button("Generate AI Insights"):

            summary = df.describe(include="all").to_string()

            columns = ", ".join(df.columns)

            prompt = f"""
            You are a professional data analyst.

            Dataset Columns:
            {columns}

            Dataset Summary Statistics:
            {summary}

            Provide:

            1. Key insights
            2. Important patterns
            3. Business recommendations
            4. Possible anomalies in the dataset
            """

            try:

                response = model.generate_content(prompt)

                st.subheader("AI Insights")

                st.write(response.text)

            except Exception as e:

                st.error(f"AI error: {e}")

        # Chat with data
        st.subheader("Chat With Your Dataset")

        question = st.text_input("Ask a question about the data")

        if st.button("Ask AI") and question:

            summary = df.describe(include="all").to_string()

            prompt = f"""
            Dataset Summary:
            {summary}

            User Question:
            {question}

            Answer based on dataset.
            """

            try:

                response = model.generate_content(prompt)

                st.write(response.text)

            except Exception as e:

                st.error(f"AI error: {e}")

    except Exception as e:

        st.error(f"Error processing dataset: {e}")
