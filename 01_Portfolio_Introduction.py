import streamlit as st
from pathlib import Path

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "pages" / "styles" / "main.css"

# load css
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

st.markdown("# Portfolio Introduction")
st.markdown('''
Hello, I am Isaac Kerson. I am a Data Analyst candidate skilled in advanced data analytics, ETL pipelines, and building machine learning models for decision making systems. I am proficient in Python, SQL, Scikit-learn, and Keras. I have experience researching and developing ML prototypes at an industry-leading master data company, implementing analytics engineering projects at a large university, and leading teams. I am currently working as a Lead Data Analytics Engineer at Stibo Systems. I will receive a Master of Science in Analytics from Georgia Institute of Technology in December, 2022.

This is my portfolio site. It contains my sample projects and resume. The first project is a synthetic data generator. Users can upload real datasets, select a data generation algorithm, create synthetic data, and review the caliber of the fake records with visualizations and quality metrics. Synthetic tabular data has important applications for training machine learning models when data collection is hindered by privacy or proprietary concerns or is unavailable or too expensive to collect. 

The second project is a vocabulary test maker. Users can input target words and sample sentences are retrieved via API calls and NoSQL database queries. Users can select and edit the sample sentences and share the finished tests via html links. The tests are automatically graded and test-takers receive instant feedback on their performance. MongoDB and Python are used on the backend for all create, read, update and delete (CRUD) operations. This type of automated teaching tool has the potential to streamline the clerical work involved in teaching and give instructors more time to focus on student international and engagement.

Thank you for visiting the site. You can contact me on [LinkedIn](https://www.linkedin.com/in/isaackerson/).

Best regards, 

Isaac

''')
st.sidebar.markdown("# Welcome")
st.sidebar.markdown("This site contains my sample projects and resume.")