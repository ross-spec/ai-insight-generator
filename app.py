import streamlit as st
import pandas as pd
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="InsightPilot AI",
    page_icon="📊",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

h1, h2, h3 {
    color: white;
}

.stButton>button {
    background-color: #6366f1;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
}

</style>
""", unsafe_allow_html=True)

# Configure Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

# Sidebar navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "AI Insights", "Chat With Data"]
)

# Header
st.title("📊 InsightPilot AI")
st.write("Turn your Excel data into smart AI insights.")

uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["csv", "xlsx"])

if uploaded_file:

    try:

        # Load dataset
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Dashboard Page
        if page == "Dashboard":

            st.subheader("Dataset Preview")
            st.dataframe(df.head())

            st.subheader("Dataset Statistics")

            col1, col2, col3 = st.columns(3)

            col1.metric("Rows", len(df))
            col2.metric("Columns", len(df.columns))
            col3.metric(
                "Numeric Fields",
                len(df.select_dtypes(include='number').columns)
            )

        # AI Insights Page
        elif page == "AI Insights":

            st.subheader("Generate AI Insights")

            if st.button("Generate Insights"):

                dataset_sample = df.head(25).to_string()

                prompt = f"""
                You are a professional data analyst.

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

        # Chat With Data Page
        elif page == "Chat With Data":

            st.subheader("Ask Questions About Your Dataset")

            question = st.text_input("Ask something about the data")

            if st.button("Ask AI") and question:

                dataset_sample = df.head(30).to_string()

                prompt = f"""
                Dataset:
                {dataset_sample}

                User question:
                {question}

                Answer based on the dataset.
                """

                response = model.generate_content(prompt)

                st.subheader("AI Answer")

                st.write(response.text)

    except Exception as e:

        st.error(f"Error processing dataset: {e}")

else:

    st.info("Please upload a dataset to begin.")
