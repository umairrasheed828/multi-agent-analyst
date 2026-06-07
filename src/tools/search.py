import time

from ddgs import DDGS


def web_search(query: str, max_results: int = 5, retries: int = 2) -> str:
    """Run a DuckDuckGo web search and return formatted snippets.

    Reliability: DuckDuckGo can rate-limit and return nothing, so we back off
    and retry. On total failure we return a marker string instead of raising,
    so one flaky tool call never crashes the whole agent graph.
    """
    for attempt in range(retries + 1):
        try:
            results = list(DDGS().text(query, max_results=max_results))
        except Exception as exc:  # network / rate-limit errors
            if attempt < retries:
                time.sleep(2)
                continue
            return f"[search failed: {exc}]"
        if results:
            lines = []
            for r in results:
                title = r.get("title", "").strip()
                body = r.get("body", "").strip()
                href = r.get("href", "") or r.get("url", "")
                lines.append(f"- {title}: {body} ({href})")
            return "\n".join(lines)
        if attempt < retries:
            time.sleep(2)  # likely rate-limited; back off and retry
    return "[no results found]"
