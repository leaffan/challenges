from data import DICTIONARY, LETTER_SCORES
from operator import itemgetter
from concurrent.futures import ThreadPoolExecutor, as_completed


def load_words():
    """
    Loads dictionary into a list and returns list.
    """
    with open(DICTIONARY) as file:
        return [l.strip() for l in file.readlines()]


def calc_word_value(word, return_word=False):
    """
    Calculates the value of the word entered into function using imported
    constant mapping LETTER_SCORES. Optionally returns the word itself, too.
    """
    word_value = sum([LETTER_SCORES[
        letter.upper()] for letter in word if letter.upper() in LETTER_SCORES])

    if not return_word:
        return word_value
    else:
        return word, word_value


def max_word_value(words=None, threaded=True):
    """
    Calculates the word with the maximum value, can receive a list
    of words as arg, if none provided uses default DICTIONARY. Optionally
    processes words sequentially, too.
    """
    if words is None:
        words = load_words()

    # calculating words simultaneously by default
    if threaded:
        word_values = list()
        with ThreadPoolExecutor(max_workers=4) as threads:
            future_tasks = {
                threads.submit(
                    calc_word_value, word, True): word for word in words}
            for future in as_completed(future_tasks):
                try:
                    word_values.append(future.result())
                except Exception as e:
                    print
                    print("Conccurrent task generated an exception: %s" % e)

        return sorted(word_values, key=itemgetter(1), reverse=True).pop(0)[0]
    # otherwise calculating words sequentially
    else:
        for word in words:
            values = [calc_word_value(word) for word in words]
        return words[values.index(max(values))]


if __name__ == "__main__":
    print(max_word_value(('bob', 'julian', 'pybites', 'quit', 'barbeque')))
