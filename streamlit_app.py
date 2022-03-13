import streamlit as st
from refranero import *

st.set_page_config(
     page_title='Refranero castellano',
     page_icon=':memo:',
     layout='wide',
     initial_sidebar_state='expanded',
 )

letter_columns = st.columns(26)
for i, letter in enumerate(ALPHABET):
    letter_columns[i].markdown(f'#### [{letter}](#{letter.lower()})', unsafe_allow_html=True)


# st.markdown(f'[Test1](#arbol)', unsafe_allow_html=True)
# st.markdown(f'[Test2](#casa)', unsafe_allow_html=True)    
# st.header('Arbol')
# st.header('Casa')

create_paremia_letter_containers()


