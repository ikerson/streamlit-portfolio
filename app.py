from pathlib import Path
from PIL import Image
import streamlit as st

# path settings

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
resume_file = current_dir / "assets" / "cv.pdf"
profile_pic = current_dir / "assets" / "profile-pic.png"

# page settings
PAGE_TITLE = "Digital CV | Isaac Kerson"
PAGE_ICON = ":wave:"
NAME = "Isaac Kerson"
DESCRIPTION = """
Data Analyst candidate skilled in advanced data analytics, ETL pipelines, 
and building machine learning models for decision making systems. 
Proficient in Python, SQL, Scikit-learn, and Keras. 
Experience researching and developing ML prototypes at an industry-leading master data company,
implementing analytics engineering projects at a large university, and leading teams. 
"""
EMAIL = "ikerson3@gatech.edu"
SOCIAL_MEDIA = {
    "LinkedIn": "https://www.linkedin.com/in/isaackerson",
    "GitHub": "https://github.com/ikerson",
    "Twitter": "https://twitter.com/Isaac_Kerson",
}
PROJECTS = {
    "Consumer Electronics Classification -  Distributed random forest classification model for consumer electronics master data": "https://github.com/ikerson",
    "IT Ticketing Time Prediction - Deep learning model to predict service ticket completion time using system logs": "https://github.com/ikerson",
    "Auto Shop Database - Content Management System using PostgreSQL database and Flask": "https://github.com/ikerson",
}

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# load css, pdf, and profile picture
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
with open(resume_file, "rb") as pdf_file:
    PDFbyte = pdf_file.read()
profile_pic = Image.open(profile_pic)


# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="medium")
with col1:
    st.title(NAME)
    st.write(DESCRIPTION)
    st.download_button(
        label="Download Resume",
        data=PDFbyte,
        file_name=resume_file.name,
        mime="application/octet-stream",
    )
    st.write(EMAIL)

with col2:
    st.image(profile_pic, width=230)


# social links
st.write('\n')
cols = st.columns(len(SOCIAL_MEDIA))
for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    cols[index].write(f"[{platform}]({link})")


# --- SKILLS ---
st.write('\n')
st.subheader("Skills")
st.write(
"""
Advanced:, Python, SQL, Pandas, Sci-Kit Learn, Keras, Data Processing, Microsoft Office, Google Workspace, Jupyter Notebooks.
Proficient: Matplotlib, Seaborn, Plotly, Pyspark, MongoDB, PostgreSQL, Git, GitHub, Bash command line, VSCode, Azure.
Expert: Education, Written & Verbal Communication, Public Speaking, Data Analysis, Data Science.
"""
)

# --- Projects ---
st.write('\n')
st.subheader("Projects")
st.write("---")
for project, link in PROJECTS.items():
    st.write(f"[{project}]({link})")


# --- WORK HISTORY ---
st.write('\n')
st.subheader("Work History")
st.write("---")

# --- JOB 1
st.write("**Lead Data Analytics Engineer | Stibo Systems | Højbjerg, Denmark**")
st.write("August 2020 - Present")
st.write(
"""
Lead a team of three in researching and creating a synthetic data generation system and distributed 
random forest classification model for consumer electronics master data. 
Acceved 97% accuracy on validation data set. 
Presented findings to company management using Seaborn, Matplotlib, and PowerPoint. 
Handed off research to the internal data science team and saw our methodology incorporated into the company's master data management product.  
"""
)

# --- JOB 2
st.write('\n')
st.write("**Learning Analytics Team Lead & Assistant Professor | Gachon University | Seoul, South Korea**")
st.write("01/2018 - 02/2022")
st.write(
    """
- ► Built data models and maps to generate meaningful insights from customer data, boosting successful sales eﬀorts by 12%
- ► Modeled targets likely to renew, and presented analysis to leadership, which led to a YoY revenue increase of $300K
- ► Compiled, studied, and inferred large amounts of data, modeling information to drive auto policy pricing
"""
)

# --- JOB 3
st.write('\n')
st.write("🚧", "**Data Analyst | Chegg**")
st.write("04/2015 - 01/2018")
st.write(
    """
- ► Devised KPIs using SQL across company website in collaboration with cross-functional teams to achieve a 120% jump in organic traﬃc
- ► Analyzed, documented, and reported user survey results to improve customer communication processes by 18%
- ► Collaborated with analyst team to oversee end-to-end process surrounding customers' return data
"""
)


