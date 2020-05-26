import unittest
import logging

from main import UnpackJSON 
from main import Timestamp
from main import VerifyHash

TIMESTAMP_JSON = [
    [   
      "sha256",
      "",
      "e3be16e996ecf573979ca58498c50029"
    ],
    [
      "sha256",
      "",
      "a74fe7cf3fa4c5847a47c3c8e6ee85094bcbda0c50b05848eef67c96ef8867f5"
    ]
]


""" This class uses PEP8 styling """
class TestLoading(unittest.TestCase):

    def test_unpack_json_wrong_type(self):
        try:
            UnpackJSON({})
        except Exception as e:
            pass
        else:
            raise AssertionError("Should have thrown an exception")

    def test_unpack_json_none(self):
        self.assertEqual(UnpackJSON([]), [])

    """ ensure JSON is unpacked as expected """
    def test_unpack_json(self):
        unpacked_json = UnpackJSON(TIMESTAMP_JSON)
        self.assertEqual(len(unpacked_json), 2)        

        counter = 0
        for timestamp in unpacked_json:
            self.assertTrue(isinstance(timestamp, Timestamp))
            self.assertEqual(timestamp.operator, "sha256")
            self.assertEqual(timestamp.prefix, "")

            if (counter == 0):
                self.assertEqual(timestamp.postfix, "e3be16e996ecf573979ca58498c50029")
            else:
                self.assertEqual(timestamp.postfix, "a74fe7cf3fa4c5847a47c3c8e6ee85094bcbda0c50b05848eef67c96ef8867f5")
                
            counter += 1

    def test_unpack_json_unknown_operator(self):

        BAD_OPERATOR_JSON = [
            [   
              "operator that doesn't exist",
              "prejunk",
              "postjunk"
            ]
        ]

        unpacked_json = UnpackJSON(BAD_OPERATOR_JSON)

        try:
            VerifyHash(unpacked_json, "abc", "def")
        except Exception as e:
            pass
        else:
            raise AssertionError("Should have thrown an exception for unknown operator")

        
    def test_verify_hash_none(self):
        try:
            VerifyHash([], "abc", "def")
        except Exception as e:
            self.assertTrue(isinstance(e, ValueError))
        else:
            raise AssertionError("Should have thrown an exception")


    def test_verify_hash_one(self):
        verify_status = VerifyHash([Timestamp("sha256", "abc", "def")], "abcdef", "9cd3f75605488339730b17f14d143ad228a16c84ecb283be7e890ecb606fc0a7")
        self.assertTrue(verify_status)

    # def test_verify_hash_json(self)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
