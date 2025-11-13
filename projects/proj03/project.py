# project.py


import pandas as pd
import numpy as np
from pathlib import Path
import re
import requests
import time


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def get_book(url):
    response = requests.get(url)
    time.sleep(0.5)
    text = response.text
    start = text.find(re.search(r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK (.*?) \*\*\*", text).group(0)) + len(re.search(r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK (.*?) \*\*\*", text).group(0))
    stop = text.find(re.search(r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK (.*?) \*\*\*", text).group(0), start)
    stripped = text[start:stop]
    stripped = stripped.replace("\r\n", "\n")
    return stripped


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def tokenize(book_string):
    ...


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------

class UniformLM(object):

    def __init__(self, tokens):
            self.mdl = self.train(tokens)

    def train(self, tokens):
        self.dct = {}
        total = 0
        for token in tokens:
            if token not in self.dct.keys():
                self.dct.update({token: 1})
                total += 1
        for key in self.dct:
            current_val = self.dct.get(key)
            current_val /= total
            self.dct.update({key: current_val})
        return pd.Series(self.dct)
    
    def probability(self, words):
        probs = []
        for word in words:
            if word not in self.mdl:
                return 0.0
            probs.append(self.mdl[word])
        return np.prod(probs)
    
    def sample(self, M):
        words = np.random.choice(self.mdl.index, M, p=self.mdl.values)
        return " ".join(words)


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


class UnigramLM(object):

    def __init__(self, tokens):

            self.mdl = self.train(tokens)

    def train(self, tokens):
        self.dct = {}
        total = 0
        for token in tokens:
            if token in self.dct.keys():
                current_val = self.dct.get(token)
                self.dct.update({token: current_val + 1})
                total += 1
            else:
                self.dct.update({token: 1})
                total += 1
        for key in self.dct:
            current_val = self.dct.get(key)
            current_val /= total
            self.dct.update({key: current_val})
        return pd.Series(self.dct)
    
    def probability(self, words):
        probs = []
        for word in words:
            if word not in self.mdl:
                return 0.0
            probs.append(self.mdl[word])
        return np.prod(probs)
    
    def sample(self, M):
        words = np.random.choice(self.mdl.index, M, p=self.mdl.values)
        return " ".join(words)


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


class NGramLM(object):
    
    def __init__(self, N, tokens):
        # You don't need to edit the constructor,
        # but you should understand how it works!
        
        self.N = N

        ngrams = self.create_ngrams(tokens)

        self.ngrams = ngrams
        self.mdl = self.train(ngrams)

        if N < 2:
            raise Exception('N must be greater than 1')
        elif N == 2:
            self.prev_mdl = UnigramLM(tokens)
        else:
            self.prev_mdl = NGramLM(N-1, tokens)

    def create_ngrams(self, tokens):
        start_point = 0
        end_point = self.N
        ngrams = []
        while end_point <= len(tokens):
            ngrams.append(tuple(tokens[start_point:end_point]))
            start_point += 1
            end_point += 1
        return ngrams
        
    def train(self, ngrams):
        ...
    
    def probability(self, words):
        ...
    

    def sample(self, M):
        ...
