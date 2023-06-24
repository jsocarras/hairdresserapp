import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import feedparser
from googleapiclient.discovery import build

PEXELS_API_KEY = 'zHYOVYb0iG4HAWwxwUZVuLjsdYtzYJ2uEL2k3y8rB4sJLnZIMgXqVj5u'
YOUTUBE_API_KEY = 'AIzaSyBJs_RpW2lZZXCCMNCOzkrceraaRekFUZg'
RSS_FEED_URL = 'https://rss.app/feeds/v1.1/Pqdhy4a54LBx8OUB.json'

def get_images():
    headers = {'Authorization': PEXELS_API_KEY}
    url = "https://api.pexels.com/v1/search?query=latest+hairstyle+trends&per_page=15"
    response = requests.get(url, headers=headers)
    data = response.json()
    return [photo['src']['medium'] for photo in data['photos']]

def get_tutorials():
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        part="snippet",
        maxResults=10,
        q="hairdressing tutorial latest trends"
    )
    response = request.execute()
    return ['https://www.youtube.com/watch?v=' + item['id']['videoId'] for item in response['items']]

def get_articles():
    feed = feedparser.parse(RSS_FEED_URL)
    return [{'title': entry['title'], 'url': entry['link'], 'summary': entry['summary']} for entry in feed['entries']]

def main():
    st.title("Hairdresser's Trend & Upskill Portal")

    st.sidebar.title("Navigation")
    choice = st.sidebar.selectbox("Choose a section", ["Trending Styles", "Video Tutorials", "Latest Articles", "Community"])

    if choice == "Trending Styles":
        st.subheader("Latest Trends in Hairstyles")

        images = get_images()
        for img_url in images:
            response = requests.get(img_url)
            img = Image.open(BytesIO(response.content))
            st.image(img, caption=img_url)

    elif choice == "Video Tutorials":
        st.subheader("Video Tutorials")

        tutorials = get_tutorials()
        for video in tutorials:
            st.video(video)

    elif choice == "Latest Articles":
        st.subheader("Latest Articles")

        articles = get_articles()
        for article in articles:
            st.write(f"[{article['title']}]({article['url']})")
            st.write(article['summary'])

    elif choice == "Community":
        st.subheader("Community")
        st.write("Join the discussion at [Hairdresser's Forum](forum_link)")

if __name__ == "__main__":
    main()
