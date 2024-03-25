import os
import requests
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()

BING_SEARCH_KEY = os.getenv("BING_SEARCH_KEY")
BING_SEARCH_V7_ENDPOINT = os.getenv("BING_SEARCH_V7_ENDPOINT")

class SearchTools():

    @tool("Search the internet using Bing")
    def search_internet(query):
        """Search the internet using Bing and return relevant results"""
        endpoint = f"{BING_SEARCH_V7_ENDPOINT}/v7.0/search"
        params = {'q': query, 'mkt': 'en-US'}
        headers = {'Ocp-Apim-Subscription-Key': BING_SEARCH_KEY}

        try:
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            search_results = response.json()

            formatted_results = []
            for result in search_results.get('webPages', {}).get('value', []):
                formatted_result = {
                    "Title": result.get('name', ''),
                    "Link": result.get('url', ''),
                    "Snippet": result.get('snippet', ''),
                }
                formatted_results.append(formatted_result)

            return formatted_results
        except Exception as ex:
            return f"An error occurred: {ex}"
