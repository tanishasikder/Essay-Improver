from spacy.matcher import Matcher 

# Dictionary of the file names with keywords
keywords_dict = {
    "argumentative": "Words/argumentative.txt",
    "expository": "Words/expository.txt",
    "narrative": "Words/narrative.txt",
    "descriptive": "Words/descriptive.txt"
}

keywords_data = {}

def load_keywords():
    # Reading the files in the dictionary and putting them
    # In the new dictionary
    for word, filepath in keywords_dict.items():
        with open(filepath, 'r') as f:
            keywords_data[word] = f.read().splitlines()

def resume_score(file_content):
    matcher = Matcher(file_content.vocab)
    sizes = {}

    for key, value in keywords_data.items():
        essay_type = [{"LEMMA": {"IN": value}}]
        matcher.add(key, [[{"LEMMA": {"IN": essay_type}}]])

    for matcher_id in matcher:
        essay = matcher.get(matcher_id)
        sizes[essay] = len(essay[1])

    return max(sizes, key=sizes.get)