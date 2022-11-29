import nltk
import sys
import os
import math
import string
from collections import defaultdict

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dic = {}
    filenames = os.listdir(directory)
    for f  in filenames:
        path = os.path.join(directory, f)
        with open(path, "r") as content:
            values = content.read()
        dic[f] = values

    return dic  


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = []
    stopwords = []
    stopwords = nltk.corpus.stopwords.words("english")
    words = nltk.tokenize.casual.casual_tokenize(document, preserve_case=False)
    for word in words.copy():
        if word in string.punctuation:
            words.remove(word)
    words = [w for w in words if w not in stopwords]
    return words
        

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idf = {}
    appeared = set()
    total_doc = len(documents)
    for doc in documents:
        appeared.update(documents[doc])
    for word in appeared:
        number = 0
        for doc in documents:
            if word in documents[doc]:
                number += 1
        idf[word] = math.log(total_doc/ number)

    return idf
                    
                

                
def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """ 
    tfidf = dict.fromkeys(files.keys(),0)
    for f in files.keys():
        for word in query:
            tf = files[f].count(word)
            tfidf[f] += tf * idfs[word]

    topfiles = []   
    for i in range(n+1):
        maxfile = max(tfidf, key= lambda x: tfidf[x])
        topfiles.append(maxfile)
        del tfidf[maxfile]
    return topfiles


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranks = {}
    for s in sentences.keys():
        idf = 0
        termdensity = 0
        for word in query:
            if word in sentences[s]:
                idf += idfs[word]
                termdensity += 1/len(sentences[s])
        ranks[s] = (idf, termdensity)
        
    topS= [k for k, v in sorted(ranks.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)]
    return topS[:n]
        

if __name__ == "__main__":
    main()
