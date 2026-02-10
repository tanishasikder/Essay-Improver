import sys
import os

from essay_fixer import process_user_file

if __name__== "__main__":
    if len(sys.argv) < 2:
        print("No file given. Try again.")
        sys.exit(1)

    input_file = sys.argv[1]
    doc = process_user_file(input_file)
    print(doc)


#https://www.geeksforgeeks.org/nlp/spacy-for-natural-language-processing/
#https://machinelearningplus.com/spacy-tutorial-nlp/#howpostagginghelpsyouindealingwithtextbasedproblems
#https://chatgpt.com/c/6977f2ad-960c-8327-9b94-4f688e3b34c3