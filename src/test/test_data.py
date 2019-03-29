import pytest
import builtins

from io import StringIO

from src.data import FancyDictionary

INPUT_DATA = ['word1', 'word2', 'word3', '1wrdo']
EXPECTED_DATA = {'1dorw': ['word1', '1wrdo'], '2dorw': ['word2'], '3dorw': ['word3']}


@pytest.fixture
def mock_open(monkeypatch):
    test_txt = StringIO("\n".join(INPUT_DATA))
    m = lambda path, mode: test_txt
    monkeypatch.setattr(builtins, 'open', m)


class MockLogging:
    info_msgs = list()
    debug_msgs = list()

    def info(self, *args):
        self.info_msgs += [eval(str(args))]

    def debug(self, *args):
        self.debug_msgs += [eval(str(args))]


def test__sort_word():
    assert FancyDictionary._sort_word(word='dcba') == 'abcd'


def test__load_data_file(mock_open):
    lgr = MockLogging()
    fd = FancyDictionary(path='test_path', logger=lgr)
    test_len = len(INPUT_DATA)
    assert fd.total_words == test_len
    assert fd._data == EXPECTED_DATA
    assert 'DB loaded successfully' in str(lgr.info_msgs)
    debug_string_expected = 'Words count = {}, DB Keys = {}, DB Values = {}'.format(test_len, test_len - 1, test_len)
    assert debug_string_expected in str(lgr.debug_msgs)


@pytest.mark.asyncio
async def test_check_exists(mock_open):
    lgr = MockLogging()
    fd = FancyDictionary(path='test_path', logger=lgr)
    assert await fd.check('word1') == ['1wrdo']
    assert 'word1' in fd._data['1dorw']


@pytest.mark.asyncio
async def test_check_missing(mock_open):
    lgr = MockLogging()
    fd = FancyDictionary(path='test_path', logger=lgr)
    assert await fd.check('word4') == []






