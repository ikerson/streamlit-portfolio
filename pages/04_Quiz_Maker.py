#############################################################################
# Imports
#############################################################################

import streamlit as st
from pathlib import Path
import csv
from fpdf import FPDF
import requests
from pymongo import MongoClient
from datetime import datetime
import pytz


#############################################################################
# App Page Setup
#############################################################################

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
csv_file = current_dir / "assets" / "word-meaning-examples.csv"

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
    word = {'word': word, 'examples': examples, 'updated': now}
    result = coll.insert_one(word)
    return result

def insert_quiz(quiz_title, results, coll):
    now = datetime.now(pytz.utc)
    quiz = {'title': quiz_title, 'quiz': results, 'updated': now}
    quiz_id = coll.insert_one(quiz).inserted_id
    return quiz_id

def get_examples_mongo(word, coll):
    result = coll.find_one({'word': word})
    if result:
        examples = result['examples']
    else:
        examples = None
    return examples

def get_quiz_by_id(quiz_id, coll):
    quiz = coll.find_one({'_id': quiz_id})
    return quiz

############################################################################
# Wordnik API, https://developer.wordnik.com/docs#!/word
############################################################################

def get_examples_api(word, apiUrl, apiKey):
    headers = {'api_key': apiKey}
    url = apiUrl + '/word.json/' + word + '/examples'
    response = requests.get(url, headers=headers)
    return response.json()

def get_examples_json(examples_json):
    examples = [example['text'] for example in examples_json['examples']]
    return examples

def clean_examples(examples, word):
    examples = list(set(examples))
    examples = [example.replace(word.lower(), ('_')).replace(word.capitalize(), ('_')) for example in examples]
    return examples

############################################################################
# FPDF, https://pyfpdf.readthedocs.io/en/latest/
############################################################################


class PDF(FPDF):
    def header(self):
        # Rendering logo:
        # self.image("../docs/fpdf2-logo.png", 10, 8, 33)
        # Setting font: helvetica bold 15
        self.set_font("helvetica", "B", 15)
        # Moving cursor to the right:
        self.cell(80)
        # Printing title:
        self.cell(30, 10, "Title", border=1, align="C")
        # Performing a line break:
        self.ln(20)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

#############################################################################
# App Utils
#############################################################################

def get_words():
    make_sentences =  None
    words = st.text_input("Enter words separated by commas")
    words = words.split(",")
    words = [word.strip() for word in words]
    words = [word for word in words if word != ""]
    if len(words) < 3:
        st.warning("Please enter at least 3 words.")
    if len(words) > 20:
        st.warning("Please enter at most 20 words.")
    if len(words) >= 3 and len(words) <= 20:
        make_sentences = st.button("Make Sentences")
    return make_sentences, words

def check_missing_words(results):
    missing_words = ', '.join([word for word in words if word not in results.keys()])
    if missing_words != '':
        st.warning(f"The following word(s) were not found: {missing_words}")
    return missing_words

def get_examples(words, coll, apiUrl, apiKey):
    results = {}
    for word in words:
        examples = get_examples_mongo(word, coll)
        if not examples:
            examples = get_examples_api(word, apiUrl, apiKey)
            examples = get_examples_json(examples)
            examples = clean_examples(examples, word)
            result = insert_word(word, examples, coll)
        results[word] = examples
    return results

def confirm_sentences():
    edit, confirm = None, None
    st.markdown(f"## Sentences")
    st.write("Here are your finized sentences. Edit or confirm the sentences below.")
    for idx, word in enumerate(st.session_state.words):
        st.write(f"{idx+1}. {st.session_state[word]}")
    edit = st.button("Edit")
    confirm = st.button("Confirm")
    return edit, confirm

def edit_sentences(results):
    st.markdown("## Edit")
    st.write("Make desired changes to the sentences below. Click 'Submit' to save the changes.")
    with st.form("edit-form"):
        for word, example in results.items():
            st.text_area(f"Edit the example for {word}", example, height=100, key=f'{word}_edit')
        edit_form_submit = st.form_submit_button("Submit")
    if edit_form_submit:
        for word in results.keys():
            results[word] = st.session_state[word+'_edit']
            del st.session_state[word+'_edit']
    return edit_form_submit, results

def get_words_from_csv(words):
    target_words = {}
    with open(csv_file) as file_in:
        csv_reader = csv.reader(file_in, delimiter=',')
        for row in csv_reader:
            if row[0].lower() in words:
                samples = [x.replace(row[0].lower(), '_', 1).replace(row[0], '_', 1) for x in row[2:] if x != '']
                target_words[row[0].lower()] = samples
    return target_words

def radio_form_submit_callback(results):
    for word in results.keys():
            results[word] = st.session_state[word+'_choice']
            del st.session_state[word+'_choice']
    st.session_state.results = results
    st.session_state.results_choose = False
    st.session_state.results_edit = True

def edit_form_submit_callback(results):
    for word in results.keys():
        results[word] = st.session_state[word+'_edit']
    del st.session_state[word+'_edit']
    st.session_state.results = results
    st.session_state.results_edit = False
    st.session_state.results_confirm = True

def confirm_form_submit_callback(results):
    st.session_state.results = results
    st.session_state.results_confirm = False
    st.session_state.results_final = True

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

############################################################################
# Start App                                                                #
############################################################################

app_url = st.secrets.app_url
target_page = st.secrets.target_page

apiUrl = 'http://api.wordnik.com/v4'
apiKey = st.secrets.api_key

mongo_user = st.secrets.mongo_user
mongo_password = st.secrets.mongo_password

if "intro_stop" not in st.session_state:
    st.session_state.intro_stop = None
if "results" not in st.session_state:
    st.session_state.results = None
if "results_choose" not in st.session_state:
    st.session_state.results_choose = None
if "results_edit" not in st.session_state:
    st.session_state.results_edit = None
if "results_confirm" not in st.session_state:
    st.session_state.results_confirm = None
if "results_final" not in st.session_state:
    st.session_state.results_final = None
if "quiz_title" not in st.session_state:
    st.session_state.quiz_title = None

st.markdown("# Sentence Maker")
st.sidebar.markdown("# Sentence Maker")
st.markdown("## Introduction")
st.markdown("Introduction goes here.")

if not st.session_state.intro_stop:
    make_sentences, words = get_words()
    if make_sentences:
        st.session_state.intro_check = True
        client = init_mongo(mongo_user, mongo_password)
        coll = client.portfolio_project.dictionary
        results = get_examples(words, coll, apiUrl, apiKey)
        close_mongo(client)
        _ = check_missing_words(results)
        st.session_state.results = results
        st.session_state.intro_stop = True
        st.session_state.results_choose = True

if st.session_state.results_choose:
    results = st.session_state.results
    radio_form = st.form(key='radio_form')
    for word, examples in results.items():
        radio_form.markdown(f"#### {word}")
        radio_form.radio(f"Choose the best example for {word}", examples, key=f'{word}_choice')
    radio_form_submit = radio_form.form_submit_button("Submit", 
                        on_click=radio_form_submit_callback, 
                        args=(results,))

if st.session_state.results_edit:
    results = st.session_state.results
    st.markdown("## Edit")
    st.write("Make desired changes to the sentences below. Click 'Submit' to save the changes.")
    with st.form("edit-form"):
        for word, example in results.items():
            st.text_area(f"Edit the example for {word}", example, height=100, key=f'{word}_edit')
        edit_form_submit = st.form_submit_button("Submit", 
                        on_click=edit_form_submit_callback, 
                        args=(results,))

if st.session_state.results_confirm:
    results = st.session_state.results
    st.markdown(f"## Quiz")
    st.write("Please give your quiz a title and confirm the sentences.")
    confirm_form = st.form(key='confirm_form')
    confirm_form.text_input("Quiz Title", key='quiz_title')
    for idx, items in enumerate(results.items()):
        confirm_form.write(f"{idx+1}. {results[items[0]]}")
    confirm_form_submit = confirm_form.form_submit_button("Confirm", 
                                                        on_click=confirm_form_submit_callback, 
                                                        args=(results,))
if st.session_state.results_final:
    results = st.session_state.results
    quiz_title = st.session_state.quiz_title
    client = init_mongo(mongo_user, mongo_password)
    coll = client.portfolio_project.quizzes
    quiz_id = insert_quiz(str(quiz_title), results, coll)
    close_mongo(client)
    st.markdown("### Quiz Created")
    st.markdown("View your quiz at:")
    st.write(f"{app_url}{target_page}/?quiz={quiz_id}")

    # word_bank = list(results.keys())
    # random.shuffle(word_bank)
    # st.markdown(f"## {quiz_title}")
    # st.markdown("### Word Bank")
    # html_table = tabulate(chunker(word_bank, 5), tablefmt='html')
    # st.markdown(html_table, unsafe_allow_html=True)
    # st.markdown("### Questions")
    # st.write("Complete the sentences with the words from the word bank.")
    # with st.form("sentence_completion"):
    #     for idx, item in enumerate(results.items()):
    #         st.text_input(f'{idx + 1}. {item[1]}', placeholder="Type answer here")
    #     st.form_submit_button(label="Submit")

    
    # answer_labels = [list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')[x] for x in range(num_answers)]
    
    # st.write(answer_labels)
    
    # st.markdown("## Sentences")
    # for idx, item in enumerate(sent_dict.items()):
    #     st.write(idx, item[0], item[1][0], item[1][1])
    #     for blank, choice in item:
    #         st.write(f"{idx+1}. {blank}")
    #         st.write(f"Answer: {answers[0]}")
    #         st.write("")


