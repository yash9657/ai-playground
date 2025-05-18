from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
import requests  # For making HTTP requests to APIs and websites
from bs4 import BeautifulSoup
import json

load_dotenv(find_dotenv())

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
api_key = os.getenv("GOOGLE_API_KEY")
cse_id = os.getenv("CSE_ID")

search_query = "List the latest news in India and seperate them as Financial, Geopolitical, etc."

# Set Up a Search Engine to Provide Web Search Results
def search(search_item, api_key, cse_id, search_depth=10, site_filter=None):
    service_url = 'https://www.googleapis.com/customsearch/v1'

    params = {
        'q': search_item,
        'key': api_key,
        'cx': cse_id,
        'num': search_depth
    }

    try:
        response = requests.get(service_url, params=params)
        response.raise_for_status()
        results = response.json()

        # Check if 'items' exists in the results
        if 'items' in results:
            if site_filter is not None:

                # Filter results to include only those with site_filter in the link
                filtered_results = [result for result in results['items'] if site_filter in result['link']]

                if filtered_results:
                    return filtered_results
                else:
                    print(f"No results with {site_filter} found.")
                    return []
            else:
                if 'items' in results:
                    return results['items']
                else:
                    print("No search results found.")
                    return []

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the search: {e}")
        return []

# Identify the search term for the search engine
search_term = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Provide a google search term based on search query provided below in 3-4 words"},
        {"role": "user", "content": search_query}]
).choices[0].message.content

print(search_term)

# Now that we have the search term, we can use the Search API to get relevant results
# The results only have the link of the web page and a snippet at this point. 
search_items = search(search_item=search_term, api_key=api_key, cse_id=cse_id, search_depth=10)

for item in search_items:
    print(f"Link: {item['link']}")
    print(f"Snippet: {item['snippet']}\n")

# Build a search dictionary with titles, urls, and summaries of the web pages
TRUNCATE_SCRAPED_TEXT = 50000  # Adjust based on your model's context window
SEARCH_DEPTH = 5

# Scrape the content of the web page
def retrieve_content(url, max_tokens=TRUNCATE_SCRAPED_TEXT):
        try:
            headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/113.0.5672.127 Safari/537.36"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            for script_or_style in soup(['script', 'style']):
                script_or_style.decompose()

            text = soup.get_text(separator=' ', strip=True)
            characters = max_tokens * 4  # Approximate conversion
            text = text[:characters]
            return text
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve {url}: {e}")
            return None

def summarize_content(content, search_term, character_limit=500):
        prompt = (
            f"You are an AI assistant tasked with summarizing content relevant to '{search_term}'. "
            f"Please provide a concise summary in {character_limit} characters or less."
        )
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": content}]
            )
            summary = response.choices[0].message.content
            return summary
        except Exception as e:
            print(f"An error occurred during summarization: {e}")
            return None

# Create a structured search dictionary, this dictionary can be passed to the LLM to generate the summary
# with proper citations
def get_search_results(search_items, character_limit=500):
    # Generate a summary of search results for the given search term
    results_list = []
    for idx, item in enumerate(search_items, start=1):
        url = item.get('link')

        snippet = item.get('snippet', '')
        web_content = retrieve_content(url, TRUNCATE_SCRAPED_TEXT)

        if web_content is None:
            print(f"Error: skipped URL: {url}")
        else:
            summary = summarize_content(web_content, search_term, character_limit)
            result_dict = {
                'order': idx,
                'link': url,
                'title': snippet,
                'Summary': summary
            }
            results_list.append(result_dict)
    return results_list

results = get_search_results(search_items)

for result in results:
    print(f"Search order: {result['order']}")
    print(f"Link: {result['link']}")
    print(f"Snippet: {result['title']}")
    print(f"Summary: {result['Summary']}")
    print('-' * 80)



final_prompt = (
    f"The user will provide a dictionary of search results in JSON format for search query {search_term} Based on on the search results provided by the user, provide a detailed response to this query: **'{search_query}'**. Make sure to cite all the sources at the end of your answer."
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": final_prompt},
        {"role": "user", "content": json.dumps(results)}],
    temperature=0

)
summary = response.choices[0].message.content

print(summary)
