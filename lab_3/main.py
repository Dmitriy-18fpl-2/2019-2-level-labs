"""
Labour work #3
Building an own N-gram mode
"""

from math import log

REFERENCE_TEXT = ''
if __name__ == '__main__':
    with open('not_so_big_reference_text.txt', 'r') as f:
        REFERENCE_TEXT = f.read()


class WordStorage:
    def __init__(self):
        self.storage = {}

    def put(self, word: str) -> int:
        if word not in self.storage and isinstance(word, str):
            word_id = len(list(self.storage.keys())) + 1
            self.storage[word] = word_id
            return word_id
        else:
            print("ERROR")

    def get_id_of(self, word: str) -> int:
        if word in self.storage and isinstance(word, str):
            return self.storage[word]
        else:
            return -1

    def get_original_by(self, id: int) -> str:
        word_id = id
        list_of_keys = list(self.storage.keys())
        list_of_values = list(self.storage.values())
        if word_id in list_of_values and isinstance(word_id, int):
            return list_of_keys[list_of_values.index(word_id)]
        else:
            return "UNK"

    def from_corpus(self, corpus: tuple):
        id_counter = 1
        if isinstance(corpus, tuple) and corpus != () and isinstance(corpus[0], list):
            for line in range(len(corpus)):
                for word in range(len(corpus[line])):
                    if corpus[line][word] not in self.storage:
                        self.storage[corpus[line][word]] = id_counter
                        id_counter += 1
                    else:
                        continue
        elif isinstance(corpus, tuple) and corpus != ():
            for word in range(len(corpus)):
                if corpus[word] not in self.storage:
                    self.storage[corpus[word]] = id_counter
                    id_counter += 1
                else:
                    continue
        else:
            return False


class NGramTrie:
    def __init__(self, n):
        if n > 1:
            self.size = n
        else:
            print("ERROR, this is pointless")
        self.gram_frequencies = {}
        self.gram_log_probabilities = {}

    def fill_from_sentence(self, sentence: tuple) -> str:
        if isinstance(sentence, tuple) and sentence != ():
            if len(sentence) <= self.size:
                last_word = sentence[len(sentence) - 1]
                sentence = list(sentence)
                for i in range(self.size - len(sentence)):
                    sentence.insert(len(sentence), last_word)
                sentence = tuple(sentence)
                if sentence not in self.gram_frequencies:
                    self.gram_frequencies[sentence] = 1
                else:
                    self.gram_frequencies[sentence] += 1
            else:
                for gram_index in range(len(sentence) - (self.size - 1)):
                    gram = tuple([sentence[gram_index + i] for i in range(self.size)])
                    if gram not in self.gram_frequencies:
                        self.gram_frequencies[gram] = 1
                    else:
                        self.gram_frequencies[gram] += 1
            return "OK"
        else:
            return "ERROR"

    def calculate_log_probabilities(self):
        if self.gram_frequencies != {}:
            for gram in self.gram_frequencies:
                overall_freq = 0
                for key_gram in list(self.gram_frequencies.keys()):
                    if gram[:self.size - 1] == key_gram[:self.size - 1]:
                        overall_freq += self.gram_frequencies[key_gram]
                self.gram_log_probabilities[gram] = log(self.gram_frequencies[gram] / (overall_freq))
        else:
            return False

    def predict_next_sentence(self, prefix: tuple) -> list:
        if isinstance(prefix, tuple) and len(prefix) == self.size - 1:
            predicted_sentence = list(prefix)
            support_number = 0
            while True:
                prefix = tuple(predicted_sentence[support_number:len(predicted_sentence)])
                next_word_prob = 0
                next_word = "safety"
                for key_log_prob in list(self.gram_log_probabilities.keys()):
                    if prefix == key_log_prob[:self.size - 1] and next_word_prob == 0:
                        next_word = key_log_prob[len(key_log_prob) - 1]
                        next_word_prob = self.gram_log_probabilities[key_log_prob]
                        continue
                    elif prefix == key_log_prob[:self.size - 1]:
                        if next_word_prob < self.gram_log_probabilities[key_log_prob]:
                            next_word = key_log_prob[len(key_log_prob) - 1]
                            next_word_prob = self.gram_log_probabilities[key_log_prob]
                        else:
                            continue
                    else:
                        continue
                if next_word == "safety" or next_word == predicted_sentence[len(predicted_sentence) - 1]:
                    return predicted_sentence
                else:
                    predicted_sentence.insert(len(predicted_sentence), next_word)
                support_number += 1
        else:
            predicted_sentence = []
            return predicted_sentence


def encode(storage_instance, corpus) -> list:
    encoded_corpus = []
    for line_index in range(len(corpus)):
        encoded_line = []
        for index, word in enumerate(corpus[line_index]):
            encoded_line.insert(index, storage_instance.get_id_of(word))
        encoded_corpus.insert(line_index, encoded_line)
    return encoded_corpus


def split_by_sentence(text: str) -> list:
    test_objects = "qwertyuioplkjhgfdsazxcvbnm. "
    signs = "!?"
    text_clean = ""
    if isinstance(text, str) and text != '' and "." in text:
        text_low = text.lower()
        for i in range(len(text_low)):
            if text_low[i] in test_objects:
                text_clean += text_low[i]
            if text_low[i] in signs:
                text_clean += "."
            else:
                continue
        corpus = text_clean.split(".")
        if corpus[len(corpus) - 1] == '':
            corpus.pop()
        for i in range(len(corpus)):
            corpus[i] = corpus[i].split()
            corpus[i].insert(len(corpus[i]), "</s>")
            corpus[i].insert(0, "<s>")
        return corpus
    else:
        print('ERROR')
        return []


def all_in_one(text, n, prefix):
    test_storage = WordStorage()
    sample = tuple(split_by_sentence(text))
    test_storage.from_corpus(sample)
    encoded_corp = encode(test_storage, sample)
    sample_gram = NGramTrie(n)
    for sentence in encoded_corp:
        sample_gram.fill_from_sentence(tuple(sentence))
    sample_gram.calculate_log_probabilities()
    prefix_list = []
    for word in prefix:
        prefix_list.insert(len(prefix_list), test_storage.get_id_of(word))
    prefix = tuple(prefix_list)
    return sample_gram.predict_next_sentence(prefix)

