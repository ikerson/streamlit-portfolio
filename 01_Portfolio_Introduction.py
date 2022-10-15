import streamlit as st
from pathlib import Path


st.set_page_config(page_icon="💬", page_title="Introduction")
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "pages" / "styles" / "main.css"

app_url = st.secrets.app_url
resume_path = app_url + 'Isaac_Kerson_Resume'
sdg_path = app_url + 'Synthetic_Data_Generator'
quiz_path = app_url + 'Quiz_Maker'

# load css
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

st.markdown(f''' 

## Introduction
Hello, I am Isaac Kerson. I am a Data Analyst candidate skilled in advanced data analytics, 
ETL pipelines, and building machine learning models for decision making systems. 

## Experience
I have experience researching and developing ML prototypes at an industry-leading master data company, 
implementing analytics engineering projects at a large university, and leading teams. 
I am proficient in Python, SQL, Scikit-learn, and Keras.
I am currently working as a Lead Data Analytics Engineer at Stibo Systems. 
I will receive a Master of Science in Analytics from Georgia Institute of Technology in December, 2022.
Learn more by reading my [resume]({resume_path}).

## Projects

### [Synthetic Data Generator]({sdg_path})
Upload real datasets, select deep learning or statistical data generation models, 
and create synthetic data. Judge the caliber of the fake records with visualizations 
and quality metrics and download the new synthetic data. Build with Python, Streamlit, 
Synthetic Data Vault library, and Matplotlib. 

### [Quiz Maker]({quiz_path})
Input target words and select sample sentences provided via API calls. 
Select and edit the selected sentences and share the link for the finalized quiz. 
Built with Python, Streamlit, API Requests library, and MongoDB.
''')

st.sidebar.markdown("# Welcome")
st.sidebar.markdown("Learn about my projects and experience here.")