import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_lottie import st_lottie
import requests
import json
import io

# Function to load Lottie animation from URL
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    try:
        return r.json()
    except json.JSONDecodeError:
        return None

# Page Configuration
st.set_page_config(page_title="Shopping Trends Analyzer", page_icon="🛍️", layout="wide")

# Load a working Lottie animation (shopping themed)
lottie_url = "https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json"  
lottie_shopping = load_lottie_url(lottie_url)

# Title and Animation
st.title("🛍️ Shopping Trends Analyser")

if lottie_shopping:
    st_lottie(lottie_shopping, height=250, key="shopping")
else:
    st.warning("⚠️ Could not load the shopping animation.")

# File Uploader
uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])

if uploaded_file:
    try:
        data = pd.read_excel(uploaded_file)

        # Show Data Preview
        st.subheader("📄 Data Preview")
        st.dataframe(data.head())

         

        # --- SIDEBAR FILTERS ---
        st.sidebar.header("🔍 Filter Your Data")
        gender = st.sidebar.multiselect("Select Gender:", options=data["Gender"].unique(), default=data["Gender"].unique())
        age = st.sidebar.multiselect("Select Age:", options=data["Age"].unique(), default=data["Age"].unique())
        category = st.sidebar.multiselect("Select Category:", options=data["Category"].unique(), default=data["Category"].unique())

        filtered_df = data[
            (data["Gender"].isin(gender)) &
            (data["Age"].isin(age)) &
            (data["Category"].isin(category))
        ]

        st.subheader("📊 Filtered Data")
        st.write(f"Total Records: {len(filtered_df)}")
        st.dataframe(filtered_df.head())

        # --- Download Filtered Data ---
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Filtered Data as CSV", data=csv_data, file_name='filtered_shopping_data.csv', mime='text/csv')


        # Show Basic Statistics
        st.subheader("📊 Basic Statistics")
        st.write(data.describe())

        st.subheader("📈 Visualize a Column")
        cat_col = st.selectbox("Choose a column to visualize:", filtered_df.select_dtypes(include='object').columns)

        if cat_col:
            fig1, ax1 = plt.subplots()
            filtered_df[cat_col].value_counts().plot(kind='bar', ax=ax1, color='skyblue')
            ax1.set_title(f"Distribution of {cat_col}")
            ax1.set_ylabel("Count")
            plt.xticks(rotation=45)
            st.pyplot(fig1)

        # --- Pie Chart ---
        st.subheader("🧁 Pie Chart - Category Breakdown")
        if "Category" in filtered_df.columns:
            pie_data = filtered_df["Category"].value_counts()
            fig3, ax3 = plt.subplots()
            ax3.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
            ax3.axis('equal')
            st.pyplot(fig3)

        # --- Monthly Trend Chart ---
        st.subheader("📅 Monthly Shopping Trend")
        if "Purchase Date" in data.columns:
            data["Purchase Date"] = pd.to_datetime(data["Purchase Date"], errors='coerce')
            data['Month'] = data["Purchase Date"].dt.to_period("M").astype(str)
            monthly_trend = data.groupby("Month").size()

            fig2, ax2 = plt.subplots()
            monthly_trend.plot(kind='line', marker='o', ax=ax2, color='green')
            ax2.set_title("Monthly Shopping Trend")
            ax2.set_ylabel("Number of Purchases")
            plt.xticks(rotation=45)
            st.pyplot(fig2)
        else:
            st.info("ℹ️ 'Purchase Date' column not found for trend analysis.")
                    

        
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.info("👆 Upload your Excel file to get started!")

