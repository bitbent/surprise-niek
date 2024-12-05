import requests
from bs4 import BeautifulSoup
import os

def scrape_definition(word):
    base_url = "https://www.encyclo.co.uk/search.php"
    params = {"q": word}  # Query parameter for the word
    
    try:
        # Send a GET request to the search page
        response = requests.get(base_url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the section containing the definitions
            definitions = soup.find_all('div', class_='def')
            
            if definitions:
                return [definition.get_text(strip=True) for definition in definitions]
            else:
                return ["No definitions found."]
        else:
            return [f"Error: Received HTTP status code {response.status_code}"]
    except Exception as e:
        return [f"Error: {str(e)}"]

def generate_static_page(word, definitions):
    # Create a simple static HTML page
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Definition of {word}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 20px;
                padding: 20px;
                background-color: #f9f9f9;
                color: #333;
            }}
            h1 {{
                color: #555;
            }}
            ul {{
                list-style-type: disc;
                margin: 20px 0;
                padding-left: 40px;
            }}
        </style>
    </head>
    <body>
        <h1>Definition of "{word}"</h1>
        <ul>
            {"".join(f"<li>{definition}</li>" for definition in definitions)}
        </ul>
        <a href="index.html">Back to Search</a>
    </body>
    </html>
    """
    # Write the HTML to a file
    with open(f"output/{word}.html", "w", encoding="utf-8") as file:
        file.write(html_content)

def main():
    # Create the output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Input word to search
    word = input("Enter a word to look up: ")
    definitions = scrape_definition(word)
    
    # Generate a static HTML page
    generate_static_page(word, definitions)
    print(f"Definitions for '{word}' have been saved to 'output/{word}.html'.")

if __name__ == "__main__":
    main()
