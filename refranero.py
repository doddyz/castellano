# Add percent loading bar at start up cf tools in st to do this  
# Implement search filters: search by frequency of use, ... (papier crayon 1st)

import os
import requests
import streamlit as st
from bs4 import BeautifulSoup

BASE_URL = 'https://cvc.cervantes.es/lengua/refranero/'

SAMPLE_REFRAN_URL = 'https://cvc.cervantes.es/lengua/refranero/ficha.aspx?Par=58028&Lng=0'

headers = {'user-agent': 'Mozilla/5.0'}

ALPHABET = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()

def get_all_letters_urls():
    urls = []
    for letter in ALPHABET:
        request_url = BASE_URL + '?letra=' + letter
        # print(request_url)
        urls.append(request_url)
    return urls


@st.experimental_memo
def get_paremias_listing(letter):
    paremias_listing_url = BASE_URL + 'listado.aspx?letra=' + letter
    r = requests.get(paremias_listing_url, headers=headers)
    page_content = r.text
    
    soup = BeautifulSoup(page_content, 'html.parser')
    parent_ol = soup.find('ol', id='lista_az')
    child_links = parent_ol.find_all('a')
    child_link_texts = [link.text for link in child_links]
    child_link_hrefs = [link['href'] for link in child_links]
    
    return {link: href for (link, href) in zip(child_link_texts, child_link_hrefs)}


def save_as_html_paremias_details_pages(letter):
    paremias = get_paremias_listing(letter)
    letter_dir_path = os.path.join(os.getcwd(), 'HTML/', letter)
    for paremia in paremias.keys():
        # with open(os.path.join(letter_dir_path, paremia + '.html'), 'w') as f:
        with open(letter_dir_path + '/' + paremia + '.html', 'w') as f:
            paremia_page = BASE_URL + paremias[paremia]
            r = requests.get(paremia_page, headers=headers)
            f.write(r.text)

@st.experimental_memo
def get_paremia_details(letter, paremia_filename):
    
    file_path_string = os.getcwd() + '/HTML/'+ letter + '/'+ paremia_filename + '.html'
    with open(file_path_string) as f:
        
        soup = BeautifulSoup(f, 'html.parser')
        parent_div = soup.find('div', class_='tabbertab')
        child_ps = parent_div.find_all('p')
    
        # Keep 1st 6 elts only
        child_ps_text = [p.text for p in child_ps][:6]
        details_dict = {text.split(':')[0]: text.split(':')[1].strip() for text in child_ps_text}
    
    return details_dict


def get_paremia_details_web(paremia_page):
    r = requests.get(paremia_page, headers=headers)
    page_content = r.text
    
    soup = BeautifulSoup(page_content, 'html.parser')
    parent_div = soup.find('div', class_='tabbertab')
    child_ps = parent_div.find_all('p')
    
    # Keep 1st 6 elts only
    child_ps_text = [p.text for p in child_ps][:6]
    details_dict = {text.split(':')[0]: text.split(':')[1].strip() for text in child_ps_text}
    
    return details_dict


def create_paremia_details_expander(letter, paremia_filename):
    paremia_details = get_paremia_details(letter, paremia_filename)
    fill_in_issue_paremia_details(paremia_details)
    with st.expander(paremia_details['Enunciado']):
        st.markdown(f''' 
        **Tipo**: {paremia_details['Tipo']}   
        **Enunciado**: {paremia_details['Enunciado']}  
        **Ideas clave**: {paremia_details['Ideas clave']}  
        **Significado**: {paremia_details['Significado']}  
        **Marcador de uso**: {paremia_details['Marcador de uso']}  
        ''')

def fill_in_issue_paremia_details(paremia_details_dict):
    for key in ['Tipo', 'Enunciado', 'Significado', 'Ideas clave', 'Marcador de uso']:
        if key not in paremia_details_dict.keys():
            paremia_details_dict[key] = 'No disponible'
        
            
def create_paremia_details_expanders(letter):
    paremias_listing = get_paremias_listing(letter)
    paremia_titles = paremias_listing.keys()
    # st.write(letter_dir_path)
    for paremia_title in paremia_titles:
        paremia_filename = paremia_title
        # st.write(f'{file_path_string}: {type(file_path_string)}')
        create_paremia_details_expander(letter, paremia_filename)


def create_paremia_letter_container(letter):
    st.subheader(letter)
    create_paremia_details_expanders(letter)


def create_paremia_letter_containers():
    for letter in ALPHABET:
        create_paremia_letter_container(letter)
        
    
    
        


    



    
