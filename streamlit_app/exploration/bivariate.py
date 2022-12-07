import pandas as pd
import numpy as np

import streamlit as st

import plotly.express as px

import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

import seaborn as sns
import matplotlib.pyplot as plt
import extra_streamlit_components as stx

def bivariate_page(df):
    st.title('Bivariate Analysis')
    corr_ = stx.tab_bar(data=[
            stx.TabBarItemData(id='wkd_cat',title='Weekday and Category',description=''),
            stx.TabBarItemData(id='num_corr',title='Correlations',description=''),
            stx.TabBarItemData(id='ess_var',title='Essential Features',description='')
            ]
        )
    if corr_ == 'wkd_cat':
        weekday_category(df)
    if corr_ == 'num_corr':
        target_corr(df)
    if corr_ == 'ess_var':
        ess_corr(df)

def target_bivariate(df):
    mean_ = df.groupby(['Measurement']).mean()['Target Variable']
    
    fig = px.scatter(mean_,trendline='ols', trendline_color_override='darkblue')

    model = LinearRegression()
    X = df['Measurement'].values.reshape(-1,1)
    y = df['Target Variable']

    X = np.array(range(1,25)).reshape(-1,1)
    y = mean_

    model.fit(X, y)
    x_range = np.linspace(X.min(), X.max(), 100)
    y_range = model.predict(x_range.reshape(-1, 1))
    fig.add_traces(go.Scatter(x=x_range, y=y_range, name='Regression Fit'))
    st.write(model.score(X,y))
    st.write(model.coef_)

    st.plotly_chart(fig)


def weekday_category(df):

    cols = st.columns([1,1])
    with cols[0].container():
        category = df.groupby('Adjusted Categories').mean()['Target Variable'].sort_values()[::-1]
        f1 = px.histogram(x=category.index, y=category.values,labels={"x":"","y":"comments"},histfunc='avg')
        f1.update_layout(title='Average Number of Comments by Page Category',height=250, width=500,margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(f1)

        pub_weekday = df.groupby('Post Published Weekday').mean()['Target Variable'].sort_values()[::-1]
        f2 = px.histogram(x=pub_weekday.index, y=pub_weekday.values,labels={"x":"","y":"comments"},histfunc='avg')
        f2.update_layout(title='Average Number of Comments by Publication Weekday',height=250, width=500,margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(f2)
    
    with cols[1].container():
        cross = pd.crosstab(df['Adjusted Categories'], df['Post Published Weekday'])
        fig,axs = plt.subplots(figsize=(5,3.8))
        sns.color_palette("mako", as_cmap=True)
        sns.heatmap(cross, xticklabels=True, yticklabels=True,annot=True,fmt='d',cmap="Blues")
        axs.set_title('Number of post by Category and Weekday')
        st.pyplot(fig)
        st.write("""Wednesday is the day the posts get the more comments. This also is the day where the more
                 popular categories are the more active. """)


def target_corr(df):

    cols = st.columns([2,1])

    with cols[0].container():

        no_ts = df.select_dtypes("number")

        no_ts = df.select_dtypes("number")[['Page Popularity Likes','Page Checkins','Page Talking About',
        'Elapsed Base Time','Post Length','Post Share Count','Measurement']]
        num_corr = [df[col].corr(df['Target Variable']) for col in no_ts.columns]
        fig = px.bar(x=no_ts.columns,y=num_corr)
        fig.update_layout(
            title='Correlations with the Target Variable',
            xaxis = dict(
                tickmode = 'array',
                ticktext = no_ts.columns),
            height=450
        )
        fig.update_xaxes(title=None)
        fig.update_yaxes(title='correlations')
        st.plotly_chart(fig)

    with cols[1].container():

        st.write("""The time between the post publication and the web crawler inspection is strongly anti-correlated
                    to the number of comments the post will get in the future. It means that a post generally gets
                    a lot more comments shortly after its publication, but it quickly slows down.""")
        st.write("""Note that from the page features, the most important one in our case seems to be the number
                    pages talking about the page that made the post. Also, the Length of a post seems to have almost
                    no correlation to its number of comments.""")


def ess_corr(df):
    
    pattern = ['total','last 24','last 48-24', 'first 24', 'evo 48-24']

    cols = st.columns([1,3])

    with cols[0].container():
        time = st.radio('Time interval:', pattern)

        if time == 'total':
            st.write("""As expected, the total number of comments on a post is strongly correlated with how much comments
                        it will receive in the future. Note that the extreme values for the page seem less
                        significant.""")
        if time == 'last 24':
            st.write("""The aggregated by page variables are less correlated with the target value for the last 24h,
                        but the number of comments on a post in that interval as the highest correlation with the
                        target among our dataset""")
        if time == 'last 48-24':
            st.write("""In the last 48 to 24h, the number of comments on the page seem more important regarding
                        our problem than the number of comments on a post""")

        if time == 'evo 48-24':
            st.write("""If the page has a post that lost a lot of comments in the last 2 days, the post will
                        be more likely to get a lot of comments in the future (negative correlation on the Aggregated
                        Min). Being able to lose a lot of comments implies having a lot.""")

    with cols[1].container():

        #for time in pattern:
        cols = [col for col in df.columns if time in col]
        #st.dataframe(df[cols])
        num_corr = [df[col].corr(df['Target Variable']) for col in cols]
        fig = px.bar(x=cols,y=num_corr)
        fig.update_layout(
            title=f'Correlations with the Target Variable, {time}',
            xaxis = dict(
                tickmode = 'array',
                ticktext = cols),
        )
        fig.update_xaxes(title=None)
        fig.update_yaxes(title='correlations')
        st.plotly_chart(fig)
