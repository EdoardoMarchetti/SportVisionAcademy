import pandas as pd
import streamlit as st
from costants import *
from utils import *
import os.path as osp
from viz import pizza_plot, radar_plot
from config import *



def compute_scores(final_answers):
    scores = {
        k:0 for k in score_categories
    }

    for v in final_answers.values():
        scores[v['category']] += v['points']

    scores['score'] = sum(list(scores.values()))

    st.session_state['score'] = scores

    return scores



st.markdown(
    """
<style>
    [data-testid="stSidebarCollapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

#MARK: Page
img_col, title_col = st.columns([.2,.8], vertical_alignment='center')
with img_col:
    st.image(osp.join('loghi', 'verde.png'))
with title_col:
    st.title('Grazie per aver completato il questionario!')

st.write(MESSAGE_OUTRO)

# Upload the data to the worksheet
user_record = {k: st.session_state[k] for k in MANDATORY_KEYS}
answers = {'_'.join(q.split('_')[1:]): v['selected_text'] for q, v in st.session_state.final_answers.items()}
user_record.update(answers)
scores = compute_scores(st.session_state.final_answers)
user_record.update(scores)
update_data = pd.concat(
    [st.session_state['existing_data'], pd.Series(user_record).to_frame().T], ignore_index=True
)


def get_thank_you_message(total_score):
    for category, data in score_ranges.items():
        if data['range'][0] <= total_score <= data['range'][1]:
            return data['message'], category

message, fascia = get_thank_you_message(scores['score'])
# Display thank you message

st.markdown(f"#### Fascia: {fascia}")
st.write(f"{message}")

radar_col, pizza_col = st.columns(2, gap='large')

with radar_col:
    fig = radar_plot(df_selected=update_data, highlight_user=st.session_state['Email'], params=score_categories, mapping=CATEGORIES_MAPPING)
    st.pyplot(fig)
    st.write(RADAR_INFO)



with pizza_col:
    fig = pizza_plot(df_selected=update_data, highlight_user=st.session_state['Email'], params=score_categories, mapping=CATEGORIES_MAPPING)
    st.pyplot(fig)
    st.write(PIZZA_INFO)
    
    

#st.table(update_data)
st.session_state['conn'].update(worksheet=SHEET, data=update_data)

# Mark the questionnaire as submitted
st.session_state['submitted'] = True