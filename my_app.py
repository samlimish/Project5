
import dash
import dash_core_components as dcc
import dash_html_components as html
from numpy.core.numeric import False_
import plotly.express as px
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
# %matplotlib inline
import matplotlib.image as mpimg
from PIL import Image
from wordcloud import WordCloud

# Bringing in csv files
old_tweet = pd.read_csv('old_twitter.csv')
new_tweet = pd.read_csv('new_twitter.csv')
stop_words = pd.read_csv('wordcloud_stopwords.csv')
stop_words = stop_words.iloc[:,1]
stop_words= stop_words.values.tolist()

# These are the main interaction between the app and the user. It allows the user to select the company that they want to see
# as well as the type of tweet (old, new, or both).
select_company = st.sidebar.selectbox('Select company', ['Apple', 'Google', 'Android'])#old_tweet['product or company'].unique())
select_time = st.sidebar.selectbox('Old, New, or Both', ['Old', 'New', 'Both'], key='time')

emotion_data=old_tweet[old_tweet['vader_emotion']==select_company]
# select_status = st.sidebar.multiselect('Consumer sentiment of the company', ('Negative','Neutral','Positive'), default=['Neutral'])
# Instead of letting people select the sentiment, decided to show everything at the same time. 
# First because people aren't going to be confsued if all three are displayed. 
# Two, because it would update/change the result of the word cloud even though nothing about the sentiment information was inputed
# to the word cloud function. 

# This is one of the two main functions of the app. It displays the ratio of the sentiment tweets to the whole.
# First it displayed raw numbers, but it was slightly difficult to compare how much the sentiments had changed. 
def to_dashboard(data):
    data=data[data['product or company']==select_company]
    my_tuple = (len(data[data['vader_emotion']=='Negative'])/len(data),
        len(data[data['vader_emotion']=='Neutral'])/len(data),
        len(data[data['vader_emotion']=='Positive'])/len(data))
    df = pd.DataFrame({
        'Emotion': ['Negative','Neutral','Positive'],
        'Ratio of Tweets' :my_tuple})
    return df
    
def return_graph(select_time):
    if select_time == 'Old':
        tweet = to_dashboard(old_tweet)
        titler= select_company+ ' Old Tweet'
        graph = px.bar(tweet, x='Emotion',
                        y='Ratio of Tweets', title=titler)
        st.plotly_chart(graph)
    elif select_time== 'New':
        tweet = to_dashboard(new_tweet)
        titler= select_company+ ' New Tweet'
        graph = px.bar(tweet, x='Emotion',
                        y='Ratio of Tweets', title=titler)
        st.plotly_chart(graph)
    elif select_time == 'Both':
        tweet1 = to_dashboard(old_tweet)
        titler1= select_company+ ' Old Tweet'
        graph1 = px.bar(tweet1, x='Emotion',
                        y='Ratio of Tweets', title=titler1)
        tweet2 = to_dashboard(new_tweet)
        titler2= select_company+ ' New Tweet'
        graph2 = px.bar(tweet2, x='Emotion',
                        y='Ratio of Tweets', title= titler2)
        st.plotly_chart(graph1)
        st.plotly_chart(graph2)


def wordcloud_generator(text, cmap=None, stopwords=', '.join(str(stop) for stop in stop_words), min_font=12, colloc=True, title='Word Cloud'):

    cloud = WordCloud(colormap=cmap, stopwords=stopwords, width=650, height=400, min_font_size=min_font,
                      collocations=colloc).generate_from_text(' '.join(text))
    fig, ax = plt.subplots(figsize=(12,7))
    ax.imshow(cloud)
    ax.set_axis_off()
    ax.margins(x=0, y=0)
    ax.axis('off')
    st.image(cloud.to_array(), caption=title)

def wc_plot(select_company):

    wordcloud_generator(text=old_tweet[old_tweet['product or company']==select_company]['clean_text'], 
    cmap='Set1', title=f'Word Cloud Old Tweet {select_company}', stopwords=stop_words)
    
    wordcloud_generator(text=new_tweet[new_tweet['product or company']==select_company]['clean_text'], 
    cmap='Set1', title=f'Word Cloud New Tweet {select_company}', stopwords=stop_words)

if st.sidebar.checkbox('Show tweet emotion by company', True, key='2'):
    st.markdown('## **Comparison of Twitter Sentiment Analysis by Company**')
    return_graph(select_time)

if st.sidebar.checkbox('Show Wordcloud', True):
    st.markdown('## **Wordcloud**')
    wc_plot(select_company)