"""SpamSieve: a Naive Bayes mail filter shared by train.py and app.py.

Each distinct word in a message counts once (binarized multinomial Naive Bayes),
so repeating a word does nothing. Words the model never saw are ignored.
"""
import math
import re

WORD = re.compile(r"[a-z]+")


def tokens(text):
    return set(WORD.findall(text.lower()))


def train(spam_docs, ham_docs, alpha=1.0):
    spam_counts, ham_counts = {}, {}
    for docs, counts in ((spam_docs, spam_counts), (ham_docs, ham_counts)):
        for doc in docs:
            for w in tokens(doc):
                counts[w] = counts.get(w, 0) + 1
    vocab = sorted(set(spam_counts) | set(ham_counts))
    spam_total = sum(spam_counts.values()) + alpha * len(vocab)
    ham_total = sum(ham_counts.values()) + alpha * len(vocab)
    weights = {
        w: round(math.log((spam_counts.get(w, 0) + alpha) / spam_total)
                 - math.log((ham_counts.get(w, 0) + alpha) / ham_total), 4)
        for w in vocab
    }
    prior = round(math.log(len(spam_docs) / len(ham_docs)), 4)
    return {"prior": prior, "weights": weights}


def score(model, text):
    """Return (spam probability, [(word, weight)] sorted by weight)."""
    parts = sorted(((w, model["weights"][w]) for w in tokens(text) if w in model["weights"]),
                   key=lambda p: -p[1])
    logit = model["prior"] + sum(wt for _, wt in parts)
    prob = 1 / (1 + math.exp(-max(min(logit, 50), -50)))
    return prob, parts
