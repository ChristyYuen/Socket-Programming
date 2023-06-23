import unittest
import subprocess
import argparse
import os
import filecmp
import sys
from pathlib import Path

def do_get_stderr(url):
        cmd = subprocess.Popen(['python3', studentPath, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = cmd.communicate()
        returncode = cmd.wait()
        if (returncode != 0):
            print(str(studentPath) + ' exited with status code ' + str(returncode) + ':\n' + str(stderr.decode('UTF-8')))
            raise RuntimeError(str(studentPath) + ' crashed during the test for ' + str(url))
        return stderr.decode('UTF-8').rstrip()

def do_compare_url(url): 
    # response = requests.get(url, allow_redirects=False)
    with open('curl_output.html', 'wb') as fd:
        curl = subprocess.Popen(['curl', '-o', 'curl_output.html', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        curl.wait()

        try:
            cmd = subprocess.Popen(['python3', studentPath, url], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            stdout, stderr = cmd.communicate()
            returncode = cmd.wait()
            if (returncode != 0):
                print(str(studentPath) +  ' exited with status code ' + str(returncode) + ':\n' + str(stderr.decode('UTF-8')))
                raise RuntimeError(str(studentPath) + ' crashed during the test for ' + str(url))
            else:
                assert Path('HTTPoutput.html').is_file(), 'No HTTPoutput.html file in ' + os.path.dirname(os.path.realpath(__file__)) + ' found after running: python3 ' + studentPath + ' ' + url

            filesAreSame = filecmp.cmp('curl_output.html', 'HTTPoutput.html')

        finally:
            if Path('HTTPoutput.html').is_file():
                os.remove('HTTPoutput.html')
    
    os.remove('curl_output.html')
    return filesAreSame

class Test200(unittest.TestCase):

    urls = ['http://www.example.com/', 'http://www.example.com/index.html', 'http://www.example.com:80/index.html', 'http://neverssl.com/', 'http://pudim.com.br/']

    def test_downloaded_object(self):
        for url in self.urls:
            with self.subTest(url=url):
                self.assertEqual(do_compare_url(url), True)

class Test301(unittest.TestCase):
    
    urls = ['http://www.ucla.edu', 'http://www.cnn.com']
    
    def test_downloaded_object(self):
        for url in self.urls:
            with self.subTest(url=url):
                self.assertEqual(do_compare_url(url), True)


class Test404(unittest.TestCase):
    def test_bad_url(self):
        self.assertEqual(do_compare_url('http://www.example.com/somerandomarticle.html'), True)

class TestConnectionReset(unittest.TestCase):
    def test_connection_reset(self):
        self.assertEqual(do_get_stderr('http://www.google.com:443'), 'curl: Connection reset by peer')

class TestChunkedEncoding(unittest.TestCase):
    def test_https(self):
        self.assertEqual(do_get_stderr('http://www.google.com/index.html'), 'curl: Chunked transfer encoding not supported')

class TestHTTPS(unittest.TestCase):
    def test_chunked_encoding(self):
        self.assertEqual(do_get_stderr('https://datatracker.ietf.org/doc/html/rfc2616'), 'curl: HTTPS not supported')

class TestBadHostResolution(unittest.TestCase):
    def test_bad_host(self):
        self.assertEqual(do_get_stderr('http://www.dylancirimellilow.com/'), 'curl: Could not resolve host')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path to program to test')
    parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose output')
    args  = parser.parse_args()

    global studentPath 
    studentPath = args.path
    assert Path(studentPath).is_file() and studentPath.endswith('.py'), "Provided path does not point to a valid python file" 

    global level 
    level = 1
    if args.verbose:
        level = 2

    unittest.main(argv=sys.argv[:1], verbosity=level)
    