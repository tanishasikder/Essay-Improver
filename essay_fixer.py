import sys
import os
import spacy
from spacy.tokens import Doc
from spacy.matcher import Matcher 
import language_tool_python
import train_model

nlp = spacy.load("en_core_web_sm")

def process_user_file(file):
    # Making sure the file exists and is a .txt file
    if not os.path.exists(file):
        print(f"Sorry. {file} does not exist.")
        sys.exit(1)

    if not file.lower().endswith('.txt'):
        sys.exit(1)
    
    try:
        # Open and read the user's file
        with open(file, 'r') as f:

            content = f.read()
            # Tokenizes, does segmentation, pos_tag,
            # Lemmatization, dependency parsing, and NER
            doc = nlp(content)
            language_tool = language_tool_python.LanguageTool('en-US')
            words = []

            for word in doc:
                # Checks if it is alphabetic or a stop word
                words.append(language_tool.check(word))

            return words
    
    except IOError as e:
        print(f"Sorry. Error reading {file}")
        sys.exit(1)

def passive_voice_checker(file_content):
    for token in file_content:
        passive_content = []
        if token.dep_ == "auxpass" or token.dep_ == "nsubjpass":
            passive_content.append(token.text)
        return passive_content

def store_output(file_content, match):
    passive = passive_voice_checker(file_content)

    info = {
        'resolution' : match.message,
        'replace' : match.replacements,
        'context' : match.context,
        'issue' : match.ruleIssueType,
        'passive_voice' : passive
    }
    return info