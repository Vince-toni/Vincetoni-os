import httpx


def web_search(query: str, max_results: int = 3, **kwargs):
    """Lightweight web-search stub using DuckDuckGo Instant Answer API.

    This is a safe, read-only stub. It returns a small list of related topics/links when available.
    If the instant answer lacks links, results may be empty — this is intended as a first-pass tool.
    """
    try:
        url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}
        resp = httpx.get(url, params=params, timeout=5.0)
        data = resp.json()

        results = []
        for topic in data.get("RelatedTopics", []):
            # Some entries have nested Topics
            if "Text" in topic and "FirstURL" in topic:
                results.append({"title": topic.get("Text"), "url": topic.get("FirstURL")})
            elif "Topics" in topic:
                for t in topic.get("Topics", []):
                    if "Text" in t and "FirstURL" in t:
                        results.append({"title": t.get("Text"), "url": t.get("FirstURL")})

            if len(results) >= max_results:
                break

        return {"query": query, "results": results[:max_results]}
    except Exception as e:
        return {"error": str(e)}
