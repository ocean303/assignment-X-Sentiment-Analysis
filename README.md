# Twitter Sentiment Analysis

A Streamlit-based web application that performs sentiment analysis on tweets and user-provided text using machine learning. The app can analyze individual text inputs or fetch and analyze tweets directly from Twitter users.

## Features

- **Text Analysis**: Analyze sentiment of any custom text input
- **Twitter Integration**: Fetch and analyze tweets from any public Twitter user
- **Real-time Predictions**: Get instant sentiment predictions (Positive/Negative)
- **Visual Cards**: Color-coded results for easy interpretation (green for positive, red for negative)
- **Pre-trained Model**: Uses a pre-trained sentiment classification model
- **Rate Limiting**: Built-in API rate limiting handling for Twitter requests

## Prerequisites

Before you begin, ensure you have the following:

- Python 3.8 or higher
- pip (Python package manager)
- Twitter API credentials (for Twitter integration)

## Installation

1. **Clone the repository**
```bash
https://github.com/ocean303/assignment-X-Sentiment-Analysis.git
cd twitter-sentiment-analysis
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up Twitter API credentials** (Optional, only if using Twitter integration)
   - Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
   - Create a new application and generate a Bearer Token
   - Create a `.streamlit/secrets.toml` file in your project directory:
   ```toml
   TWITTER_BEARER_TOKEN = "your_bearer_token_here"
   ```
   - Alternatively, set the environment variable:
   ```bash
   export TWITTER_BEARER_TOKEN="your_bearer_token_here"
   ```

## Project Structure

```
.
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── models/
│   ├── sentiment_model.pkl         # Pre-trained sentiment model
│   └── vectorizer.pkl              # TF-IDF vectorizer
└── .streamlit/
    └── secrets.toml               # Twitter API credentials (create this)
```

## Usage

1. **Run the Streamlit app**
```bash
streamlit run app.py
```

2. **Open the application**
   - Your default browser will open to `http://localhost:8501`

3. **Choose an analysis mode**
   - **Input Text**: Enter any text and click "Analyze" to get sentiment prediction
   - **Get Tweets from User**: Enter a Twitter username and fetch their recent tweets for analysis

## How It Works

The application follows these steps:

1. **Text Preprocessing**:
   - Removes special characters and numbers
   - Converts to lowercase
   - Removes English stopwords
   - Tokenizes and cleans the text

2. **Vectorization**:
   - Uses TF-IDF (Term Frequency-Inverse Document Frequency) to convert text to numerical features

3. **Prediction**:
   - Feeds the vectorized text to the pre-trained sentiment model
   - Returns either "Positive" or "Negative" sentiment

4. **Visualization**:
   - Displays results in color-coded cards for easy interpretation

## Dependencies

- **streamlit**: Web app framework
- **scikit-learn**: Machine learning library
- **nltk**: Natural language processing
- **tweepy**: Twitter API client
- **pandas**: Data manipulation

See `requirements.txt` for specific version requirements.

## API Configuration

### Twitter API Setup

To use the Twitter integration feature:

1. Visit [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new project and app
3. Generate API keys and select "Bearer Token"
4. Add your Bearer Token to `.streamlit/secrets.toml` or environment variables

Note: If the Twitter API is not configured, the app will still work with text input mode.

## Troubleshooting

**Issue**: "Twitter API not configured!"
- **Solution**: Ensure your Bearer Token is correctly set in `.streamlit/secrets.toml` or as an environment variable

**Issue**: "User not found"
- **Solution**: Check that the Twitter username is correct and the account is public

**Issue**: "No tweets found"
- **Solution**: The user may have no public tweets or tweets may be protected

**Issue**: Module import errors
- **Solution**: Reinstall dependencies with `pip install -r requirements.txt`

## Model Information

The sentiment model is a binary classifier trained to distinguish between positive and negative sentiments. The model uses the TF-IDF vectorizer for text feature extraction and is serialized using pickle for easy loading.


**Happy Analyzing! 🚀**
