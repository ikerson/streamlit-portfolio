import streamlit as st
import requests
import pandas as pd
import timeit

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
            st.warning(f"Server responded with {response.status_code} status code. Please check the url and try again.")
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

if df is None:
    st.warning("Please upload a dataset.")
elif isinstance(df, pd.DataFrame) and df.shape[0] > 0:
    st.write(f"Dataset has {df.shape[0]} rows and {df.shape[1]} columns.")
    st.dataframe(df)
    if df.shape[0] > 10000:
        st.warning("Due to limited resources, synthetic data will only be generated for the first 10,000 rows.")
    st.markdown("## Generate Synthetic Data")
    st.markdown("#### Select the model to generate synthetic data.")
    st.table(pd.DataFrame({'Model': ['GaussianCopula Model', 'TVAE', 'CTGAN Model'], 
            "Description": ["Statistical mode that uses Gaussian copulas to model the joint distributions to synthesize the data",
            "Variational autoencoder Deep Learning synthesizer",
            "Generative adversarial network deep learning synthesizer"]}, index=[1,2,3]))
    model_selection = st.selectbox("Select one", ["GaussianCopula", "TVAE", "CTGAN"])
else:
    st.warning("Pandas could not read the csv file.")

if model_selection:
    if model_selection == "GaussianCopula":
        st.markdown("## GaussianCopula Model")
        st.markdown("#### Select the number of synthetic data to generate.")
        num_rows = st.number_input("Number of rows", min_value=1, max_value=10000, value=1000)
        if num_rows:
            st.success("Generating synthetic data...")
            from sdv.tabular import GaussianCopula
            model = GaussianCopula()
            model.fit(df)
            synthetic_data = model.sample(num_rows)
            st.success("Synthetic data generated successfully.")
            st.markdown("### Synthetic Data")
            st.dataframe(synthetic_data)
            st.markdown("### Report")
            st.dataframe(model.get_metadata())