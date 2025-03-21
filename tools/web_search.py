from duckduckgo_search import DDGS

def search(topic):
    """Search the web for a topic and return concatenated text."""
    ddgs = DDGS()
    results = list(ddgs.text(topic, max_results=5))
    return " ".join([result['body'] for result in results])

def generate_email_from_search(recipient_name, email_subject, search_results, llm):
    """Generate an email body based on web search results."""
    prompt = f"Dear {recipient_name},\n\nHere is some information about {email_subject}:\n\n{search_results}\n\nBest regards,\nAI Agent"
    return prompt