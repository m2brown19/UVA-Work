import unittest
import btc_parse

class MyTestCase(unittest.TestCase):

    def test_preamble_same_line_start(self):
        f = open("blk00000-b29664.blk", "rb")
        all_lines = []
        for line in f:
            for byte in line:
                all_lines.append(byte)
        f.close()
        index = 0
        result = btc_parse.readPreamble(index, all_lines)

        self.assertEqual(('d9b4bef9', '00008f85', 8), result)

    def test_preamble_same_line_mid(self):
        f = open("blk00000-b29664.blk", "rb")
        all_lines = []
        for line in f:
            for byte in line:
                all_lines.append(byte)
        f.close()
        index = 16
        result = btc_parse.readPreamble(index, all_lines)

        self.assertEqual(('55ee864e', '0063d42b', 24), result)


    def test_preamble_diff_lines_even_split(self):
        f = open("blk00000-b29664.blk", "rb")
        all_lines = []
        for line in f:
            for byte in line:
                all_lines.append(byte)
        f.close()
        index = 482
        result = btc_parse.readPreamble(index, all_lines)

        self.assertEqual(('0a40c3da', '113d78fd', 490), result)

    def test_preamble_diff_lines_odd_split(self):
        f = open("blk00000-b29664.blk", "rb")
        all_lines = []
        for line in f:
            for byte in line:
                all_lines.append(byte)
        f.close()
        index = 485
        result = btc_parse.readPreamble(index, all_lines)

        self.assertEqual(('3d78fd0a', '0033b711', 493), result)

    def test_header(self):
        f = open("blk00000-b29664.blk", "rb")
        all_lines = []
        for line in f:
            for byte in line:
                all_lines.append(byte)
        f.close()
        index = 0
        result = btc_parse.readHeader(index, all_lines)
        print(result)

        self.assertEqual((80, 'd9b4bef9', '858f000001000000602bd8e84e86ee552bd46300cbc31e1961c03fa92d228b99',
                          '154aa99b8988e97b1f113d8076357a77572455574765a533000000007da75864',
                          'ad40afec', 'c5997d1c', '4b25b0c9'), result)


    def test_csuint(self):
        f = open("blk00000-b29664.blk", "rb")
        all_lines = []
        for line in f:
            for byte in line:
                all_lines.append(byte)
        f.close()
        #Test it on different sizes
        #1 byte
        index1byte = 0
        result = btc_parse.readCompactUInt(index1byte, all_lines)
        self.assertEqual((1, 'f9'), result)

        #2 byte
        index2byte = 227
        result = btc_parse.readCompactUInt(index2byte, all_lines)
        self.assertEqual((230, '0140'), result)


        #4 byte
        index4byte = 928 #fe
        result = btc_parse.readCompactUInt(index4byte, all_lines)
        self.assertEqual((933, '18a96911'), result)


        #8 byte
        index8byte = 799  # ff
        result = btc_parse.readCompactUInt(index8byte, all_lines)
        self.assertEqual((808, '57870f7f00ffffff'), result)

if __name__ == '__main__':
        unittest.main()