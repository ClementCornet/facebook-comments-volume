# Facebook Comments Volume Dataset

## Dataset Description

This dataset is composed of data about 49000 Facebook posts. It provides 53 variables,
such as the Page Category or Popularity, or the number of comments a post has received
short after its publication. The objective it to predict the number of comments the post will
receive in the future.

The different variables are divided in 5 categories, according to the responsible of the dataset:

- Page Features

Those variables do not describe the post in itself, but the page that posted it, such as the Page Category, or its total number of likes.

- Essential Features

The aim of this dataset is to predict the number of comments a post will receive in the future. The dataset contains the pattern of 
comments on the post in various time intervals (first 24 hours, first 24 to first 48h...). It also contains 'derived' features, where the previously discussed features are aggregated by page.

- Weekday Features

Two variables describe the weekday a post was published, and the weekday the web crawler that built the dataset got inspected the post.

- Other Variables

Some variables do not fit our typology, but may still be important. One variable contains the time between the post publication, and the time the crawler inspected it. We also have information about the post length, and the post share count.

- Target Variable

Finally, this dataset it built to predict the number of comments a post will get in the future. Our target variable stores the number of comments received after the crawler firt inspected it. The delay is also stored.

## Task to be Accomplished

### Data Preparation

As this particular Dataset has been created directly to perform Machine Learning, the data preparation is not really long here. Some columns have to be renamed to gain clarity, and the categorical encodings (hierarchical and one-hot) have to be reversed, at least for the time of the data exploration. As the dataset does not contain null values, we don't need to handle those.

### Univariate Analysis

Many variables don't scale linearly. A lot of posts get very few comments, but some get thousands. This goes with the nature of social medias.  
Concerning the essential variables, it is not possible to plot them as a time series (representing number of comments / 24h over time), because the delay beetween the publication and the crawler analysis is not consistent.  
It also is interresting to note that both the publication weekdays, and web crawler analysis weekdays are almost evenly distributed.

### Creating new Variables

Also, we can group the 106 different categories in 11, to group categroies with close meaning, and have a better understanding of our data.  
Also, to understand the tendency for a given post, we can create a new variable representing the evolution beetween the last 48 to 24h and the last 24h.

### Bivariate Analysis

The categories that have the average highest target variable (i.e. the most popular) are Sports and Arts, while Wednesday posts seem to be popular as well. Actually, both Sports and Arts have more post published on wednesdays. This might be because of sports competitions organized thoses days, and the films are released on wednesdays.  
Also, a post is more likely to get a lot of comments in the future if the web crawler inspected it shortly after its publication. New posts get the more comments, but quickly get outdated.

### Predictions

The objective of our study is to predict the number of comment a post will get in the future. This is a regression problem. 

Before performing machine learning algorithms on our data, we have to prepare it. One hot encoding was unclear for data exploration, but now we should re-encode our categorical variables to be able to process them. Also, we use standard scaling on our numerical columns, to get scaled data.

To be able to get the best predictions, we try out multiple regression algorithms. For each algorithm, we perform a grid search to determine the best hyperparameters using a grid search. XGBoost performs the best with our data, but are far from perfect : social medias can be unpredictable
