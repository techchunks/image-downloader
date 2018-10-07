import os
import shutil
import unittest
from unittest import mock
from download import download, InvalidURLException, InvalidFileTypeException, DuplicateException


class MyTestCase(unittest.TestCase):
    def _mock_urlopen(self, mock_urlopen, read_value=b'somedata', headers={'Content-Type': 'image/jpeg'}):
        m = mock.MagicMock()
        m.read.return_value = read_value
        m.headers = headers

        m.__enter__.return_value = m
        mock_urlopen.return_value = m

    def setUp(self):
        self.test_image_dir = './test_images/'
        shutil.rmtree(self.test_image_dir, ignore_errors=True)
        os.makedirs(self.test_image_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_image_dir, ignore_errors=True)

    @unittest.mock.patch('download.urlopen')
    def test_successful_download(self, mock_urlopen):
        self._mock_urlopen(mock_urlopen)
        url = 'https://somevalidurl.com/image.jpg'
        download(url, download_dir=self.test_image_dir)

    @unittest.mock.patch('download.urlopen')
    def test_duplicate_download(self, mock_urlopen):
        self._mock_urlopen(mock_urlopen)
        url = 'https://somevalidurl.com/image.jpg'
        download(url, download_dir=self.test_image_dir)

        self._mock_urlopen(mock_urlopen)
        url = 'https://somevalidurl.com/image.jpg'
        self.assertRaises(DuplicateException, download, url, download_dir=self.test_image_dir)

    @unittest.mock.patch('download.urlopen')
    def test_invalid_content_type(self, mock_urlopen):
        self._mock_urlopen(mock_urlopen, headers={'Content-Type': 'video/mpg'})
        url = 'https://somevalidurl.com/video.mpg'

        self.assertRaises(InvalidFileTypeException, download, url, download_dir=self.test_image_dir)

    def test_invalid_url(self):
        url = '//someinvalidurl.orgg/aksdjaklsda'
        self.assertRaises(InvalidURLException, download, url, download_dir=self.test_image_dir)


if __name__ == "__main__":
    unittest.main()
