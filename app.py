import streamlit as st
from streamlit_app.utilities.helpers import go_to_page

from streamlit_option_menu import option_menu as om
import pandas as pd

st.set_page_config(layout='wide')

df = pd.read_csv('fb_comments2.csv',index_col=None)

with st.sidebar:
    choice = om('Facebook Comments', ['Presentation',
                                    'Univariate Analysis',
                                    'Created Variables',
                                    'Bivariate Analysis',
                                    'Predictions'],
                        orientation='vertical')


go_to_page(choice, df)