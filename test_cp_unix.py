'''
If file in dir is corrupt does that make it a corrupt directory?
if file in src if corrupt, should we raise an exception?
'''

import pytest
import os
import datetime
from compare_directory import are_dir_trees_equal, write_results
import log_wrapper as nl

logger = nl.setup_logger('first_logger', 'first_logfile.log')


@pytest.fixture(scope="module")
def get_directories_windows():
    src_dir = r'c:\Python_Practice'
    dst_dir = r'c:\Python_Practice2'

    yield src_dir, dst_dir

def test_unix_recursive_cp(get_directories_windows):
    """

    :param get_directories_windows:
    :return:
    """
    result = dict()
    result["test_datetime"] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    result["test_name"] = "test_unix_recursive_cp"

    if not os.path.exists(get_directories_windows[1]):
        result["test_result"] = "Parent Directory is missing."
        result["PASS"] = False

    else:
        result["PASS"] = are_dir_trees_equal(get_directories_windows[0], get_directories_windows[1], result["test_datetime"])

    write_results(result, f'test_results.json')

    assert result["PASS"]
