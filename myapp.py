import streamlit as st
import time
import pandas as pd
from urllib.parse import urlparse
from usp.tree import sitemap_tree_for_homepage

st.title("URL grabber from sitemap file")
st.markdown("This is a tool for iFOCUS.sk Link Nest plugin - Internal linking for Wordpress")

# use the suppress_st_warning parameter to suppress the warning message
@st.cache(suppress_st_warning=True)  
def sitemap_urls(url):
    with st.spinner("Wait for it..."):
        time.sleep(10)

        # parse the URL to ensure it is a valid HTTP(S) URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = "https://" + url

        # find the sitemap tree for the homepage
        tree = sitemap_tree_for_homepage(url)
        st.success("Done!")

    urls = []

    for page in tree.all_pages():
        page = page.url
        urls.append(page)

    return urls

x = st.text_input("Insert Your URL. We will find your sitemap file. It will take few seconds.")

if x:
    try:
        urls = sitemap_urls(x)
        df = pd.DataFrame({"Keyword": "somekeyword", "Atribute (title)": "somekeyword", "Atribute (rel)": "search", "URL": urls})
        st.download_button("Download URLs as CSV", df.to_csv(index=False), file_name="sitemap-urls.csv",)
    except Exception as e:
        st.write("An error occurred:", e)
else:
    st.write("INFO: Please enter a valid URL.")
