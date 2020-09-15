"""
This module contains a wrapper for test results.
"""

import json


class TestResult(object):

    def __init__(self, test_name, result_timestamp):

        self.test_name = test_name
        self.result_timestamp = result_timestamp
        self.result_status = None

    def write_results(self, file_name):
        """

        :param file_name:
        :return:
        """
        with open(file_name, 'a') as fp:
            json.dump(self.__dict__, fp, indent=4)
