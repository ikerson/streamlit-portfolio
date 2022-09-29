import streamlit as st
import requests
import pandas as pd

df = None

st.markdown("# Synthetic Data Generator")
st.sidebar.markdown("# Synthetic Data Generator")

st.markdown("## Introduction")
st.markdown("This is a simple app to generate synthetic data for a given dataset. The app uses the [SDGym](https://sdv.dev/SDGym/) library to generate synthetic data. The app is built using [Streamlit](https://streamlit.io/).")

st.markdown("## Usage")
st.markdown("To use the app, simply upload a dataset in CSV format. The app will automatically detect the delimiter and the column names. The app will then generate synthetic data for the dataset. The app will also generate a report of the synthetic data.")

url = st.text_input("Enter the URL of the dataset.")

if url:
    if url.endswith(".csv"):
        st.success("Downloading dataset...")
        response = requests.get(url)
        if response.status_code == 200:
            st.success("Starting connection...")
            size = requests.get(url, stream=True).headers['Content-length']
            if size and int(size) < 2e+8:
                st.success("Reading file...")
                try:
                    df = pd.read_csv(url)
                    st.success("File read successfully.")
                except IOError as e:
                    st.error("Error:", e)
            else:
                st.write("Dataset is {size} bytes. This is too large process.")
        else: 
            st.warning("Error:", response.status_code)
    else: 
        st.warning("URLs must end in .csv")

data = st.file_uploader("Upload a CSV file.")

if data:
    st.success("File uploaded successfully.")
    try:
        df = pd.read_csv(data)
        st.success("File read successfully.")
    except IOError as e:
        st.exception("Error:", e)

if isinstance(df, pd.DataFrame) and df.shape[0] > 0:
    st.write(f"Dataset has {df.shape[0]} rows and {df.shape[1]} columns.")
    st.dataframe(df)
    if df.shape[0] > 10000:
        st.warning("Due to limited resources, synthetic data will only be generated for the first 10,000 rows.")
    st.markdown("## Generate Synthetic Data")
    st.selectbox("Select a model to generate synthetic data.", ["CTGAN", "TVAE", "GaussianCopula"])
else:
    st.warning("Pandas could not read the csv file.")