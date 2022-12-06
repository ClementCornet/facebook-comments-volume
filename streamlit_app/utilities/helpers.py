import pandas as pd
import streamlit as st

import extra_streamlit_components as stx

from streamlit_app.exploration.univariate import univariate_page
from streamlit_app.exploration.bivariate import bivariate_page
from streamlit_app.exploration.created_vars import created_page
from streamlit_app.predictions.predictions import pred_page


def go_to_page(choice, df):
    if choice == 'Presentation':
        land_page()


    if choice == 'Univariate Analysis':
        univariate_page(df)

    if choice == 'Created Variables': 
        created_page(df)

    if choice == 'Bivariate Analysis': 
        bivariate_page(df)
    
    if choice == 'Predictions':
        pred_page(df)


def land_page():
    st.markdown("""
    # Facebook Comments Volume Dataset
    This dataset is composed of data about Facebook posts. It provides 53 variables,
    such as the Page Category or Popularity, or the number of comments a post has received
    short after its publication. The objective is to predict the number of comments the post will
    receive in the future.

    The different variables are divided in 5 categories, according to the responsible of the dataset:

    - Page Features

    Those variables do not describe the post in itself, but the page that posted it, such as the Page Category, or its total number of likes.

    - Essential Features

    The aim of this dataset is to predict the number of comments a post will receive in the future. The dataset contains the pattern of 
    comments on the post in various time intervals (first 24 hours, first 24 to first 48h...). It also contains 'derived' features, where the previously discussed features are aggregated by page.
        """)
    cols = st.columns([1,1,1])
    cols[1].image('essential_features.jpg')

    st.markdown("""
    - Weekday Features

    Two variables describe the weekday a post was published, and the weekday the web crawler that built the dataset got inspected the post.

    - Other Variables

    Some variables do not fit our typology, but may still be important. One variable contains the time between the post publication, and the time the crawler inspected it. We also have information about the post length, and the post share count.

    - Target Variable

    Finally, this dataset it built to predict the number of comments a post will get in the future. Our target variable stores the number of comments received after the crawler firt inspected it. The delay is also stored.""")