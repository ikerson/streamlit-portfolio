import streamlit as st
from pathlib import Path
import requests
import pandas as pd
from sdv.tabular import GaussianCopula, CTGAN, TVAE
from sdv.evaluation import evaluate
from timeit import default_timer as timer
from table_evaluator import TableEvaluator
from table_evaluator import viz

st.set_page_config(page_icon="📈")
st.set_option('deprecation.showPyplotGlobalUse', False)

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"

# load css
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

if "dataset_url" not in st.session_state:
    st.session_state.dataset_url = None
if "csv_data" not in st.session_state:
    st.session_state.csv_data = None
if "real_data" not in st.session_state:
    st.session_state.real_data = None
if "model_selection" not in st.session_state:
      st.session_state.model_selection = None
if "num_rows" not in st.session_state:
    st.session_state.num_rows = None
if "model" not in st.session_state:
    st.session_state.model = None
if "synth_data" not in st.session_state:
    st.session_state.synth_data = None
if "gen_time" not in st.session_state:
    st.session_state.gen_time = None
if "plot_selection" not in st.session_state:
    st.session_state.plot_selection = None

def synth_gen():
    if st.session_state.model_selection == "GaussianCopula":
        st.session_state.model = GaussianCopula()
    if st.session_state.model_selection == "CTGAN":
        st.session_state.model = CTGAN()
    if st.session_state.model_selection == "TVAE":
        st.session_state.model = TVAE()
    start = timer()
    st.session_state.model.fit(st.session_state.real_data)
    st.session_state.synth_data = st.session_state.model.sample(st.session_state.num_rows)
    end = timer()
    st.session_state.gen_time = end - start

# def clear_session():
#     st.session_state.real_data = None
#     st.session_state.csv_data = None
#     st.session_state.dataset_url = None

st.markdown("# Synthetic Data Generator")
st.sidebar.markdown("# Synthetic Data Generator")
st.sidebar.markdown("Generate synthetic data by uploading a dataset or providing a URL to a dataset. Select a model and number of rows to generate. The app will generate the synthetic data, display the results, and provide quality metrics.")

st.session_state.dataset_url = st.text_input("Enter the URL of the dataset.")

if st.session_state.dataset_url:
    if st.session_state.dataset_url.endswith(".csv"):
        st.success("Downloading dataset...")
        response = requests.get(st.session_state.dataset_url)
        if response.status_code == 200:
            st.success("Starting connection...")
            size = requests.get(st.session_state.dataset_url, stream=True).headers['Content-length']
            if size and int(size) < 2e+8:
                st.success("Reading file...")
                try:
                    st.session_state.real_data = pd.read_csv(st.session_state.dataset_url)
                    st.success("File read successfully.")
                except IOError as e:
                    st.error("Error:", e)
            else:
                st.write("Dataset is {size} bytes. This is too large process.")
        else: 
            st.warning(f"Server responded with {response.status_code} status code. Please check the url and try again.")
    else:
        st.warning("The URL must end in .csv")
st.session_state.csv_data = st.file_uploader("Upload a CSV file.", type=["csv"])

if st.session_state.csv_data:
    st.success("File uploaded successfully.")
    try:
        st.session_state.real_data = pd.read_csv(st.session_state.csv_data)
        st.success("File read successfully.")
    except IOError as e:
        st.exception("Error:", e)

if st.session_state.real_data is None:
    st.warning("Please upload a dataset.")
elif isinstance(st.session_state.real_data, pd.DataFrame) and st.session_state.real_data.shape[0] > 0:
    st.write(f"Dataset has {st.session_state.real_data.shape[0]} rows and {st.session_state.real_data.shape[1]} columns.")
    st.dataframe(st.session_state.real_data)
    if st.session_state.real_data.shape[0] > 10000:
        st.warning("Due to limited resources, synthetic data will only be generated for the first 10,000 rows.")
    st.markdown("## Generate Synthetic Data")
    st.markdown("#### Select the model to generate synthetic data.")
    st.table(pd.DataFrame({'Model': ['GaussianCopula Model', 'TVAE', 'CTGAN Model'], 
            "Description": ["Statistical mode that uses Gaussian copulas to model the joint distributions to synthesize the data",
            "Variational autoencoder Deep Learning synthesizer",
            "Generative adversarial network deep learning synthesizer"]}, index=[1,2,3]))
    st.number_input("Number of rows", min_value=1, max_value=10000, value=10000, key='num_rows')
    st.selectbox("Select one", ["GaussianCopula", "TVAE", "CTGAN"], on_change=synth_gen, key='model_selection')
else:
    st.warning("Pandas could not read the csv file.")

if st.session_state.real_data is not None and st.session_state.model_selection is not None:
    st.markdown(f"### Synthetic Data generated with {st.session_state.model_selection} model.")
    st.dataframe(st.session_state.synth_data)
    st.write(f"{st.session_state.synth_data.shape[0]} records generated in {st.session_state.gen_time:.2f} seconds.")
    st.markdown(f"### Report")
    eval_df = evaluate(st.session_state.synth_data, 
                st.session_state.real_data, 
                metrics=['CSTest', 'KSComplement', 'ContinuousKLDivergence', 'DiscreteKLDivergence'], 
                aggregate=False)
    st.dataframe(eval_df[["name","raw_score","min_value","max_value", "goal"]].dropna(subset = ['raw_score']))
    eval_model = TableEvaluator(st.session_state.real_data, st.session_state.synth_data)
    st.markdown(f"### Visualizations")
    st.selectbox("Select comparision plot", ["Mean and Standard Diviation", "Distribution Plots", "PCA Plots"], key='plot_selection')

    if st.session_state.plot_selection == "Mean and Standard Diviation":
        st.pyplot(eval_model.plot_mean_std(rplt=True))
    elif st.session_state.plot_selection == "Distribution Plots":
        st.pyplot(eval_model.plot_distributions(rplt=True))
    elif st.session_state.plot_selection == "PCA Plots":
        st.pyplot(eval_model.plot_pca(rplt=True))

# # st.button("Clear Session", on_click=clear_session)        
    
