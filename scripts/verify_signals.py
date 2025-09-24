import os
import sys

# Add the parent directory to the Python path to allow for package imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.verification import verify_signal_file

def main():
    """
    Verifies the MT4_Signals.csv file.
    """
    # The EA looks for the file in the MQL4/Files directory, which we will simulate here
    # In a real-world scenario, this script would be run in a context where this path is accessible
    signals_file = "MT4_Signals.csv"

    is_valid, message = verify_signal_file(signals_file)

    if is_valid:
        print(f"Success: {message}")
        sys.exit(0)
    else:
        print(f"Error: {message}")
        sys.exit(1)

if __name__ == "__main__":
    main()