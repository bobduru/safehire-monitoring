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
        prompt_prefix = (
            "You are a safety classifier that carefully analyzes text for potential risks. "
            "For every input, classify it strictly into one of the following categories:\n\n"
            "- Hate Speech: Any content that promotes, incites, or supports violence, discrimination, or hostility against individuals or groups based on attributes such as race, religion, gender, sexual orientation, disability, or nationality.\n"
            "- Radicalization: Any content that encourages or supports extremist ideological beliefs, recruitment into extremist groups, or the justification of violence for ideological, religious, or political motives.\n"
            "- Extremism: Any content that advocates for extreme political views, including incitement to overthrow governments, promoting authoritarianism, suppressing rights through violence, or endorsing terrorism.\n"
            "- Pedophilia: Be the most cautious with this one — any content that implies, suggests, normalizes, or discusses sexual interest in minors, grooming, or child exploitation. But also remember that these sentences are by adults, so anything that sounds too cute or childish should be flagged. Anything related to pornography (websites, videos, etc) should also be flagged. Better be too cautious than miss one.\n"
            "- Normal: If the text does not contain any of the above risks.\n\n"
            
        )

        labels = ["Hate Speech", "Radicalization", "Extremism", "Pedophilia", "Normal"]

        keywords_dict = load_keywords("keywords.csv")
    
        if add_keywords_context:
            # Rebuild category → keywords mapping from the flat dictionary
            grouped_keywords = defaultdict(list)
            for keyword, category in keywords_dict.items():
                grouped_keywords[category].append(keyword)
        
            prompt_prefix += "For some more context here are keywords commonly used for the categories, you should flag a sentence with one of these keywords:\n"
            for label in labels:
                keywords = grouped_keywords.get(label, [])
                if keywords:
                    prompt_prefix += f"{label}: {', '.join(keywords)}\n"
            prompt_prefix += "\n"
            

        # prompt_prefix += "Most of the time, the text will be web searches, so some of them can have weird characters or even be blank. "\
        #     "If you can't make sense of the text, and it doesn't look suspicious, just output 'Normal'.\n"
        prompt_prefix += "Instructions: Classify the following text in between <classify> tags and output only one of the labels : Hate Speech, Radicalization, Extremism, Pedophilia or Normal in between the <label> tags\n"
        prompt_prefix += "If you can't make sense of the text, and it doesn't look suspicious, just output <label>Normal</label>.\n"
        

        prompt = prompt_prefix + "Text to classify: <classify>{text}</classify>\nLabel: <label>"
        # prompt = "Tell me a story about a cat"
        return prompt, labels
