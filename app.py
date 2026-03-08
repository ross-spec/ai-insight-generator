import streamlit as st
import pandas as pd

st.title("AI Insight Generator")

st.write("Upload your Excel or CSV dataset and get insights.")

uploaded_file = st.file_uploader("Upload dataset", type=["csv","xlsx"])

if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write("Dataset Preview")
    st.dataframe(df.head())

    if st.button("Generate Insights"):

        st.subheader("Insights")

        st.write("• Identify trends in your dataset")
        st.write("• Analyze top performing categories")
        st.write("• Check seasonal patterns")
