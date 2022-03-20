import streamlit as st
import time
from refranero import *

st.set_page_config(
     page_title='Refranero castellano',
     page_icon=':memo:',
     layout='wide',
     initial_sidebar_state='expanded',
 )


st.markdown('# Refranero Castellano :memo:')

letter_columns = st.columns(26)
for i, letter in enumerate(ALPHABET):
    letter_columns[i].markdown(f'[{letter}](#{letter.lower()})', unsafe_allow_html=True)

    
create_paremia_letter_containers()








