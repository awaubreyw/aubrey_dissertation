#CREDIT Aufar Laksana https://gist.github.com/alaksana96/3bbec4503a3aec64517cd8e408075678

import json

def search(search_string, inverted_index):
    """
    This function takes a string as the first parameter and an inverted index as the second parameter.
    It then searches the string in the inverted index
    It will always try to return at least one result
    This is an example of a very simple search algorithm
    """
    # Its important to lowercase so that we can match things like "Visual" and "visual"
    tokens = search_string.lower().split() # Split on spaces e.g. ['How', 'to', 'lie', 'using', 'visual', 'proofs']

    document_set = {}
    for token in tokens:
        if token in inverted_index.keys():
            if document_set == {}:
                document_set = inverted_index[token]
            else:
                intersect = set.intersection(document_set, inverted_index[token])
                document_set = intersect if len(intersect) > 0 else document_set
            
    return document_set


# load the inverted indexes
# We also convert the lists back to sets (for faster lookup and uniqueness)
with open("title_inverted_index.json", "r") as f:
    loaded_index = json.load(f)
    TITLE_INVERTED_INDEX = {k : set(v) for k, v in loaded_index.items()}

with open("description_inverted_index.json", "r") as f:
    loaded_index = json.load(f)
    DESCRIPTION_INVERTED_INDEX = {k : set(v) for k, v in loaded_index.items()}

            
# You can search across the titles only
print(f"Search across titles only\n{search('visual proofs', TITLE_INVERTED_INDEX)}\n")

# Or you can search across the descriptions
print(f"Search across descriptions only\n{search('visual proofs', DESCRIPTION_INVERTED_INDEX)}\n")

# Or you could search across both
titles = search("visual proofs", TITLE_INVERTED_INDEX)
descriptions = search("visual proofs", DESCRIPTION_INVERTED_INDEX)
print(f"Search across titles and descriptions:\n{set.union(titles, descriptions)}\n")