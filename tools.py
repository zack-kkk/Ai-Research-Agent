import requests
import xml.etree.ElementTree as ET


# ----------------------------
# 1. WIKIPEDIA TOOL
# ----------------------------
def wikipedia_tool(query):
    try:
        # clean query
        clean_query = query.lower()

        if "vs" in clean_query:
            clean_query = clean_query.split("vs")[0]

        clean_query = clean_query.strip().replace(" ", "_").title()

        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{clean_query}"

        res = requests.get(url).json()

        return {
            "title": res.get("title"),
            "extract": res.get("extract")
        }

    except:
        return {}


# ----------------------------
# 2. ARXIV TOOL (RESEARCH PAPERS)
# ----------------------------
def arxiv_tool(query: str):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5"
    response = requests.get(url)

    root = ET.fromstring(response.text)
    papers = []

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        link = entry.find("{http://www.w3.org/2005/Atom}id").text

        papers.append({
            "title": title.strip(),
            "link": link
        })

    return papers


# ----------------------------
# 3. DUCKDUCKGO SEARCH (NO API KEY)
# ----------------------------
def web_search_tool(query: str):
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    response = requests.get(url).json()

    return {
        "abstract": response.get("Abstract", ""),
        "heading": response.get("Heading", ""),
        "source": response.get("AbstractURL", "")
    }


# ----------------------------
# 4. OPEN LIBRARY (BOOK DATA)
# ----------------------------
def books_tool(query: str):
    url = f"https://openlibrary.org/search.json?q={query}"
    response = requests.get(url).json()

    books = []

    for doc in response.get("docs", [])[:5]:
        books.append({
            "title": doc.get("title"),
            "author": doc.get("author_name", ["Unknown"])[0] if doc.get("author_name") else "Unknown"
        })

    return books


# ----------------------------
# 5. QUOTABLE (INSPIRATION CONTEXT)
# ----------------------------
def quote_tool():
    url = "https://api.quotable.io/random"
    response = requests.get(url).json()

    return {
        "quote": response.get("content"),
        "author": response.get("author")
    }
def books_tool(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=5"

    try:
        res = requests.get(url).json()
        books = []

        for item in res.get("items", []):
            info = item.get("volumeInfo", {})

            books.append({
                "title": info.get("title"),
                "authors": info.get("authors", []),
                "link": info.get("infoLink")
            })

        return books

    except:
        return []