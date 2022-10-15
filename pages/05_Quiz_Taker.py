import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId
import pytz
import requests
import random
from tabulate import tabulate
from datetime import datetime
from pathlib import Path

st.set_page_config(page_icon="🧾", page_title='Quiz Taker')
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"

# load css
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

############################################################################
# MongoDB, https://www.mongodb.com/
############################################################################

def init_mongo(mongo_user, mongo_password):
    client = MongoClient(f"mongodb+srv://{mongo_user}:{mongo_password}@sandbox.zqzg8.mongodb.net/?retryWrites=true&w=majority")
    return client

def close_mongo(client):
    client.close()

def write_collection(coll, limit=10):
    cursor = coll.find()
    for idx, doc in enumerate(cursor):
        if idx < limit:
            st.write(doc)

def insert_word(word, examples, coll):
    now = datetime.now(pytz.utc)
    result = coll.insert_one({'word': word, 'examples': examples, 'updated': now})
    return result

def get_examples_mongo(word, coll):
    result = coll.find_one({'word': word})
    if result:
        examples = result['examples']
    else:
        examples = None
    return examples

def get_quiz_by_id(quiz_id, coll):
    quiz = coll.find_one({'_id': ObjectId(quiz_id)})
    return quiz

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

apiUrl = 'http://api.wordnik.com/v4'
apiKey = st.secrets.api_key

mongo_user = st.secrets.mongo_user
mongo_password = st.secrets.mongo_password

quiz_id = None

st.markdown("# Quiz Taker")
st.sidebar.markdown("# Quiz Taker")
st.sidebar.markdown("Enter a quiz ID to take a quiz.")
query_params = st.experimental_get_query_params()
if "quiz" in query_params:
    quiz_id = query_params["quiz"][0]
else: 
    quiz_id = st.text_input("Enter the quiz id").strip()

if quiz_id and ObjectId.is_valid(quiz_id):
    client = init_mongo(mongo_user, mongo_password)
    coll = client.portfolio_project.quizzes
    quiz_info = get_quiz_by_id(quiz_id, coll)
    close_mongo(client)
    if quiz_info:
        results = quiz_info['quiz']
        title = quiz_info['title']
        if title == None: title = "Quiz" # if no title, use "Quiz"
        word_bank = list(results.keys())
        random.shuffle(word_bank)
        st.markdown("## " + title)
        st.markdown("### Word Bank")
        html_table = tabulate(chunker(word_bank, 5), tablefmt='html')
        st.markdown(html_table, unsafe_allow_html=True)
        st.markdown("### Questions")
        st.write("Complete the sentences with the words from the word bank.")
        with st.form("sentence_completion"):
            for idx, item in enumerate(results.items()):
                st.text_input(f'{idx + 1}. {item[1]}', placeholder="Type answer here")
            st.form_submit_button(label="Submit")
    else:
        st.warning("Quiz not found. Please check the id and try again.")

if quiz_id and not ObjectId.is_valid(quiz_id):
    st.warning("Invalid quiz id. Please check the id and try again.")

