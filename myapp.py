import streamlit as st
import time
import pandas as pd
import requests
from urllib.parse import urlparse
from usp.tree import sitemap_tree_for_homepage

"""
# Sitemap URL Extractor

Welcome to the Sitemap URL Extractor, your one-stop tool for discovering and extracting URLs from sitemaps!

This interactive Streamlit app was crafted by [Your Name] to simplify the process of finding and exporting URLs from sitemaps. Just enter a website URL, click the "Search" button, and let the magic happen!

"""

st.markdown('''
<style>
.stApp [data-testid="stToolbar"]{
    display:none;
}
</style>
''', unsafe_allow_html=True)

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def sitemap_urls(url):
    with st.spinner("Scanning for sitemap..."):
        time.sleep(10)

        # Ensure the URL is valid with an HTTP(S) scheme
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = "https://" + url

        # Find the sitemap tree for the homepage
        tree = sitemap_tree_for_homepage(url)
        st.success("Sitemap detected!")

    urls = []

    for page in tree.all_pages():
        page = page.url
        urls.append(page)

    return urls

x = st.text_input("Enter a website URL")

if st.button("Search"):
    if x:
        # Check if the URL has a scheme (http or https)
        if not urlparse(x).scheme:
            # If the URL doesn't have a scheme, add 'http://' to the beginning
            x = 'http://' + x

        # Check if the URL responds with a status code of 200
        try:
            if requests.get(x).status_code == 200:
                urls = sitemap_urls(x)
                df = pd.DataFrame({"Keyword": "SEO", "Attribute (title)": "Description", "Attribute (rel)": "Follow", "URL": urls})
                st.download_button("Download Extracted URLs as CSV", df.to_csv(index=False), file_name="sitemap-urls.csv",)

            else:
                st.error("ERROR: Please enter a valid URL that responds with a status code of 200.")
        except Exception as e:
            st.error("An error occurred: " + str(e))
    else:
        st.warning("Please enter a website URL before clicking the 'Search' button.")
