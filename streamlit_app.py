import streamlit as st
from refranero import *

st.set_page_config(
     page_title='Refranero multilingüe',
     page_icon=':flag-es:',
     layout='wide',
     initial_sidebar_state='expanded',
 )

letter_columns = st.columns(26)
for i, letter in enumerate(ALPHABET):
    letter_columns[i].markdown(f'[{letter}](#{letter})')



st.subheader('A')

# create_paremia_details_expander(SAMPLE_REFRAN_URL)
# create_paremia_details_expanders('A')

st.subheader('B')
st.subheader('C')
st.subheader('D')
st.subheader('E')
st.subheader('F')
    
    
    



