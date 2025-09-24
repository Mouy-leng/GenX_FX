import os
import csv

def verify_signal_file(filepath):
    """
    Verifies that the signal file exists and has the correct header.
    """
    if not os.path.exists(filepath):
        return False, "File not found"

    with open(filepath, 'r') as f:
        try:
            reader = csv.reader(f)
            header = next(reader)
        except StopIteration:
            return False, "File is empty"
        except csv.Error:
            return False, "File is not a valid CSV"

    expected_header = [
        'magic', 'symbol', 'signal', 'entryPriceStr',
        'stopLossStr', 'takeProfitStr', 'lotSizeStr', 'timestamp'
    ]

    if header != expected_header:
        return False, f"Invalid header. Expected {expected_header}, but got {header}"

    return True, "File is valid"