import math


REFERENCE_TEXTS = []


def clean_tokenize_corpus(texts: list) -> list:
    test_objects = "qwertyuioplkjhgfdsazxcvbnm "
    corpus = []
    if isinstance(texts, list) and texts != []:
        for text in texts:
            if isinstance(text, str) and text != []:
                text_clean = ''
                text_low = text.lower()
                if '<br />' in text_low:
                    text_low = text_low.replace('<br />', ' ')
                for index in range(len(text_low)):
                    if text_low[index] in test_objects:
                        text_clean += text_low[index]
                    else:
                        continue
                t = text_clean.split()
                corpus += [t]
            else:
                continue
        return corpus
    else:
        print('ERROR')
        return []


class TfIdfCalculator:
    def __init__(self, corpus):
        self.corpus = corpus
        self.tf_values = []
        self.idf_values = {}
        self.tf_idf_values = []
        self.file_names = []

    def calculate_tf(self):
        if isinstance(self.corpus, list) and self.corpus != []:
            iteration = 0
            for text in self.corpus:
                if isinstance(text, list) and text != []:
                    self.tf_values += [{}]
                    all_words = 0
                    for word in text:
                        if isinstance(word, str):
                            all_words += 1
                else:
                    continue
                for word in text:
                    if isinstance(word, str) and word not in self.tf_values[iteration]:
                        self.tf_values[iteration][word] = text.count(word) / all_words
                    else:
                        continue
                iteration += 1

    def calculate_idf(self):
        if isinstance(self.corpus, list):
            non_texts = 0
            for text in self.corpus:
                if isinstance(text, list):
                    continue
                else:
                    non_texts += 1
            all_texts = len(self.corpus) - non_texts
            list_of_words = self.__unique_words_extracter__()
            for word in list_of_words:
                word_appearance = 0
                for text in self.corpus:
                    if isinstance(text, list) and text != []:
                        if word in text:
                            word_appearance += 1
                        else:
                            continue
                self.idf_values[word] = math.log(all_texts / word_appearance)

    def __unique_words_extracter__(self):
        list_of_unique_words = []
        for text in self.corpus:
            if isinstance(text, list) and text != []:
                for word in text:
                    if isinstance(word, str) and word not in list_of_unique_words:
                        list_of_unique_words += [word]
                    else:
                        continue
        return list_of_unique_words

    def calculate(self):
        if isinstance(self.tf_values, list) and isinstance(self.idf_values, dict) and self.idf_values != {} and self.tf_values !=[]:
            for tf_dict_index in range(len(self.tf_values)):
                self.tf_idf_values += [{}]
                for word in list(self.tf_values[tf_dict_index].keys()):
                    if word not in self.tf_idf_values[tf_dict_index]:
                        self.tf_idf_values[tf_dict_index][word] = self.tf_values[tf_dict_index][word] * self.idf_values[word]
                    else:
                        continue

    def report_on(self, word, document_index):
        if isinstance(self.tf_idf_values, list) and document_index <= len(self.tf_idf_values) and self.tf_idf_values != [] and word not in self.tf_idf_values:
            word_values = sorted(self.tf_idf_values[document_index].items(), key=lambda item: (-item[1], item[0]))
            value_position = 0
            top_dict = {}
            for index, pare in enumerate(word_values):
                if index + 1 == len(word_values):
                    top_dict[pare[0]] = value_position
                    continue
                if word in self.corpus[document_index] and pare[1] == word_values[index + 1][1]:
                    top_dict[pare[0]] = value_position
                    continue
                elif pare[1] != word_values[index + 1][1]:
                    top_dict[pare[0]] = value_position
                    value_position += 1
            report = (self.tf_idf_values[document_index][word], top_dict[word])
            return report
        else:
            return ()

    def cosine_distance(self, index_text_1, index_text_2):
        if index_text_1 <= len(self.tf_idf_values) and index_text_2 <= len(self.tf_idf_values):
            vector_words = self.__unique_words_extracter__()
            vectors = []
            for index, text in enumerate(self.corpus):
                if index == index_text_1 or index_text_2:
                    vector = []
                    for word in vector_words:
                        if word in text:
                            vector += [self.tf_idf_values[index][word]]
                        else:
                            vector += [0]
                    print(vector)
                    vectors += [vector]
            a_b_sum = math.fsum(vectors[0][i] * vectors[1][i] for i in range(len(vector(0))))
            a_b_cube_sum = (math.sqrt(math.fsum(i*i for i in vectors[0])) * (math.sqrt(math.fsum(i*i for i in vectors[1]))))
            cos_dist = a_b_sum / a_b_cube_sum
            return cos_dist
        else:
            return 1000

    def save_to_csv(self):
        with open('report.csv', 'w') as f:
            tf_headline = ['TF(' + i + ')' for i in self.file_names]
            tf_idf_headline = ['TF-IDF(' + i + ')' for i in self.file_names]
            top = ['Слово'] + tf_headline + ['IDF'] + tf_idf_headline
            f.write(';'.join(top) + '\n')
            list_of_words = self.__unique_words_extracter__()
            for word in list_of_words:
                f.write(word + ';')
                for index in range(len(self.tf_values)):
                    if word in self.tf_values[index]:
                        f.write(str(self.tf_values[index][word]) + ';')
                    else:
                        f.write(str(0) + ';')
                f.write(str(self.idf_values[word]) + ';')
                for index in range(len(self.tf_idf_values)):
                    if word in self.tf_idf_values[index] and index == len(self.tf_idf_values) - 1:
                        f.write(str(self.tf_idf_values[index][word]) + '\n')
                    elif word not in self.tf_idf_values[index] and index == len(self.tf_idf_values) - 1:
                        f.write(str(0) + '\n')
                    elif word in self.tf_idf_values[index]:
                        f.write(str(self.tf_idf_values[index][word]) + ';')
                    else:
                        f.write(str(0) + ';')


if __name__ == '__main__':
    texts = ['5_7.txt', '15_2.txt', '10547_3.txt', '12230_7.txt']
    for text in texts:
        with open(text, 'r') as f:
            REFERENCE_TEXTS.append(f.read())
    # scenario to check your work
    test_texts = clean_tokenize_corpus(REFERENCE_TEXTS)
    tf_idf = TfIdfCalculator(test_texts)
    tf_idf.calculate_tf()
    tf_idf.calculate_idf()
    tf_idf.calculate()
    print(tf_idf.report_on('good', 0))
    print(tf_idf.report_on('and', 1))
