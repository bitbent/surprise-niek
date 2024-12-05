import requests
from bs4 import BeautifulSoup

def get_definition(word):
    # Base URL for Encyclo's search
    base_url = "https://www.encyclo.co.uk/search.php"
    params = {"q": word}  # Query parameter for the word
    
    try:
        # Send a GET request
        response = requests.get(base_url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Locate the section containing the definitions
            definitions = soup.find_all('div', class_='def')  # Adjust class name if structure changes
            
            # Check if any definitions were found
            if definitions:
                # Extract and return all definitions as a list
                result = [definition.get_text(strip=True) for definition in definitions]
                return {
                    "word": word,
                    "status": "Found",
                    "definitions": result
                }
            else:
                return {
                    "word": word,
                    "status": "Not Found",
                    "definitions": "No definitions found for this word."
                }
        else:
            return {
                "word": word,
                "status": "Error",
                "definitions": f"HTTP Error {response.status_code}"
            }
    except Exception as e:
        return {
            "word": word,
            "status": "Error",
            "definitions": str(e)
        }

# Example usage
word = "Python"
result = get_definition(word)
print(result)
