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
