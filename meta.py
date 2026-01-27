import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_meta_data(url):
    try:
        response = requests.get(
            url.strip(),
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}  # helps avoid some blocks
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "lxml")

        # Meta title
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else "No title found"
        title_len = len(title)

        # Meta description
        description_tag = soup.find("meta", attrs={"name": "description"})
        description = (
            description_tag.get("content", "").strip()
            if description_tag else ""
        )
        description = description if description else "No description found"
        desc_len = len(description)

        # H1 tags
        h1_tags = soup.find_all("h1")
        h1_texts = [tag.get_text(strip=True) for tag in h1_tags] if h1_tags else ["No h1 tags found"]

        # H2 tags
        h2_tags = soup.find_all("h2")
        h2_texts = [tag.get_text(strip=True) for tag in h2_tags] if h2_tags else ["No h2 tags found"]

        return title, title_len, description, desc_len, h1_texts, h2_texts, None

    except requests.exceptions.RequestException as e:
        return None, None, None, None, None, None, str(e)


st.set_page_config(page_title="Website Meta Data Extractor", layout="wide")
st.title("🌐 Website Meta Data Extractor")

url_input = st.text_area("Enter one or more URLs (space-separated):")

if url_input:
    urls = [u.strip() for u in url_input.split() if u.strip()]

    all_rows = []  # <- collect everything for download

    for url in urls:
        st.markdown(f"### 📌 Results for: {url}")
        with st.spinner(f"Fetching meta data for {url}..."):
            title, title_len, description, desc_len, h1_texts, h2_texts, error = get_meta_data(url)

            if error:
                st.error(f"❌ Error fetching data from {url}: {error}")
                all_rows.append({
                    "URL": url,
                    "Meta Title": "",
                    "Title Length": "",
                    "Meta Description": "",
                    "Description Length": "",
                    "H1 Tags": "",
                    "H2 Tags": "",
                    "Error": error
                })
            else:
                # Meta Title
                st.subheader("Meta Title:")
                st.write(title)
                if title_len <= 60:
                    st.success(f"✅ Character length (with spaces): {title_len} (Good for SEO)")
                else:
                    st.error(f"⚠️ Character length (with spaces): {title_len} (Too long for SEO)")

                # Meta Description
                st.subheader("Meta Description:")
                st.write(description)
                if desc_len <= 160:
                    st.success(f"✅ Character length (with spaces): {desc_len} (Good for SEO)")
                else:
                    st.error(f"⚠️ Character length (with spaces): {desc_len} (Too long for SEO)")

                # H1 Tags
                st.subheader("H1 Tags:")
                for h1 in h1_texts:
                    st.write(f"- {h1}")

                # H2 Tags
                st.subheader("H2 Tags:")
                for h2 in h2_texts:
                    st.write(f"- {h2}")

                # store row for download (join lists for CSV)
                all_rows.append({
                    "URL": url,
                    "Meta Title": title,
                    "Title Length": title_len,
                    "Meta Description": description,
                    "Description Length": desc_len,
                    "H1 Tags": " | ".join(h1_texts),
                    "H2 Tags": " | ".join(h2_texts),
                    "Error": ""
                })

        st.markdown("---")

    # DOWNLOAD SECTION (after processing all urls)
    if all_rows:
        df = pd.DataFrame(all_rows)

        st.subheader("⬇️ Download results")
        st.dataframe(df, use_container_width=True)

        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv_bytes,
            file_name="meta_data_results.csv",
            mime="text/csv"
        )
