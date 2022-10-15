from pathlib import Path
from PIL import Image
import streamlit as st

# path settings

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
resume_file = current_dir / "assets" / "cv.pdf"
profile_pic = current_dir / "assets" / "profile-pic.jpg"

app_url = st.secrets.app_url
sdg_path = app_url + 'Synthetic_Data_Generator'
quiz_path = app_url + 'Quiz_Maker'

# page settings
PAGE_TITLE = "Isaac Kerson | Resume"
PAGE_ICON = ":page_facing_up:"
PAGE_LAYOUT = "centered"
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
PROJECTS = [
    ("Synthetic Data Generator", sdg_path, "Upload real datasets, select deep learning or statistical data generation models, and create synthetic data. Judge the caliber of the fake records with visualizations and quality metrics and download the new synthetic data. Built with Python, Streamlit, Synthetic Data Vault library, and Matplotlib."),
    ("Quiz Maker", quiz_path, "Input target words and select sample sentences provided via API calls. Select and edit the sentences and share the link for the finalized quiz. Built with Python, Streamlit, API Requests library, and MongoDB."),
]
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=PAGE_LAYOUT)

# --- SOCIAL MEDIA LINKS ---
st.write('\n')
cols = st.columns(len(SOCIAL_MEDIA))
for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    cols[index].write(f"[{platform}]({link})")

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


# --- SKILLS ---
st.write('\n')
st.subheader("Skills")
st.write("**Advanced**: Python, SQL, Pandas, Sci-Kit Learn, Keras, Data Processing, Microsoft Office, Google Workspace, Jupyter Notebooks.")
st.write("**Proficient**: Matplotlib, Seaborn, Plotly, Pyspark, MongoDB, PostgreSQL, Git, GitHub, Bash command line, VSCode, Azure.")
st.write("**Expert**: Team Management, Education, Written & Verbal Communication, Public Speaking, Data Analysis, Data Science.")


# --- Projects ---
st.write('\n')
st.subheader("Projects")
st.write("---")
for project in PROJECTS:
    st.write(f"[{project[0]}]({project[1]}) - {project[2]}")


# --- WORK HISTORY ---
st.write('\n')
st.subheader("Work History")
st.write("---")

# --- JOB 1
st.markdown("**Lead Data Analytics Engineer**, Stibo Systems, Højbjerg, Denmark")
st.markdown("Present - August 2021")
st.write(
"""
Lead a team of three in researching and creating a synthetic data generation system and distributed 
random forest classification model for consumer electronics master data. 
Acceved 97% accuracy on validation data set. 
Presented findings to company management using Seaborn, Matplotlib, and PowerPoint. 
Handed off research to the internal data science team and saw our methodology incorporated into the company's master data management product.  
"""
)
st.write("---")

# --- JOB 2
st.markdown("**Learning Analytics Team Lead & Assistant Professor**, Gachon University, Seoul, South Korea")
st.markdown("September 2021 - January 2011")
st.write(
"""
Implemented, organized and led multiple Learning Analytics projects for the university's Global Language Center. 
Developed Python scripts for Google Classroom API calls for automated creation of classes, homework assignments, and announcements. 
Built and maintained end-to-end student grade management system in Google Sheets for importing student data, 
automatically ingesting assignment grades, flagging struggling students, calculating class-wide performance statistics 
and visualizualizating results in summary dashboard. Created a live, interactive, in-class activity tracking system 
by integrating student smartphones, Google Sheets, and Google Forms. The system provided students instant feedback on 
their learning and allowed teachers to adjust their lessons and instructional approach in real time. 
Trained colleagues as well as led product maintenance improvement over a ten-year period.
"""
)
st.write("---")

# --- JOB 3
st.markdown("**Grade Team Lead & English Language Arts Teacher**, University Neighborhood Middle School, New York, New York, USA")
st.markdown("July 2009 - July 2007")
st.write(
"""
Worked on a teacher-lead team to design and implement a real-time student attendance system using Google Sheets. 
Led seventh grade team in reviewing student academic, behavioral, and attendance data to plan student interventions and curriculum improvements. 
Received formal Letter of Accommodation from Principal for accomplishments as team
"""
)
st.write("---")

# --- Education & Certificates ---
st.write('\n')
st.subheader("Education & Certificates")
st.write("GEORGIA INSTITUTE OF TECHNOLOGY, **Master of Science in Analytics**, December 2022")
st.write("NEW YORK UNIVERSITY, **Master of Education**, May 2007")
st.write("GEORGE MASON UNIVERSITY, **Bachelor of Arts in English Language**, January 2001")
st.write("IBM, **DevOps and Software Engineering Certification**, Current")
st.write("MONGODB, **MongoDB for Python Developers Certification**, January 2022")
st.write("DATACAMP, **Python Data Science Certification**, July 2021")
st.write("GOOGLE, **IT Automation with Python Certification**, July 2020")
st.write("---")
