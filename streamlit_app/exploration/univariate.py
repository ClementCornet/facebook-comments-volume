import streamlit as st
import extra_streamlit_components as stx

import plotly.express as px
import numpy as np
import pandas as pd

from plotly.subplots import make_subplots
import plotly.graph_objects as go

import matplotlib.pyplot as plt


def univariate_page(df):
    #st.dataframe(df)
    st.title('Univariate Analysis')

    features = stx.tab_bar(data=[
            stx.TabBarItemData(id='page_ft',title='Page Features',description=''),
            stx.TabBarItemData(id='ess_ft',title='Essential Features',description=''),
            stx.TabBarItemData(id='wkd_ft',title='Weekday Features',description=''),
            stx.TabBarItemData(id='oth_ft',title='Other Features',description=''),
            stx.TabBarItemData(id='target',title='Target Variable',description='')]
        )
    if features == 'page_ft':
        page_features(df)
    if features == 'ess_ft':
        essentiel_features(df)
    if features == 'wkd_ft':
        weekday_features(df)
    if features == 'oth_ft':
        other_features(df)
    if features == 'target':
        target_features(df)



def page_features(df):
    cols = st.columns([3,1])

    with cols[0].container():
        f1 = px.box(x=df['Page Popularity Likes'],log_x=True)
        f1.update_layout(xaxis_title='Page Popularity Likes', margin=dict(l=0, r=0, t=0, b=0),height=150)
        st.plotly_chart(f1)

        f2 = px.box(x=df['Page Talking About'],log_x=True)
        f2.update_layout(xaxis_title='Pages Talking About', margin=dict(l=0, r=0, t=0, b=0),height=150)
        st.plotly_chart(f2)

        f4 = px.box(x=df['Page Checkins'], log_x=True)
        f4.update_layout(xaxis_title='Pages Checkins', margin=dict(l=0, r=0, t=0, b=0),height=150)
        st.plotly_chart(f4)

    with cols[1].container():
        val = df['Page Category'].value_counts()
        page_cat = val[val >= len(df)/50]
        page_cat['Other'] =  np.sum(val[val < len(df)/50])
        f3 = px.pie(values=page_cat.values, names=page_cat.index,title='Page Category')
        f3.update_traces(textposition='inside', textinfo='percent+label',showlegend=False)
        f3.update_layout(
                margin=dict(l=0, r=0, t=40, b=0),
                width=300,
                height=300
            )
        st.plotly_chart(f3)
        st.write("""To have a better understanding of the consequences of the page category, we can group the categories
                    that have a similar meaning.""")
    
    

def essentiel_features(df):

    col_stat = [
        "Number of comments",
        "Aggregated Min",
        "Aggregated Max",
        "Aggregated Avg",
        "Aggregated Median",
        "Aggregated Std"
    ]

    cols = st.columns([1,4])
    pattern = ['total','last 24', 'last 48-24', 'first 24']

    display_stat_radio = cols[0].radio('Statistic to Show : ',col_stat)
    display_cols = 'dd'
    if display_stat_radio == "Number of comments":
        display_cols = ['total','last 24', 'last 48-24', 'first 24']
    else:
        stat = display_stat_radio.split()[1]
        display_cols = [col for col in df.columns if stat in col and 'evo' not in col]

    cols[0].write("""To have a better view on the tendency for a given post, we could extract the evolution
                    of its number of comments and like between the last 48-24h and last 24h""")

    fig = make_subplots(rows=2, cols=2, subplot_titles=pattern)

    for i,col in enumerate(display_cols):
        fig.add_trace(
            go.Histogram(x=df[col],xbins=dict(
                    start=0,
                    end=1700,
                    size=10
                )),
            row=i%2+1, col=i//2+1
        )
    
    fig.update_layout(
                margin=dict(l=0, r=0, t=40, b=0),
                showlegend=False
            )
    cols[1].plotly_chart(fig)

    cols[0].write("""We cannot represent those informations as time series, as the time between the publication and
                    the basetime is unconsistent.""")

def weekday_features(df):

    # Two pie charts
    cols = st.columns(2)
    s1 = df['Post Published Weekday'].value_counts()
    s2 = df['Base DateTime Weekday'].value_counts()

    f1 = px.pie(values=s1.values, names=s1.index, title='Post Published Weekday')
    f2 = px.pie(values=s2.values, names=s2.index, title='Base DateTime Weekday')

    f1.update_traces(textposition='inside', textinfo='percent+label',showlegend=False)
    f2.update_traces(textposition='inside', textinfo='percent+label',showlegend=False)

    f1.update_layout(margin=dict(l=0, r=100, t=40, b=100))
    f2.update_layout(margin=dict(l=0, r=100, t=40, b=100))

    cols[0].plotly_chart(f1)
    cols[1].plotly_chart(f2)

    st.write("The weekday post were published, and the web crawler inspected them are almost evenly distributed")


def other_features(df):

    f1 = px.histogram(df['Elapsed Base Time'],height=150,width=1000)
    f1.update_layout(showlegend=False)
    f1.update_layout(xaxis_title='Elapsed Base Time', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(f1)

    f2 = px.box(x=df['Post Length'],log_x=True,height=150,width=1000)
    f2.update_layout(xaxis_title='Post Length (log scale)', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(f2)
    
    f3 = px.box(x=df['Post Share Count'],log_x=True,height=150,width=1000)
    f3.update_layout(xaxis_title='Post Share Count (log scale)', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(f3)


def target_features(df):

    cols = st.columns([1,5,4])

    measure = df['Measurement'].value_counts()
    measure_24 = measure.loc[24]
    measure_less = len(df) - measure_24
    f1 = px.pie(values=[measure_24, measure_less], names=['24h','Less than 24h'])
    f1.update_traces(textposition='inside', textinfo='percent+label',showlegend=False)
    f1.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            width=250,
            height=250
        )
    cols[1].write('Target Measurement Time')
    cols[1].plotly_chart(f1)

    cols[2].write("""The vast majority of the Target Variable (number of comments) measurement occure 24h
                    after the base time. Also, more than half of the posts of the dataset get no comments
                    during this interval and 95% get less than 8, while very rare posts get +1000 comments.""")

    f2 = px.box(df, x='Target Variable', log_x=True, height=150, width=1000)
    f2.update_layout(xaxis_title='Target Variable (log scale)', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(f2)

    
    