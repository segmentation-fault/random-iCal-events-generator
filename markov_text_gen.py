__author__ = 'antonio franco'

'''
Copyright (C) 2019  Antonio Franco (antonio_franco@live.it)
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from copy import deepcopy
from urllib.request import urlopen
import numpy as np
import pickle
from io import BufferedReader


class MarkovTextGen(object):
    def __init__(self) -> None:
        """
        This class represents a markov chain text generator. Given a text file, it generates random sentences.
        """
        super().__init__()
        self.word_dict = {}
        self.corpus = []

    def __make_pairs__(self):
        """
        Makes pairs state -> transitions
        """
        for i in range(len(self.corpus) - 1):
            yield (self.corpus[i], self.corpus[i + 1])

    def train_by_txt(self, my_file: BufferedReader) -> None:
        """
        Given a file object, representing a txt file, it creates the markov chain
        Thanks to: https://towardsdatascience.com/simulating-text-with-markov-chains-in-python-1a27e6d13fc6
        :param my_file (file object): txt file to read
        """
        self.corpus = my_file.read().split()
        pairs = self.__make_pairs__()

        for word_1, word_2 in pairs:
            if word_1 in self.word_dict.keys():
                self.word_dict[word_1].append(word_2)
            else:
                self.word_dict[word_1] = [word_2]

    def get_rnd_text(self, n_words: int, prefix: str = "", suffix: str = ".") -> str:
        """
        Returns a random text with exactly n_words words, preceded by a prefix and a suffix
        :param n_words (int): number of words to produce
        :param prefix (str): optional prefix to append at the beginning of the string
        :param suffix (str): optional suffix to append at the end of the string
        :return: random sentence
        """
        first_word = np.random.choice(self.corpus)

        while first_word.islower():
            first_word = np.random.choice(self.corpus)

        chain = [first_word]

        for i in range(n_words):
            chain.append(np.random.choice(self.word_dict[chain[-1]]))

        sentenz = prefix + " "

        for i in range(0, len(chain)):
            sentenz += str(chain[i].decode('UTF-8')) + " "

        return sentenz + suffix

    def get_rnd_text_until(self, termin_char: str, max_words: int = 100) -> str:
        """
        Returns a random sentence until termin_char is encountered, or max_words is hit
        :param termin_char (str): character that, when encountered, causes the generation to stop
        :param max_words (int): maximum number of words before the generation stops
        :return: random sentence
        """
        first_word = np.random.choice(self.corpus)

        while first_word.islower():
            first_word = np.random.choice(self.corpus)

        chain = [first_word]

        last_word = b''
        i = 0

        while last_word.find(termin_char) < 0 and i < max_words:
            last_word = np.random.choice(self.word_dict[chain[-1]])
            chain.append(last_word)
            i = i + 1

        sentenz = " "

        for i in range(0, len(chain)):
            sentenz += str(chain[i].decode('UTF-8')) + " "

        return sentenz

    def load_dictionary(self, pickle_file: str) -> None:
        """
        Loads the markov chain stored in the pickle file with path pickle_file
        :param pickle_file (str): path of the pickle file
        """
        pickle_in = open(pickle_file, "rb")
        my_dict = pickle.load(pickle_in)
        self.corpus = deepcopy(my_dict["corpus"])
        self.word_dict = deepcopy(my_dict["word_dict"])

    def save_dictionary(self, pickle_file: str) -> None:
        """
        Saves the markov chain the pickle file with path pickle_file
        :param pickle_file (str): path of the pickle file
        """
        pickle_out = open(pickle_file, "wb")
        my_dict = {"corpus": self.corpus, "word_dict": self.word_dict}
        pickle.dump(my_dict, pickle_out)
        pickle_out.close()


if __name__ == "__main__":
    # Creates the Markov chain using a book from project Gutenberg, then saves the markov chain as a pickle file
    train_uri = "https://www.gutenberg.org/files/388/388-0.txt"
    f = urlopen(train_uri)

    M = MarkovTextGen()
    M.train_by_txt(f)

    f.close()

    M.save_dictionary("Churchill.pickle")
