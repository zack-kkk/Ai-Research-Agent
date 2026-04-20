
#  AI Research Agent

An agentic AI system that autonomously gathers information from multiple sources and returns structured research output.

---

##  Features

* Multi-tool agent (Wikipedia, ArXiv, Web, Books)
* Dynamic tool selection (no fixed pipeline)
* Handles different query types:

  * General queries
  * Comparison queries (e.g., "X vs Y")
  * Book queries
* Structured output:

  * Summary
  * Research Papers
  * Books
  * Agent reasoning steps

---

##  Architecture

The system follows an **agentic loop**:

Plan → Act → Observe → Decide

* **Plan**: Choose which tool to use
* **Act**: Call APIs (Wikipedia, DuckDuckGo, ArXiv, Google Books)
* **Observe**: Evaluate usefulness of response
* **Decide**: Continue or stop

---

##  Tech Stack

* Backend: FastAPI
* Frontend: HTML + JavaScript
* APIs:

  * Wikipedia API
  * DuckDuckGo API
  * ArXiv API
  * Google Books API

---

##  How to Run

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Run backend:

```
uvicorn main:app --reload
```

3. Open frontend:

```
index.html
```

---

##  Output Example

* Summary of topic
* Research papers from ArXiv
* Recommended books
* Agent reasoning steps

---

##  Limitations

* Rule-based reasoning (not LLM-based)
* No memory (single query only)

---

##  Future Improvements

* Add LLM-based reasoning
* Add chat memory
* Rank sources by relevance
* Deploy online

---

##  Author

Sanjay M
