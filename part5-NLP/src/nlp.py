import os

import nltk


def get_sentences(filename):
    """

    """
    dir_path = os.path.dirname(os.path.realpath(__file__))

    try:
        results = []
        with open(os.path.join(dir_path, '..', filename)) as file:
            for line in file:
                results.append(nltk.sent_tokenize(line))

        return results

    except FileNotFoundError:
        print("File %s was not found." % filename)
        raise
    except Exception as e:
        print("Something terrible happened: %s", str(e))
        raise

def extract_subject(root):
    print(test)
