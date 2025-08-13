import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_meta_data(url):
    try:
        response = requests.get(url.strip(), timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'lxml')

        # Meta title
        title_tag = soup.find('title')
        title = title_tag.string.strip() if title_tag and title_tag.string else 'No title found'
        title_len = len(title)

        # Meta description
        description_tag = soup.find('meta', attrs={'name': 'description'})
        description = description_tag['content'].strip() if description_tag and description_tag.get('content') else 'No description found'
        desc_len = len(description)

        # H1 tags
        h1_tags = soup.find_all('h1')
        h1_texts = [tag.get_text(strip=True) for tag in h1_tags] if h1_tags else ['No h1 tags found']

        # H2 tags
        h2_tags = soup.find_all('h2')
        h2_texts = [tag.get_text(strip=True) for tag in h2_tags] if h2_tags else ['No h2 tags found']

        return title, title_len, description, desc_len, h1_texts, h2_texts, None

    except requests.exceptions.RequestException as e:
        return None, None, None, None, None, None, str(e)


st.set_page_config(page_title="Website Meta Data Extractor", layout="wide")
st.title('🌐 Website Meta Data Extractor')

# User input
url_input = st.text_area('Enter one or more URLs (space-separated):')

if url_input:
    urls = [u.strip() for u in url_input.split() if u.strip()]

    for url in urls:
        st.markdown(f"### 📌 Results for: {url}")
        with st.spinner(f'Fetching meta data for {url}...'):
            title, title_len, description, desc_len, h1_texts, h2_texts, error = get_meta_data(url)

            if error:
                st.error(f"❌ Error fetching data from {url}: {error}")
            else:
                # Meta Title
                st.subheader('Meta Title:')
                st.write(title)
                if title_len <= 60:
                    st.success(f"✅ Character length (with spaces): {title_len} (Good for SEO)")
                else:
                    st.error(f"⚠️ Character length (with spaces): {title_len} (Too long for SEO)")

                # Meta Description
                st.subheader('Meta Description:')
                st.write(description)
                if desc_len <= 160:
                    st.success(f"✅ Character length (with spaces): {desc_len} (Good for SEO)")
                else:
                    st.error(f"⚠️ Character length (with spaces): {desc_len} (Too long for SEO)")

                # H1 Tags
                st.subheader('H1 Tags:')
                for h1 in h1_texts:
                    st.write(f"- {h1}")

                # H2 Tags
                st.subheader('H2 Tags:')
                for h2 in h2_texts:
                    st.write(f"- {h2}")

        st.markdown("---")
