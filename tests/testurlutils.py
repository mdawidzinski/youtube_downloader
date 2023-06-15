import unittest
from utils.url_utils import check_url_invalidity
# module for importing params functionality
from nose2.tools import params


class UrlUtilsTest(unittest.TestCase):

    def test_with_None_url(self):
        # Given
        given = None
        expected_title = 'Invalid link'
        expected_msg = 'Cannot continue with empty link.\nPlease, provide a valid link.'

        # When
        result_title, result_msg = check_url_invalidity(given)

        # Then
        assert expected_title == result_title
        assert expected_msg == result_msg

    @params('', 'aaaa')
    def test_empty_url(self, given):
        # Given
        expected_title = 'Invalid link'
        expected_msg = 'Cannot continue with too short link.\nPlease, check, if it was copied in full.'

        # When
        result_title, result_msg = check_url_invalidity(given)

        # Then
        assert expected_title == result_title
        assert expected_msg == result_msg

    def test_wrong_beginning(self):
        # Given
        given = 'https://www.godtube.com/watch/?v=19220JNU'
        expected_title = 'Invalid link'
        beginning = 'https://www.youtube.com/watch'
        expected_msg = f'Link must start with {beginning}.\nPlease, check, if the right link was copied.'

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

