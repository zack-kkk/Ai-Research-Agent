from tools import wikipedia_tool, arxiv_tool, web_search_tool, books_tool


def is_books_query(query):
    q = query.lower()
    return "book" in q or "books" in q


def decide_next_action(step, knowledge, tried):
    if step == 0 and "wiki" not in tried:
        return "wiki"

    if len(knowledge) < 500 and "web" not in tried:
        return "web"

    if "arxiv" not in tried:
        return "arxiv"

    return "stop"


def run_agent(query: str):

    # 📚 HANDLE BOOK QUERIES FIRST (IMPORTANT FIX)
    if is_books_query(query):

        books = books_tool(query)

        summary = "Here are some recommended books:\n\n"

        for b in books[:5]:
            title = b.get("title", "Unknown")
            authors = ", ".join(b.get("authors", [])) if b.get("authors") else "Unknown"
            summary += f"- {title} by {authors}\n"

        return {
            "query": query,
            "steps": ["Detected books query", "Fetched books directly"],
            "summary": summary,
            "insights": [
                "Books provide structured and in-depth knowledge.",
                "Recommended titles are based on relevance.",
                "Ideal for beginners and advanced learners."
            ],
            "papers": [],
            "books": books,
            "sources": ["Google Books"]
        }

    # 🔥 HANDLE COMPARISON QUERIES
    if "vs" in query.lower():
        parts = query.split("vs")
        topic1 = parts[0].strip()
        topic2 = parts[1].strip()

        wiki1 = wikipedia_tool(topic1)
        wiki2 = wikipedia_tool(topic2)

        summary = f"{topic1}:\n{wiki1.get('extract','No data found')}\n\n{topic2}:\n{wiki2.get('extract','No data found')}"

        return {
            "query": query,
            "steps": ["Detected comparison query"],
            "summary": summary,
            "insights": ["Comparison between two topics"],
            "papers": [],
            "books": [],
            "sources": ["Wikipedia"]
        }

    # 🧠 NORMAL AGENT FLOW
    state = {
        "query": query,
        "steps": [],
        "knowledge": "",
        "papers": [],
        "sources": set(),
        "tried_tools": set()
    }

    max_steps = 5

    for step in range(max_steps):

        action = decide_next_action(step, state["knowledge"], state["tried_tools"])

        if action == "stop":
            state["steps"].append("Stopping: No more tools needed")
            break

        state["steps"].append(f"Step {step+1}: Using {action}")
        state["tried_tools"].add(action)

        if action == "wiki":
            result = wikipedia_tool(query)
            text = result.get("extract", "")
            state["sources"].add("Wikipedia")

            if text:
                state["knowledge"] += text + "\n"

        elif action == "web":
            result = web_search_tool(query)
            text = result.get("abstract", "")
            state["sources"].add("DuckDuckGo")

            if text and len(text) > 50:
                state["knowledge"] += text + "\n"

        elif action == "arxiv":
            papers = arxiv_tool(query)
            state["papers"] = papers[:5]
            state["sources"].add("ArXiv")

        if action != "arxiv":
            if text:
                state["steps"].append(f"{action} gave useful data")
            else:
                state["steps"].append(f"{action} gave no data")

        if len(state["knowledge"]) > 1000:
            state["steps"].append("Enough data collected")
            break

    # 📚 FETCH BOOKS (secondary)
    books = books_tool(query)
    state["steps"].append("Fetched books")

    # 🧾 SUMMARY FIX
    if state["knowledge"]:
        summary = state["knowledge"][:1200]
    else:
        summary = "No useful summary found. Try a more specific query."

    return {
        "query": query,
        "steps": state["steps"],
        "summary": summary,
        "insights": ["Combined multiple sources"],
        "papers": state["papers"],
        "books": books,
        "sources": list(state["sources"])
    }