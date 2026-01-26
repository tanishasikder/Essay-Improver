import sys
import os

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
    
    except IOError as e:
        print(f"Sorry. Error reading {file}")
        sys.exit(1)

if __name__== "__main__":
    if len(sys.argv) < 2:
        print("No file given. Try again.")
        sys.exit(1)

    input_file = sys.argv[1]
    process_user_file(input_file)