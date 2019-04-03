import pytest
import jsonutil as util

try:
    import ujson as json # Speedup if present; no big deal if not
except ImportError:
    import json

@pytest.fixture
def config():
    print('get_config')
    with open('./jsonutil_test.json', 'r') as json_file:
        json_content = json_file.read()
        json_content = util.remove_comments(json_content)
        json_content = util.remove_trailing_commas(json_content)
    yield (json.loads(json_content))

def test_json_parse(config):
    print("test_answer")
    assert config['type'] == 'sftp'
    assert type(config['ignore_regexes']) == list
