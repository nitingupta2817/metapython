import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_meta_data(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Get the meta title
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.string.strip() if title_tag.string else 'No title found'
            title_length = len(title)
        else:
            title = 'No title found'
            title_length = 0

        # Get the meta description
        description_tag = soup.find('meta', attrs={'name': 'description'})
        if description_tag and 'content' in description_tag.attrs:
            description = description_tag['content'].strip()
            description_length = len(description)
        else:
            description = 'No description found'
            description_length = 0

        # Debugging: Print lengths to verify
        print(f"Title: {title}, Length: {title_length}")
        print(f"Description: {description}, Length: {description_length}")

        # Get all h1 tags
        h1_tags = soup.find_all('h1')
        h1_texts = [tag.get_text(strip=True) for tag in h1_tags] if h1_tags else ['No h1 tags found']

        # Get all h2 tags
        h2_tags = soup.find_all('h2')
        h2_texts = [tag.get_text(strip=True) for tag in h2_tags] if h2_tags else ['No h2 tags found']

        return title, description, title_length, description_length, h1_texts, h2_texts, None
    except requests.exceptions.RequestException as e:
        return None, None, 0, 0, None, None, str(e)

st.title('Website Meta Data Extractor')

# Input URL from the user
url = st.text_input('Enter the URL of the website:')

if url:
    with st.spinner('Fetching meta data...'):
        title, description, title_length, description_length, h1_texts, h2_texts, error = get_meta_data(url)

        if error:
            st.error(f"Error fetching data: {error}")
        else:
            st.subheader('Meta Title:')
            st.write(f"{title} ({title_length} characters)")

            st.subheader('Meta Description:')
            st.write(f"{description} ({description_length} characters)")

            st.subheader('H1 Tags:')
            for h1 in h1_texts:
                st.write(h1)

            st.subheader('H2 Tags:')
            for h2 in h2_texts:
                st.write(h2)
