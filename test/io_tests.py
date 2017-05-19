import os
import sys
import unittest

sys.path.append('../io/')
import read_data 

class io_test(unittest.TestCase):

    def test_read_data(self):
        d = read_data.epoch_to_datetime(1379879533)

        self.assertEqual(d.tm_year, 2013)
        self.assertEqual(d.tm_mon, 9)
        self.assertEqual(d.tm_mday, 22)
        self.assertEqual(d.tm_hour, 19)
        self.assertEqual(d.tm_min, 52)
        self.assertEqual(d.tm_sec, 13)


if __name__ == '__main__':
    unittest.main() 
