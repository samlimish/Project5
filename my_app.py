
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
# %matplotlib inline
import matplotlib.image as mpimg
from PIL import Image
from wordcloud import WordCloud


old_tweet = pd.read_csv('old_twitter')
new_tweet = pd.read_csv('new_twitter')
old_pos = pd.read_csv('old_pos')
old_neg = pd.read_csv('old_neg')
old_neut = pd.read_csv('old_neut')
new_pos = pd.read_csv('new_pos')
new_neg = pd.read_csv('new_neg')
new_neut = pd.read_csv('new_neut')
stop_words = pd.read_csv('wordcloud_stopwords')
stop_words= stop_words.values.tolist()


# Using select_company and select_status, create wordclouds based on user's choices. 
# Make a checkbox that if checked will show just word clouds and not the number of tweets.
# Also display the bargraph that shows the frequency of the words


select_company = st.sidebar.selectbox('Select company', old_tweet['product or company'].unique())
select_time = st.sidebar.select_slider('Old or New', ['Old', 'New'], key='time')

emotion_data=old_tweet[old_tweet['vader_emotion']==select_company]
select_status = st.sidebar.multiselect('Consumer sentiment of the company', ('Negative','Neutral','Positive'))

def to_dashboard(data):
    data=data[data['product or company']==select_company]
    if len(select_status) == 0:
        pass
    if len(select_status) == 1:
        # status_list=[select_status[0]]
        my_tuple = (len(data[data['vader_emotion']==select_status[0]]))
        df = pd.DataFrame({
        'Emotion': select_status,
        'Number of Tweets' :my_tuple})
        return df
    elif len(select_status) == 2:
        my_tuple = (len(data[data['vader_emotion']==select_status[0]]),
        len(data[data['vader_emotion']==select_status[1]]))
        df = pd.DataFrame({
        'Emotion': select_status,
        'Number of Tweets' :my_tuple})
        return df
    elif len(select_status) == 3:
        my_tuple = (len(data[data['vader_emotion']==select_status[0]]),
        len(data[data['vader_emotion']==select_status[1]]),
        len(data[data['vader_emotion']==select_status[2]]))
        df = pd.DataFrame({
        'Emotion': select_status,
        'Number of Tweets' :my_tuple})
        return df
# Fix so that it only displays either a single emotion or multiple emotions that can be chosen
# Fix so that only one company is shown at a time unless there is enough time to allow multiple companies 
# to be displayed at the same time



if st.sidebar.checkbox('Show tweet emotion by company', True, key='2'):
    st.markdown('## **Comparison of Twitter Sentiment Analysis by Company**')
    if select_time == 'Old':#st.get_option('time') == 'Old':
        tweet = to_dashboard(old_tweet)
        graph = px.bar(tweet, x='Emotion',
                        y='Number of Tweets')
    elif select_time== 'New':#st.get_option('time') == 'New':
        tweet = to_dashboard(new_tweet)
        graph = px.bar(tweet, x='Emotion',
                        y='Number of Tweets')
    st.plotly_chart(graph)
def wordcloud_generator(text, cmap=None, stopwords=','.join(str(stop) for stop in stop_words), min_font=12, n_grams=True, title='Word Cloud'):
    st.write(select_status)
    cloud = WordCloud(colormap=cmap, stopwords=stopwords, width=650, height=400, min_font_size=min_font,\
                      collocations=n_grams).generate_from_text(text)#(' '.join(text))
    fig, ax = plt.subplots(figsize=(12,7))
    ax.imshow(cloud)
    ax.set_axis_off()
    ax.set_title=(title)
    ax.margins(x=0, y=0)
    ax.axis('off')
    st.image(cloud.to_array())


if st.sidebar.checkbox('Show Wordcloud', True):
    st.markdown('## **Wordcloud**')
    
    if select_time == 'Old':
        text1 = old_tweet[(old_tweet['product or company']==select_company)].copy()
        
        for status in select_status:
            text=""
            text2 = text1.loc[text1['vader_emotion']==status].copy()
            # print(type(' '.join(text2['clean_text'])))
            text += ','.join(text2['clean_text'])
            wordcloud_generator(text, cmap='Set1')
    elif select_time == 'New':
        text1 = new_tweet[(new_tweet['product or company']==select_company)].copy() 
        for status in select_status:
            text=""
            text2 = text1.loc[text1['vader_emotion']==status].copy()

            text += ','.join(text2['clean_text'])
            wordcloud_generator(text, cmap='Set1')


