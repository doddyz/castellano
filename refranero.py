# Extraer todas las páginas web localmente
# Extraer keys & values of paremia page,
# Papier crayon pour la suite pour affichage in expander a lo mejor ...
# Next need to get individual refran content from individual refran pages:
# Recuperar tipo, idioma, ideas clave, todo tipo de campo como diccionario Python a lo mejor

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


# Will return dic of paremia titles and details urls
def get_paremias_listing(letter):
    paremias_listing_url = BASE_URL + 'listado.aspx?letra=' + letter
    # print(paremias_listing_url)
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

def get_paremia_details(paremia_page):
    r = requests.get(paremia_page, headers=headers)
    page_content = r.text
    
    soup = BeautifulSoup(page_content, 'html.parser')
        # print(soup)
    parent_div = soup.find('div', class_='tabbertab')
    child_ps = parent_div.find_all('p')
    # child_ps_strong_text = [p.strong.text for p in child_ps]
    # Keep 1st 6 elts only
    child_ps_text = [p.text for p in child_ps][:6]
    details_dict = {text.split(':')[0]: text.split(':')[1].strip() for text in child_ps_text}
    
    return details_dict
    # child_link_texts = [link.text for link in child_links]
    # child_link_hrefs = [link['href'] for link in child_links]
        
    # return {link: href for (link, href) in zip(child_link_texts, child_link_hrefs)}

def create_paremia_details_expander(paremia_page):
    paremia_details = get_paremia_details(paremia_page)
    with st.expander(paremia_details['Enunciado']):
        st.markdown(f'''
        **Tipo**: {paremia_details['Tipo']}   
        **Enunciado**: {paremia_details['Enunciado']}  
        ''')

def create_paremia_details_expanders(letter):
    paremias_listing = get_paremias_listing(letter)
    paremia_titles = paremias_listing.keys()
    for paremia_title in paremia_titles:
        paremia_page = BASE_URL + paremias_listing[paremia_title]
        create_paremia_details_expander(paremia_page)
    
        


    



    
