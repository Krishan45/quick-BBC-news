import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox, scrolledtext

def scrape_headlines():
    url = "https://www.bbc.com/news"  # Set the URL directly
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Define keywords for classification
    categories = {
        'Sports': ['sport', 'football', 'basketball', 'cricket', 'tennis'],
        'Politics': ['politics', 'government', 'election', 'policy', 'senate', 'congress'],
        'Technology': ['technology', 'tech', 'gadget', 'AI', 'innovation'],
        'Health': ['health', 'medicine', 'virus', 'disease', 'treatment'],
        'Entertainment': ['entertainment', 'movie', 'music', 'celebrity', 'TV'],
        'War': ['war', 'conflict', 'military', 'battle', 'troops'],
        'Country': ['country', 'nation', 'state', 'government'],
        'Fun': ['fun', 'games', 'amusement', 'comedy', 'entertainment'],
        'Art': ['art', 'painting', 'sculpture', 'gallery', 'exhibition']
    }

    # Initialize the dictionary to store classified headlines
    classified_headlines = {category: [] for category in categories}
    classified_headlines['Miscellaneous'] = []  # Add a miscellaneous category for unmatched headlines

    try:
        # Request the website
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the news headlines from the HTML
        headlines = soup.find_all('h2')  # Assuming 'h2' contains the headlines

        # Classify headlines based on keywords
        for i in headlines:
            headline_text = i.text.strip()
            
            # Skip unwanted sections
            if "More" in headline_text or "Follow BBC on" in headline_text:
                continue

            categorized = False

            for category, keywords in categories.items():
                if any(keyword.lower() in headline_text.lower() for keyword in keywords):
                    classified_headlines[category].append(headline_text)
                    categorized = True
                    break
            
            # If no category matched, add to 'Miscellaneous'
            if not categorized:
                classified_headlines['Miscellaneous'].append(headline_text)

        return classified_headlines  # Return the classified headlines

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to scrape the URL: {e}")
        return None

def show_headlines():
    headlines = scrape_headlines()  # Scrape headlines
    if headlines:
        output_window = tk.Toplevel()  # Create a new window
        output_window.title("BBC News Headlines")

        text_area = scrolledtext.ScrolledText(output_window, wrap=tk.WORD, width=80, height=20)
        text_area.pack(padx=10, pady=10)

        text_area.insert(tk.END, "=== BBC News Headlines ===\n\n")

        # Display all classified headlines, skipping empty categories
        for category, items in headlines.items():
            if items:  # Only print categories that have headlines
                text_area.insert(tk.END, f"--- {category} Headlines: ---\n")
                for item in items:
                    text_area.insert(tk.END, f" - {item}\n")
                text_area.insert(tk.END, "\n")  # Print a newline for better separation

        text_area.configure(state='disabled')  # Make text area read-only

def main():
    root = tk.Tk()
    root.title("News Scraper")

    # Create a button to scrape headlines
    scrape_button = tk.Button(root, text="Get BBC News Headlines", command=show_headlines)
    scrape_button.pack(pady=20)

    root.geometry("300x150")
    root.mainloop()

if __name__ == "__main__":
    main()
