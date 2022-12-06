import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def pred_page(df):
    st.title("Predictions")

    algos_names = [
                    'LinearRegression ',
                    'Ridge',
                    'Lasso',
                    'DecisionTreeRegressor ',
                    'XGBRegressor'
                ]
    r2 = [
        -3.748479787854166e+16,
        0.29530953637888124,
        0.3386819574999238,
        0.5195721996566155,
        0.6519693547475467,
    ]

    fig = px.bar(x=algos_names, y=r2,title='Best R² for each Algorithm',text_auto=True)
    fig.update(layout_yaxis_range = [-1,1])
    fig.update_xaxes(title='Algorithm')
    fig.update_yaxes(title='R² over a validation dataset')

    cols = st.columns([2,1])

    cols[0].plotly_chart(fig)

    cols[1].write("""As we want to predict the number of comments a post will get in the future, we have a regression
                problem. Knowing that, we test multiple regression algorithm with multiple hyperparameters,
                using a grid search,to obtain the best possible model.""")

    cols[1].write("""Our data cannot fit a linear regression at all. Although, XGBoost Regressor is the
                    best performing, as we could expect, especially on large and heterogenous data. It performs
                    quite well, but our data (or the social medias) does not seem totally predictable""")