import numpy as np
import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

def created_page(df):
    
    st.title('Created Variables')

    cols = st.columns([1,2])

    with cols[0].container():

        df['Adjusted Categories'] =  df['Page Category'].apply(lambda x : group_categories(x))

        page_cat = df['Adjusted Categories'].value_counts()
        f3 = px.pie(values=page_cat.values, names=page_cat.index,title='Adjusted Page Category')
        f3.update_traces(textposition='inside', textinfo='percent+label',showlegend=False)
        f3.update_layout(
                margin=dict(l=0, r=0, t=40, b=0),
                width=300,
                height=300
            )
        st.plotly_chart(f3)

        st.write("""Merging very similar categories (like 'sports league' and 'sports team') makes 'Page Category'
                    more readable.""")
        st.write("""Also, we represented the evolution of the essential values between the last
                    48 to 24 hours and the last 24 hours to have a better understanding on the tendency.""")

    with cols[1].container():

        pattern = ['Min','Max','Avg','Median','Std','total']
        display_cols = [col for col in df.columns if 'evo' in col]
        #st.write(display_cols)
        fig = make_subplots(rows=2, cols=3, subplot_titles=pattern)

        for i,col in enumerate(display_cols):
            fig.add_trace(
                go.Histogram(x=df[col],xbins=dict(
                        size=10
                    )),
                row=i%2+1, col=i//2+1
            )
        
        fig.update_layout(
                    margin=dict(l=0, r=0, t=40, b=0),
                    showlegend=False,
                    title='How did the page number of comments evolve?  '
                )
        st.plotly_chart(fig)




def group_categories(cat):
    if cat in ["Politician","Political party",'Non-governmental organization (ngo)',
    'Government official']:
        return 'Politics'
    if cat in ['Aerospace/defense','Cars','Website','Automobiles and parts',
    'Telecommunication','App page','Software','Electronics','Computers/technology',
    'Camera/photo','Computers','Phone/tablet','Tools/equipment','Internet/software']:
        return 'Technology'
    if cat in ['Food/beverages','Clothing','Restaurant/cafe',
    'Outdoor gear/sporting goods','Vitamins/supplements','Health/medical/pharmacy',
    'Home decor','Health/beauty','Health/medical/pharmaceuticals','Coach','Spas/beauty/personal care']:
        return 'Personal Care'
    if cat in ['Personal blog','Jewelry/watches''Reference website','Landmark','Other']:
        return 'Other'
    if cat in ['Athlete','Professional sports team','Sports event','Sports league',
    'Sports venue','Sports/recreation/activities','Recreation/sports website']:
        return 'Sports'
    if cat in ['Arts/humanities website','Record label','Movie','Song','Artist',
    'Musician/band','Author','Comedian','Studio','Writer','Music video','Music award','Album','Book',
    'Producer','Tv/movie award','Musical instrument','Photographer']:
        return 'Art'
    if cat in ['Media/news/publishing','News/media website','Magazine',
    'Publisher','Business/economy website','Society/culture website','News personality']:
        return 'News'
    if cat in ['Travel/leisure','Hotel','Transportation','Local/travel website']:
        return 'Personal Care'
    if cat in ['Product/service','Retail and consumer merchandise','Company',
    'Local business','Shopping/retail','Professional services','Appliances','Insurance company'
    'Bank/financial institution','Small business']:
        return 'Companies'
    if cat in ['Public figure','Arts/entertainment/nightlife','Actor/director'
    'Tv show','Entertainer','Non-profit organization','Tv channel','Entertainment website',
    'Movie theater','Just for fun','Club','Tv network','Bar','Games/toys','Radio station',
    'Teens/kids website','Video game']:
        return 'Entertainment'
    if cat in ['Education website','Community','Education','School sports team','University',
    'Church/religious organization','School','Cause','Organization']:
        return 'Communities'
    return 'Other'