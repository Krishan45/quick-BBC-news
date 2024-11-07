from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to scrape BBC News headlines
def get_bbc_headlines():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    return [item.get_text(strip=True) for item in soup.find_all('h2')]

# Function to scrape NDTV headlines
def get_ndtv_headlines():
    url = 'https://www.ndtv.com/'
    response = requests.get(url)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    return [item.get_text(strip=True) for item in soup.find_all('h3')]

# Function to scrape The Hindu headlines
def get_hindu_headlines():
    url = 'https://www.thehindu.com/'
    response = requests.get(url)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    return [item.get_text(strip=True) for item in soup.find_all('h3')]

# Function to scrape The Economist headlines
def get_economist_headlines():
    url = 'https://www.economist.com/'
    response = requests.get(url)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = []

    for item in soup.find_all('h3'):
        text = item.get_text(strip=True)
        if text:
            headlines.append(text)

    return headlines

# Function to categorize headlines
def categorize_headlines():
    categories = {
        'Politics': [],
        'Health': [],
        'Environment': [],
        'Entertainment': [],
        'Crime': [],
        'Sports': [],
        'Technology': [],
        'Business': [],
        'Science': [],
        'Culture': [],
        'General': []
    }

    sources = {
        'BBC': get_bbc_headlines(),
        'NDTV': get_ndtv_headlines(),
        'The Hindu': get_hindu_headlines(),
        'The Economist': get_economist_headlines()
    }

    for source, headlines in sources.items():
        for headline in headlines:
            if not headline.strip():
                continue
            # Categorization logic
            if any(keyword in headline.lower() for keyword in ['election', 'government', 'political']):
                categories['Politics'].append((source, headline))
            elif any(keyword in headline.lower() for keyword in ['hurricane', 'climate']):
                categories['Environment'].append((source, headline))
            elif any(keyword in headline.lower() for keyword in ['health', 'covid']):
                categories['Health'].append((source, headline))
            elif any(keyword in headline.lower() for keyword in ['movie', 'music', 'entertainment']):
                categories['Entertainment'].append((source, headline))
            elif any(keyword in headline.lower() for keyword in ['kill', 'murder']):
                categories['Crime'].append((source, headline))
            elif any(keyword in headline.lower() for keyword in ['football', 'soccer', 'basketball', 'tennis']):
                categories['Sports'].append((source, headline))
            elif any(keyword in headline.lower() for keyword in ['technology', 'tech', 'gadget']):
                categories['Technology'].append((source, headline))
            elif any(keyword in headline.lower() for keyword in ['business', 'market', 'economy']):
                categories['Business'].append((source, headline))
            elif any(keyword in headline.lower() for keyword in ['science', 'research', 'discovery']):
                categories['Science'].append((source, headline))
            elif any(keyword in headline.lower() for keyword in ['culture', 'art', 'festival']):
                categories['Culture'].append((source, headline))
            else:
                categories['General'].append((source, headline))

    return {k: v for k, v in categories.items() if v}

@app.route('/')
def index():
    categorized_headlines = categorize_headlines()  # Get categorized headlines

    return render_template('index.html', categories=categorized_headlines)  # Pass categorized headlines to the template

if __name__ == '__main__':
    app.run(debug=True)
