import unittest
from utils.url_utils import check_url_invalidity
# module for importing params functionality
from nose2.tools import params


class UrlUtilsTest(unittest.TestCase):

    @params("", "aaaa")
    def test_empty_url(self, given):
        # Given
        expected_title = 'Invalid link'
        expected_msg = 'Cannot continue with too short link.\nPlease, check, if it was copied in full.'

        # When
        result_title, result_msg = check_url_invalidity(given)

        # Then
        assert expected_title == result_title
        assert expected_msg == result_msg

    def test_proper_url(self):
        # Given
        given = 'https://www.youtube.com/watch?v=WXWtXZl9Pa0'
        expected_title = None
        expected_msg = None

        # When
        result_title, result_msg = check_url_invalidity(given)

        # Then
        assert expected_title == result_title
        assert expected_msg == result_msg

