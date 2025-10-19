import streamlit as st
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
import tweepy
import os

# Download stopwords once, using Streamlit's caching
@st.cache_resource
def load_stopwords():
    nltk.download('stopwords')
    return stopwords.words('english')

# Load model and vectorizer once
@st.cache_resource
def load_model_and_vectorizer():
    with open('./models/sentiment_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('./models/vectorizer.pkl', 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
    return model, vectorizer

# Initialize Twitter API client
@st.cache_resource
def init_twitter_client():
    # Get credentials from environment variables or Streamlit secrets
    bearer_token = st.secrets.get("TWITTER_BEARER_TOKEN", os.getenv("TWITTER_BEARER_TOKEN"))
    
    if not bearer_token:
        return None
    
    return tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

# Define sentiment prediction function
def predict_sentiment(text, model, vectorizer, stop_words):
    # Preprocess text
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower()
    text = text.split()
    text = [word for word in text if word not in stop_words]
    text = ' '.join(text)
    text = [text]
    text = vectorizer.transform(text)
    
    # Predict sentiment
    sentiment = model.predict(text)
    return "Negative" if sentiment == 0 else "Positive"

# Function to fetch tweets using tweepy
def fetch_tweets(client, username, num_tweets=5):
    """
    Fetch tweets from a Twitter user using tweepy
    """
    try:
        # Get user by username
        user = client.get_user(username=username)
        if not user:
            return None, "User not found"
        
        # Fetch user tweets
        tweets = client.get_users_tweets(
            id=user.data.id,
            max_results=min(num_tweets, 100),
            tweet_fields=['created_at', 'public_metrics']
        )
        
        if not tweets.data:
            return [], "No tweets found"
        
        tweet_texts = [tweet.text for tweet in tweets.data]
        return tweet_texts, None
        
    except tweepy.TweepyException as e:
        return None, f"API Error: {str(e)}"
    except Exception as e:
        return None, f"Error: {str(e)}"

# Function to create a colored card
def create_card(tweet_text, sentiment):
    color = "green" if sentiment == "Positive" else "red"
    card_html = f"""
    <div style="background-color: {color}; padding: 10px; border-radius: 5px; margin: 10px 0;">
        <h5 style="color: white;">{sentiment} Sentiment</h5>
        <p style="color: white;">{tweet_text}</p>
    </div>
    """
    return card_html

# Main app logic
def main():
    st.title("Twitter Sentiment Analysis")

    # Load stopwords and model/vectorizer only once
    stop_words = load_stopwords()
    model, vectorizer = load_model_and_vectorizer()

    # Initialize Twitter client
    client = init_twitter_client()

    # User input: either text input or Twitter username
    option = st.selectbox("Choose an option", ["Input text", "Get tweets from user"])
    
    if option == "Input text":
        text_input = st.text_area("Enter text to analyze sentiment")
        if st.button("Analyze"):
            if text_input.strip():
                sentiment = predict_sentiment(text_input, model, vectorizer, stop_words)
                st.success(f"Sentiment: **{sentiment}**")
            else:
                st.warning("Please enter some text to analyze.")

    elif option == "Get tweets from user":
        if not client:
            st.error("❌ Twitter API not configured!")
            st.info("""
            ### Setup Instructions:
            1. Get a free Twitter API key: https://developer.twitter.com/en/portal/dashboard
            2. Create a `secrets.toml` file in `.streamlit/` folder with:
            ```
            TWITTER_BEARER_TOKEN = "your_bearer_token_here"
            ```
            3. Restart the app
            """)
            return
        
        username = st.text_input("Enter Twitter username (without @)")
        num_tweets = st.slider("Number of tweets to fetch", 1, 20, 5)
        
        if st.button("Fetch Tweets"):
            if not username.strip():
                st.warning("Please enter a username.")
                return
            
            with st.spinner(f"Fetching tweets from @{username}..."):
                tweets, error = fetch_tweets(client, username, num_tweets)
            
            if error:
                st.error(f"❌ {error}")
            elif tweets:
                st.success(f"✅ Found {len(tweets)} tweets")
                for i, tweet_text in enumerate(tweets, 1):
                    sentiment = predict_sentiment(tweet_text, model, vectorizer, stop_words)
                    card_html = create_card(tweet_text, sentiment)
                    st.markdown(card_html, unsafe_allow_html=True)
            else:
                st.error(f"No tweets found for @{username}.")

if __name__ == "__main__":
    main()