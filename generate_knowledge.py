import requests
from bs4 import BeautifulSoup
import json

# List of Think Round Inc. URLs to extract knowledge from
URLS = {
    "Mission": "https://www.thinkround.org/mission",
    "Programs": "https://www.thinkround.org/hardin-studios",
    "Paradise Project": "https://www.thinkround.org/the-center-for-the-human-family",
    "About Us": "https://www.thinkround.org/aboutus",
    "Home": "https://www.thinkround.org"
}

def fetch_page_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        return "\n".join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return ""

def build_knowledge_base():
    knowledge_entries = []
    
    for title, url in URLS.items():
        content = fetch_page_text(url)
        if content:
            entry = {
                "question": f"What does Think Round Inc. say about {title}?",
                "answer": content,
                "source": "Think Round Inc.",
                "category": title
            }
            knowledge_entries.append(entry)
    
    return knowledge_entries

if __name__ == "__main__":
    kb = build_knowledge_base()
    
    output_path = "data/knowledge_base.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(kb, f, indent=2, ensure_ascii=False)
    
    print(f"knowledge_base.json created with {len(kb)} entries.")
