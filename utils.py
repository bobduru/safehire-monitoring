import pandas as pd
from collections import defaultdict

def load_keywords(csv_path):
    """
    Load keywords and their categories from a CSV file.
    Assumes CSV has at least 'keyword' and 'category' columns.
    Returns:
        - keywords_dict: {keyword_lowercase: category}
        - keywords_context_str: formatted string for use in prompts
    """
    df = pd.read_csv(csv_path)

    # Build the keyword → category dictionary
    keywords_dict = {
        row["keyword"].strip().lower(): row["category"].strip()
        for _, row in df.iterrows()
        if pd.notna(row["keyword"]) and pd.notna(row["category"])
    }

    return keywords_dict

def create_prompt(add_keywords_context=True):
    """
    Create a prompt for text classification by reading from prompt.txt and optionally adding keyword context.
    Returns:
        - prompt: The formatted prompt string
        - labels: List of classification labels
    """
    # Read the base prompt from file
    with open("prompt2.txt", "r") as f:
        prompt_prefix = f.read()

    # labels = ["Hate Speech", "Radicalization", "Extremism", "Pedophilia", "Normal"]

    labels = ["Child Sexual Exploitation", "Radicalization", "Association with High-Risk Organisations", "Normal"]

    if add_keywords_context:
        # Load and process keywords
        keywords_dict = load_keywords("keywords2.csv")
        
        # Rebuild category → keywords mapping
        grouped_keywords = defaultdict(list)
        for keyword, category in keywords_dict.items():
            grouped_keywords[category].append(keyword)
        
        # Create keywords context string
        keywords_context = "For some more context here are keywords commonly used for the categories, you should flag a sentence with one of these keywords:\n"
        for label in labels:
            keywords = grouped_keywords.get(label, [])
            if keywords:
                keywords_context += f"{label}: {', '.join(keywords)}\n"
        keywords_context += "\n"
        
        # Replace the placeholder in the prompt
        prompt_prefix = prompt_prefix.replace("{keywords_context}", keywords_context)
    else:
        # Remove the keywords context placeholder if not adding keywords
        prompt_prefix = prompt_prefix.replace("{keywords_context}", "")

    return prompt_prefix, labels
