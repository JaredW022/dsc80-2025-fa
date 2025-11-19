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
    book_string = book_string.replace("\r\n", "\n")
    paragraphs = re.split(r'\n{2,}', book_string.strip())
    tokens = []
    for paragraph in paragraphs:
        tokens.append('\x02')
        tokens.extend(re.findall(r'\w+|[^\w\s_]', paragraph))
        tokens.append('\x03')
    return tokens


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
        og_ngrams = self.create_ngrams(ngrams)
        nm1gram = []
        for tup in og_ngrams:
            nm1gram.append(tup[:-1])

        cond_total = {}
        for og_ngram in og_ngrams:
            if og_ngram in cond_total.keys():
                current_val = cond_total.get(og_ngram)
                cond_total.update({og_ngram: current_val + 1})
            else:
                cond_total.update({og_ngram: 1})

        cond_total2 = {}
        for ngram in nm1gram:
            if ngram in cond_total2.keys():
                current_val = cond_total2.get(ngram)
                cond_total2.update({ngram: current_val + 1})
            else:
                cond_total2.update({ngram: 1})

        df = pd.DataFrame()
        df["ngram"] = og_ngrams
        df["n1gram"] = nm1gram

        probabilites = []
        for i in range(len(df["n1gram"])):
            probabilites.append(cond_total.get(df["ngram"][i]) / cond_total2.get(df["n1gram"][i]))

        df["prob"] = probabilites

        return df
    
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
        nm1gram = []
        for tup in ngrams:
            nm1gram.append(tup[:-1])

        cond_total = {}
        for og_ngram in ngrams:
            if og_ngram in cond_total.keys():
                current_val = cond_total.get(og_ngram)
                cond_total.update({og_ngram: current_val + 1})
            else:
                cond_total.update({og_ngram: 1})

        cond_total2 = {}
        for ngram in nm1gram:
            if ngram in cond_total2.keys():
                current_val = cond_total2.get(ngram)
                cond_total2.update({ngram: current_val + 1})
            else:
                cond_total2.update({ngram: 1})

        df = pd.DataFrame()
        df["ngram"] = ngrams
        df["n1gram"] = nm1gram

        probabilites = []
        for i in range(len(df["n1gram"])):
            probabilites.append(cond_total.get(df["ngram"][i]) / cond_total2.get(df["n1gram"][i]))

        df["prob"] = probabilites

        return df.drop_duplicates().reset_index(drop=True)

    def probability(self, words):
        current_model = self
        prob = 1.0
        if 1 < current_model.N:
            current_model = current_model.prev_mdl
            prob *= current_model.probability(words[:self.N - 1])
        indexed = self.mdl.set_index("ngram")
        for i in range(len(words) - self.N + 1):
            if tuple(words[i:i + self.N]) in indexed.index:
                prob *= indexed.loc[[tuple(words[i:i + self.N])], "prob"].iloc[0]
            else:
                return 0.0
        return prob
    
    def sample(self, M):
        words = ["\x02"]
        while len(words) < M + 1:
            if len(words) == M:
                words.append("\x03")
                break
            if len(words) < self.N:
                current_mdl = self
                while hasattr(current_mdl, "prev_mdl") and current_mdl.N - 1 > len(words):
                    current_mdl = current_mdl.prev_mdl
                temp_mdl = current_mdl.mdl[current_mdl.mdl["ngram"].apply(lambda x: x[:-1]) == tuple(words[-(current_mdl.N - 1):])]
                if temp_mdl.empty:
                    words.append("\x03")
                else:
                    words.append(np.random.choice(list(temp_mdl["ngram"].apply(lambda x: x[-1])), p=list(temp_mdl["prob"])))
            else: 
                temp_mdl = self.mdl[self.mdl["ngram"].apply(lambda x: x[:-1]) == tuple(words[-(self.N - 1):])]
                if temp_mdl.empty:
                    words.append("\x03")
                else:
                    words.append(np.random.choice(list(temp_mdl["ngram"].apply(lambda x: x[-1])), p=list(temp_mdl["prob"])))
        return " ".join(words)