"""
Data handling for Print Similar web service
"""
import time

from collections import defaultdict


class FancyDictionary:
    def __init__(self, path, logger):
        """
        :param str path: path of source dictionary
        """
        self.logger = logger
        self._data, self.total_words = self._load_data_file(path)

    @staticmethod
    def _sort_word(word):
        """
        Used to return a sorted string based on a given word
        :param str word:
        :rtype: str
        """
        return "".join((sorted(word)))

    async def check(self, word):
        """
        Fetch a word from the DB
        :param str word:
        :rtype: list[str]
        """
        search_item = self._sort_word(word)  # Sort to get a unique representation for all permutations
        result = self._data[search_item].copy()  # Don't change the original data
        if result:
            result.remove(word)  # Remove the word that we asked about

        return result

    def _load_data_file(self, path):
        """
        Load a dictionary txt file
        :param str path: path of data source
        """
        start_time = time.time()
        data = defaultdict(list)
        total_words = 0

        with open(path, "r") as fileHandler:
            for line in fileHandler:
                total_words += 1
                word = line.strip()  # Need to stripe as each line (except last one) will contain new line character
                sorted_word = self._sort_word(word)  # get the sorted version of the word
                data[sorted_word] += [word]  # Insert the data to the DB

        end_time = time.time()

        self.logger.info("DB loaded successfully (loaded in {:.5f}s)".format(end_time - start_time))
        self.logger.debug(f"Words count = {total_words}, "
                          f"DB Keys = {len(data.keys())}, "
                          f"DB Values = {sum([len(data[x]) for x in data if isinstance(data[x], list)])}")

        return data, total_words
