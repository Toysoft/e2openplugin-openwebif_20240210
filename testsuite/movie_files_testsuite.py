#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import copy
import unittest

import requests

#: movie folder
MOVIE_FOLDER = '/media/hdd/movie'

#: the main .ts file
MAIN_TS_FILE = u"{dir}/20170830 1650 - TNT Serie HD (S) - Animal Kingdom - S\u00fcndenbock.ts".format(
    dir=MOVIE_FOLDER)

EXPECTED_FILES = [
    u"{dir}/20170830 1650 - TNT Serie HD (S) - Animal Kingdom - S\u00fcndenbock.eit".format(
        dir=MOVIE_FOLDER),
    MAIN_TS_FILE,
    u"{dir}/20170830 1650 - TNT Serie HD (S) - Animal Kingdom - S\u00fcndenbock.ts.ap".format(
        dir=MOVIE_FOLDER),
    u"{dir}/20170830 1650 - TNT Serie HD (S) - Animal Kingdom - S\u00fcndenbock.ts.cuts".format(
        dir=MOVIE_FOLDER),
    u"{dir}/20170830 1650 - TNT Serie HD (S) - Animal Kingdom - S\u00fcndenbock.ts.meta".format(
        dir=MOVIE_FOLDER),
]

ENV_VAR = "ENIGMA2_HTTP_API_HOST"

ENV_VAL_FALLBACK = "127.0.0.1"

EXPECTED_MOVIE_ITEM = {
    u'filename_stripped': u'20170830 1650 - TNT Serie HD (S) - Animal Kingdom - S\xfcndenbock.ts',
    u'description': u'S\xfcndenbock',
    u'tags': u'',
    u'filesize': 0,
    u'filesize_readable': u'',
    u'serviceref': u'1:0:0:0:0:0:0:0:0:0:/media/hdd/movie/20170830 1650 - TNT Serie HD (S) - Animal Kingdom - S\xfcndenbock.ts',
    u'filename': u'/media/hdd/movie/20170830 1650 - TNT Serie HD (S) - Animal Kingdom - S\xfcndenbock.ts',
    u'eventname': u'Animal Kingdom',
    u'length': u'?:??',
    u'servicename': u'TNT Serie HD (S)',
    u'begintime': u'30.8., 16:50',
    u'fullname': u'1:0:0:0:0:0:0:0:0:0:/media/hdd/movie/20170830 1650 - TNT Serie HD (S) - Animal Kingdom - S\xfcndenbock.ts',
    u'recordingtime': 1504104600,
    u'descriptionExtended': u'1. Staffel, Folge 5: XXXXX XXXXXXXXX XXXX XXXXXX D\xe4mxxxx XX xxxxxxXx XXX XXXXXXX xxxx XXXX XXXXX XX XXXXXXX XXX xxxx XX XXXXXXXX XXXXXXX XXXXXXX x\xe4xxxx XXX xxx XXXXX xxxx xxxxx XXX xxx XXXXXXX XXXX xx XXX XXXXX Xp\xfclxx X\xf6xxXXX X XXXX XXX XXXXXX XXXxxxxx xxx xxx xxxxx xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 50 Min.\n2016.\nAb 12 Jahren',
    u'lastseen': 0
}


class MoviefilesTestCase(unittest.TestCase):
    """
    This test suite shall be used to verify that current and future
    implementations of movie listing classes or functions generate the
    expected values for provided example files.

    The example files  are stripped copies of les files gennerated by
    an enigma2 device.
    """

    def setUp(self):
        self.enigma2_host = os.environ.get(ENV_VAR, ENV_VAL_FALLBACK)
        self.file_controller_url = "http://{netloc}/file?dir={dir}".format(
            netloc=self.enigma2_host, dir=MOVIE_FOLDER)
        self.api_controller_url = "http://{netloc}/api/movielist".format(
            netloc=self.enigma2_host)

    def testFilesResponseByFileController(self):
        req = requests.get(self.file_controller_url)
        self.assertTrue(req.status_code, 200)

        raw_data = req.json()
        data = raw_data[0]
        self.assertEqual(1, len(raw_data))
        self.assertTrue(data['result'])
        files = set(copy.copy(EXPECTED_FILES))
        common_files = set(data['files']) & files
        self.assertEqual(files, common_files)

    def testFilesResponseByApiController(self):
        req = requests.get(self.api_controller_url)
        self.assertTrue(req.status_code, 200)

        raw_data = req.json()
        data = raw_data['movies']
        found = 0
        movie_item = None
        for item in data:
            if item['filename'] == MAIN_TS_FILE:
                found += 1
                movie_item = item
        self.assertEqual(1, found)
        self.assertEqual("Animal Kingdom", movie_item['eventname'])
        self.assertEqual(movie_item, EXPECTED_MOVIE_ITEM)


if __name__ == '__main__':
    print("In order for this test to work the environment variable")
    print(">>> {var: ^70} <<<".format(var=ENV_VAR))
    print("needs to be set to the hostname/network location of an "
          "enigma2 device reachable by this script!")
    print("If this is not the case, the fallback value")
    print(">>> {val: ^70} <<<".format(val=ENV_VAL_FALLBACK))
    print("will be used!")
    print("")
    print("Following example files need to be put in {dir}:".format(
        dir=MOVIE_FOLDER))
    print("")
    for file_item in EXPECTED_FILES:
        print("* {!r}".format(file_item))
    print("")
    print("We will be using the network location {val!r} for this test".format(
        val=os.environ.get(ENV_VAR, ENV_VAL_FALLBACK)))
    print("")
    print("")
    unittest.main()
