from collections import defaultdict
import re
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from costants import *
from utils import *
import os.path as osp
from viz import pizza_plot, scatter_ranking, radar_plot

# MARK: Session state
mandatory_keys = ['Nome', 'Cognome', 'Email', 'Telefono', 'Età']
score_categories = ['Tecnologia', 'Calcio', 'Personale', 'Economico']
SHEET = 'Sheet1'

keys = mandatory_keys
for k in keys:
    if k not in st.session_state:
        st.session_state[k] = ''

# ----------Questionario--------------
# Question dictionary

if 'questions' not in st.session_state:
    st.session_state['questions'] = {}

def set_question_in_session_state(question):
    if question not in st.session_state:
        st.session_state['questions'][question] = {a['text']: 0 for a in questions[question].values()}

# Function to handle checkbox selection and update session state
def change_answer_status(question, selection):
    for key in st.session_state['questions'][question]:
        st.session_state['questions'][question][key] = 0  # Deselect all
    st.session_state['questions'][question][selection] = 1  # Select the chosen one



# MARK: Google Sheet connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing data
existing_data = conn.read(
    worksheet=SHEET,  # Nome worksheet
    ttl=5
)
existing_data = existing_data.dropna(how='all')

# st.dataframe(existing_data)
img_col, title_col = st.columns([.2,.8], vertical_alignment='center')
with img_col:
    st.image(osp.join('loghi', 'verde.png'))
with title_col:
    st.title('Sport Analisi Academy')

# Initialize session state for answers, score, and final answers
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'score' not in st.session_state:
    st.session_state.score = defaultdict(lambda : 0)
if 'final_answers' not in st.session_state:
    st.session_state.final_answers = {}
if 'questionnaire_completed' not in st.session_state:
    st.session_state.questionnaire_completed = False

# Helper function to check if questionnaire is completed
def check_questionnaire_completed():
    """Check if all the questions are answered and set the session state."""
    questionnaire_complete = all(f"{q}_confirmed" in st.session_state for q in questions)
    if questionnaire_complete:
        st.session_state.questionnaire_completed = questionnaire_complete
    else:
        st.error('Per favore compila tutte le domande')
    return questionnaire_complete

# Helper function to display a question and handle answer selection
def display_question(question_key, question_data):
    st.markdown(f"### {question_data['question_text']}")

    selected_answer = st.selectbox(
                question_data["question_text"], 
                options=[ans['text'] for ans in question_data['answers'].values()], 
                key=question_key,  # Use the question_key to track answers
                index = None,
                label_visibility = 'collapsed'
            )
    
    # Button to confirm the selection
    if selected_answer:
        question_category = question_data['category']
        answers_object = list(filter(lambda x: x[1]['text'] == selected_answer, question_data['answers'].items()))[0]
        answer_key, asnwer_prop = answers_object
        
        # Store the selected answer and update the score
        st.session_state.answers[question_key] = answer_key
        # st.session_state.score[question_category] += asnwer_prop['points']
        # st.session_state.score['score'] += asnwer_prop['points']
        # for c in score_categories:
        #     st.write(c, st.session_state.score[c])
        # st.write(st.session_state.score['score'])
        
        # Update the final_answers dictionary
        st.session_state.final_answers[question_key] = {
            'question_text': question_data['question_text'],
            'category': question_data['category'],
            'selected_answer': selected_answer,
            'selected_text': asnwer_prop['text'],
            'points': asnwer_prop['points']
        }
        st.session_state[f"{question_key}_confirmed"] = True
        
        # # Check if the questionnaire is now completed
        # completed = check_questionnaire_completed()

        # if completed:
        #     st.rerun()


    return selected_answer
        
# Function to handle sub-questions or messages
def display_subquestions_or_message(main_question_key, main_answer_key, question_data):
    main_answer = question_data['answers'][main_answer_key]
    
    # Check if the main answer has sub-questions or a message
    if 'sub_questions' in main_answer:
        sub_questions = main_answer['sub_questions']
        
        # For each sub-question
        for sub_question_key, sub_question_data in sub_questions.items():
            if f"{main_question_key}_confirmed" in st.session_state:
                display_question(sub_question_key, sub_question_data)
    elif 'message' in main_answer:
        # Display the message
        st.markdown(f"**Note:** {main_answer['message']}")


def compute_scores(final_answers):
    scores = {
        k:0 for k in score_categories
    }

    for v in final_answers.values():
        scores[v['category']] += v['points']

    scores['score'] = sum(list(scores.values()))

    st.session_state['score'] = scores

    return scores

# Conditionally render content
if st.session_state.questionnaire_completed:

    # Upload the data to the worksheet
    user_record = {k: st.session_state[k] for k in mandatory_keys}
    answers = {'_'.join(q.split('_')[1:]): v['selected_text'] for q, v in st.session_state.final_answers.items()}
    user_record.update(answers)
    scores = compute_scores(st.session_state.final_answers)
    user_record.update(scores)

    update_data = pd.concat(
        [existing_data, pd.Series(user_record).to_frame().T], ignore_index=True
    )
    #st.table(update_data)
    conn.update(worksheet=SHEET, data=update_data)

    # Mark the questionnaire as submitted
    st.session_state['submitted'] = True

    def get_thank_you_message(total_score):
        for category, data in score_ranges.items():
            if data['range'][0] <= total_score <= data['range'][1]:
                return data['message'], category

    message, fascia = get_thank_you_message(scores['score'])
    # Display thank you message
    st.markdown(f"# Fascia: {fascia}")
    st.markdown(f"#### {message}")
    

    st.pyplot(radar_plot(df_selected=update_data, highlight_user=st.session_state['Email']))

    st.pyplot(pizza_plot(df_selected=update_data, highlight_user=st.session_state['Email']))
    
else:
    # Display the questionnaire form

    st.markdown('### Info personali')
    name_col, surname_col = st.columns(2)

    with name_col:
        st.session_state['Nome'] = st.text_input('Nome').capitalize()

    with surname_col:
        st.session_state['Cognome'] = st.text_input('Cognome').capitalize()

    email_col, phone_col, age_col = st.columns([0.4, 0.4, 0.2])

    with email_col:
        st.session_state['Email'] = st.text_input('Email')

    with phone_col:
        st.session_state['Telefono'] = st.text_input('Telefono (includi suffisso ex.+39)')

    with age_col:
        st.session_state['Età'] = st.text_input('Età')

    # Check for mandatory fields
    for k in mandatory_keys:
        if not st.session_state[k]:
            st.warning('Completa i campi precedenti')
            st.stop()

    # Check if email and phone are valid before proceeding
    if not are_personal_details_valid():
        st.stop()

    st.divider()


    # Render main questions
    for question_key, question_data in questions.items():
        # Display the main question
        selected_answer = display_question(question_key, question_data)
        
        # If the main question is confirmed, show sub-questions or message
        if selected_answer: #f"{question_key}_confirmed" in st.session_state:
            main_answer_key = st.session_state.answers[question_key]
            display_subquestions_or_message(question_key, main_answer_key, question_data)

    
        
    st.button(label='Invia', on_click=check_questionnaire_completed)
