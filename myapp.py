import streamlit as st
import time
import pandas as pd
import requests
from urllib.parse import urlparse
from usp.tree import sitemap_tree_for_homepage

"""
# URL grabber from sitemap file
This is a tool for [iFOCUS.sk](https://www.ifocus.sk) Link Nest plugin - Internal linking for Wordpress

We will find your sitemap file. It will take few seconds.
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
    
x = st.text_input("")

if x:
    # Check if the URL has a scheme (http or https)
    if not urlparse(x).scheme:
        # If the URL doesn't have a scheme, add 'http://' to the beginning
        x = 'http://' + x
        
    # Check if the URL responds with a status code of 200
    try:
        if requests.get(x).status_code == 200:
            urls = sitemap_urls(x)
            df = pd.DataFrame({"Keyword": "somekeyword", "Atribute (title)": "somekeyword", "Atribute (rel)": "search", "URL": urls})
            st.download_button("Download URLs as CSV", df.to_csv(index=False), file_name="sitemap-urls.csv",)

        else:
            st.error("ERROR: Please enter a valid URL that responds with a status code of 200.")
    except Exception as e:
        st.error("An error occurred: " + str(e))
else:
    st.write("INFO: Please enter a valid URL. (Example: yourdomain.com)")
