import unittest
import requests_mock

from vvpmagics.httpsession import HttpSession


@requests_mock.Mocker()
class HttpSessionTests(unittest.TestCase):
    base_url = "http://localhost:8080/"
    path = "test"
    return_text = "Hello, world."

    def test_get_request(self, requests_mocker):
        requests_mocker.request(
            method='get', url='http://localhost:8080/{}'.format(self.path), text=self.return_text)

        result = HttpSession(self.base_url, None).get(self.path)

        assert result.status_code == 200
        assert result.text == self.return_text

    def test_get_manages_request_headers(self, requests_mocker):
        request_headers = {'testheader': 'testheadervalue'}
        session_headers = {'testsessionheader': 'testsessionheadervalue'}
        requests_mocker.request(
            method='get', url='http://localhost:8080/{}'.format(self.path),
            request_headers={**request_headers, **session_headers}, text=self.return_text)
        requests_mocker.request(
            method='get', url='http://localhost:8080/{}'.format(self.path),
            request_headers=request_headers, text=self.return_text)

        http_session_with_headers = HttpSession(self.base_url, session_headers)
        result = http_session_with_headers.get(self.path, request_headers)
        assert result.text == self.return_text

        http_session_without_headers = HttpSession(self.base_url, None)
        result = http_session_without_headers.get(self.path, request_headers)
        assert result.text == self.return_text

    def test_post_request(self, requests_mocker):
        def match_request_text(request):
            return 'test' in (request.text or '')

        requests_mocker.request(method='post', url='http://localhost:8080/{}'.format(
            self.path), additional_matcher=match_request_text, text=self.return_text)

        result = HttpSession(self.base_url, None).post(self.path, "hello world test")

        assert result.status_code == 200
        assert result.text == self.return_text


if __name__ == '__main__':
    unittest.main()
