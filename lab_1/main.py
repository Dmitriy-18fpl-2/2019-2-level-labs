"""
Labour work #1
Count frequencies dictionary by the given arbitrary text
"""


def calculate_frequences(text: str) -> dict:
    """
    Calculates number of times each word appears in the text
    """
    test_objects_1 = "qwertyuioplkjhgfdsazxcvbnm "
    test_objects_2 = "qwertyuioplkjhgfdsazxcvbnm"
    text_clean = ""
    if type(text) == str:
        text_low = text.lower()
        for i in range(len(text_low)):
            if text_low[i] == "'" and text_low[i - 1] in test_objects_2 and text_low[i + 1] in test_objects_2:
                text_clean += text_low[i]
            if text_low[i] in test_objects_1:
                text_clean += text_low[i]
            if text_low[i] == "\n":
                text_clean += " "
            else:
                continue
        list_of_words = text_clean.split()
        global frequencies
        frequencies = {}
        for i in range(len(list_of_words)):
            if list_of_words[i] not in frequencies:
                frequencies[list_of_words[i]] = 1
            else:
                frequencies[list_of_words[i]] += 1
        return (frequencies)
    else:
        frequencies = {}
        return frequencies
        print('error, text must be str')

def filter_stop_words(frequencies: dict, stop_words: tuple) -> dict:
    """
    Removes all stop words from the given frequencies dictionary
    """
    if type(stop_words) == tuple and type(frequencies) == dict:
        global frequencies_edited
        frequencies_edited = frequencies.copy()
        check_list = list(frequencies_edited.keys())
        for key in check_list:
            if type(key) != str:
                del(frequencies_edited[key])
            else:
                continue
        for i in stop_words:
            if type(i) != str:
                print('error,', i, 'is not str.')
                continue
            if i in frequencies_edited:
                del(frequencies_edited[i])
            else:
                continue
    else:
        print('error, stop_words must be tuple')
    return (frequencies_edited)


def get_top_n(frequencies: dict, top_n: int) -> tuple:
    """
    Takes first N popular words
    """
    if type(top_n) == int and top_n >= 1:
        N_words = []
        for k, v in frequencies.items():
            if len(N_words) == 0:
                N_words += [k]
            else:
                order = len(N_words)
                for index, element in enumerate(N_words):
                    if v >= frequencies[N_words[index]] or v == frequencies[N_words[index]]:
                        order -= 1
                    else:
                        continue
                N_words.insert(order, k)
                if len(N_words) >= top_n + 1:
                    del N_words[top_n]
        N_popular_words = tuple(N_words)
        return (N_popular_words)
    else:
        N_popular_words = ()
        return N_popular_words
        print('error, top_n must be int')

