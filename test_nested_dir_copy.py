'''
If file in dir is corrupt does that make it a corrupt directory?
if file in src if corrupt, should we raise an exception?
'''

import pytest
import os
import datetime
import inspect
from compare_directory import are_dir_trees_equal, write_results
from result_wrapper import TestResult
import log_wrapper as nl

logger = nl.setup_logger('first_logger', 'nested_dir_copy.log')


@pytest.fixture(scope="module")
def get_directories_windows():
    src_dir = r'c:\Python_Practice'
    dst_dir = r'c:\Python_Practice2'

    yield src_dir, dst_dir

@pytest.fixture(scope="module")
def get_directories_unix():
    src_dir = r'/home/user'
    dst_dir = r'/home/user'

    yield src_dir, dst_dir


def test_windows_recursive_cp(get_directories_windows):
    """

    :param get_directories_windows:
    :return:
    """

    result = TestResult(inspect.stack()[0][3], datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

    if not os.path.exists(get_directories_windows[1]):
        result.result_status = "Parent Directory is missing."

    else:
        result.result_status = are_dir_trees_equal(get_directories_windows[0], get_directories_windows[1], result.result_timestamp)

    result.write_results(f'test_results.json')

    assert result.result_status
