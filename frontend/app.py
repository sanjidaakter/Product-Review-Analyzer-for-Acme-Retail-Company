import streamlit as st
import pandas as pd
import requests

st.title("🛒 Acme Product Review Analyzer")

# File uploader
uploaded_file = st.file_uploader("Upload CSV file with product reviews", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    results = []

    with st.spinner("Analyzing reviews..."):
        for _, row in df.iterrows():
            review_text = row["review_text"]
            try:
                res = requests.post(
                    "http://localhost:8000/analyze/", data={"text": review_text}
                )
                data = res.json()
                results.append(
                    {
                        "product_name": row["product_name"],
                        "review_text": review_text,
                        **data,
                    }
                )
            except Exception as e:
                results.append(
                    {
                        "product_name": row["product_name"],
                        "review_text": review_text,
                        "sentiment": "error",
                        "topic": "error",
                        "error": str(e),
                    }
                )

    result_df = pd.DataFrame(results)
    st.success("Analysis complete!")

    # Display DataFrame
    st.dataframe(result_df)

    # Download button
    st.download_button(
        label="Download Results as CSV",
        data=result_df.to_csv(index=False),
        file_name="analyzed_reviews.csv",
        mime="text/csv",
    )

    # Sentiment distribution
    st.subheader("📊 Sentiment Distribution")
    if "sentiment" in result_df.columns:
        st.bar_chart(result_df["sentiment"].value_counts())

    # Topic distribution
    st.subheader("📌 Top Topics")
    if "topic" in result_df.columns:
        st.bar_chart(result_df["topic"].value_counts())
