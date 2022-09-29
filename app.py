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
PAGE_LAYOUT = "wide"
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

# st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=PAGE_LAYOUT)


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
