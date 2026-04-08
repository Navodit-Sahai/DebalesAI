import os
import requests

SERP_API_KEY = os.getenv("SERP_API_KEY")



def search_web(query, k=5):
    if SERP_API_KEY:
        return serp_search(query, k)
    return duck_search(query, k)


def serp_search(query, k):
    try:
        res = requests.get(
            "https://serpapi.com/search",
            params={"q": query, "api_key": SERP_API_KEY, "num": k},
            timeout=10
        )
        data = res.json()

        results = data.get("organic_results", [])
        return "\n\n".join([
            f"{i+1}. {r.get('title')}\n{r.get('link')}\n{r.get('snippet')}"
            for i, r in enumerate(results)
        ]) or "No results found."

    except Exception as e:
        return f"Error: {e}"


def duck_search(query, k):
    try:
        res = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json"},
            timeout=10
        )
        data = res.json()

        results = []
        
        if data.get("AbstractText"):
            results.append("Summary: " + data["AbstractText"])

        for item in data.get("RelatedTopics", [])[:k]:
            if "Text" in item:
                results.append(item["Text"])

        return "\n\n".join(results) or "No results found."

    except Exception as e:
        return f"Error: {e}"