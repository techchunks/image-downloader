import os
import sys
import mimetypes
import hashlib
from urllib.request import urlopen
from urllib.parse import urlparse


class InvalidURLException(Exception):
    pass


class InvalidFileTypeException(Exception):
    pass


class DuplicateException(Exception):
    pass


def clean_url(url):
    result = urlparse(url)
    if all([result.scheme, result.netloc, result.path]):
        return result.geturl().rsplit('?', 1)[0]
    raise InvalidURLException('Invalid URL %s', url)


def download(url, download_dir='./images'):
    """ This function will download the image and store in given directory.
    Image hash is calculated and used as filename in order to avoid duplicates, this does
    help improving time complexity but space complexity. To improve time complexity one can
    make filename from hash of url (In this case I wasn't sure if that will effect desired results).
    """
    # validate URL
    url = clean_url(url)
    with urlopen(url) as response:
        file_content_type = response.headers['Content-Type']
        file_data = response.read()

        # Do not continue saving file if not a valid image
        if not file_content_type.startswith('image/'):
            raise InvalidFileTypeException('Not a valid image "%s"', url)

        extension = mimetypes.guess_extension(file_content_type)

        # create filehash to prevent duplicates
        img_hash = hashlib.md5(file_data).hexdigest()

        filename = img_hash + extension

        file_path = os.path.join(download_dir, filename)

        if os.path.isfile(file_path):
            raise DuplicateException('File "%s (%s)" already exist!' % (file_path, url))

        with open(file_path, 'wb') as f:
            f.write(file_data)

        return file_path


def main(argv):
    try:
        file_path = argv[0]
    except IndexError:
        raise Exception('Please provide file path!')

    with open(file_path, 'r+') as f:
        exceptions = 0
        duplicates = 0

        for count, url in enumerate(f):
            try:
                download(url)
            except (InvalidFileTypeException, InvalidURLException):
                exceptions += 1
            except DuplicateException:
                duplicates += 1

    print('URLs Processed: %s', count + 1)
    print('New images:     %s', count + 1 - duplicates - exceptions)
    if exceptions:
        print('Exceptions:     %s', exceptions)
    if duplicates:
        print('Duplicates:     %s', duplicates)


if __name__ == "__main__":
    main(sys.argv[1:])
