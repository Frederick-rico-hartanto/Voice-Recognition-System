import webbrowser
from utils.speak import speak

# Function to perform a web search
def search_online(query):
    try:
        print(f"Searching online for: {query}")
        speak(f"Searching online for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    except Exception as e:
        print(f"Error performing search: {e}")
        speak("Error performing the search")
