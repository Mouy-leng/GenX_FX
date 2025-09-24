import unittest
import os
import csv
from utils.verification import verify_signal_file

class TestSignalFileVerification(unittest.TestCase):

    def setUp(self):
        self.valid_file = 'valid_signals.csv'
        self.empty_file = 'empty_signals.csv'
        self.invalid_header_file = 'invalid_header_signals.csv'
        self.nonexistent_file = 'nonexistent_signals.csv'

        with open(self.valid_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['magic', 'symbol', 'signal', 'entryPriceStr', 'stopLossStr', 'takeProfitStr', 'lotSizeStr', 'timestamp'])
            writer.writerow(['123', 'EURUSD', 'BUY', '1.1', '1.0', '1.2', '0.1', '2023-01-01'])

        with open(self.empty_file, 'w') as f:
            pass

        with open(self.invalid_header_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'symbol', 'action', 'entry_price', 'stop_loss', 'take_profit', 'confidence', 'reasoning', 'source'])

    def tearDown(self):
        for f in [self.valid_file, self.empty_file, self.invalid_header_file]:
            if os.path.exists(f):
                os.remove(f)

    def test_valid_file(self):
        is_valid, message = verify_signal_file(self.valid_file)
        self.assertTrue(is_valid)
        self.assertEqual(message, "File is valid")

    def test_nonexistent_file(self):
        is_valid, message = verify_signal_file(self.nonexistent_file)
        self.assertFalse(is_valid)
        self.assertEqual(message, "File not found")

    def test_empty_file(self):
        is_valid, message = verify_signal_file(self.empty_file)
        self.assertFalse(is_valid)
        self.assertEqual(message, "File is empty")

    def test_invalid_header(self):
        is_valid, message = verify_signal_file(self.invalid_header_file)
        self.assertFalse(is_valid)
        self.assertTrue("Invalid header" in message)