from collections import defaultdict

import streamlit as st
from streamlit_gsheets import GSheetsConnection

from config import *

pages = [
        st.Page("pages/form.py", title="Form"),
        st.Page("pages/graphs.py", title="Risultati"),
    ]

pg = st.navigation(pages)

#MARK: Inizializzazione dello status
#-----------------------------------

#Connessione e dati
if 'conn' not in st.session_state:
    conn = st.connection("gsheets", type=GSheetsConnection)
    existing_data = conn.read(
        worksheet=SHEET,  # Nome worksheet
        ttl=5
    )
    existing_data = existing_data.dropna(how='all')

    st.session_state['conn'] = conn
    st.session_state['existing_data'] = existing_data

#User
for k in MANDATORY_KEYS:
    if k not in st.session_state:
        st.session_state[k] = ''

#Questionario
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'score' not in st.session_state:
    st.session_state.score = defaultdict(lambda : 0)
if 'final_answers' not in st.session_state:
    st.session_state.final_answers = {}
if 'questionnaire_completed' not in st.session_state:
    st.session_state.questionnaire_completed = False
if 'show_error_message' not in st.session_state:
    st.session_state['show_error_message'] = False


    

pg.run()