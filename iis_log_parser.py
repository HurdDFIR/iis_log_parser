import csv
import logging
import argparse
import time
import traceback
import sys

l = logging.getLogger()
MAXINT = sys.maxsize
while True:
    try:
        csv.field_size_limit(MAXINT)
        break
    except OverflowError:
        MAXINT = int(MAXINT/10)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s [%(levelname)s] [%(lineno)d]  \t%(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
        'ignore_color': format
    }

    def __init__(self, ignore_color=False):
        self.ignore_color = ignore_color

    def format(self, record):
        if self.ignore_color:
            log_fmt = self.FORMATS.get('ignore_color')
        else:
            log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
    
def get_arguments():
    parser = argparse.ArgumentParser(description='iis_log_parser.py will go through an input IIS log and convert it to CSV format.')
    parser.add_argument('-f', '--file', dest='input_file', 
        action='store', type=str, default=None, required=True,
        help='IIS log file to parse.')
    parser.add_argument('-o', '--output', dest='output_file', 
        action='store', type=str, default=None, required=True,
        help='Output file path. Output will be written in CSV format.')
    parser.add_argument('-v', '--verbose', required=False, action='store_true', 
        help='Turn on verbose logging.')
    args = parser.parse_args()

    # Logging configuration
    if(args.verbose):
        l.setLevel(logging.DEBUG)
        #log handlers
        screen = logging.StreamHandler()
        screen.setLevel(logging.DEBUG)
        screen.setFormatter(CustomFormatter())
        #debug_log = logging.FileHandler('debug.log')
        #debug_log.setLevel(logging.DEBUG)
        #debug_log.setFormatter(CustomFormatter(ignore_color=True))
        l.addHandler(screen)
        #l.addHandler(debug_log)
    else:
        l.setLevel(logging.INFO)
        #log handlers
        screen = logging.StreamHandler()
        screen.setLevel(logging.INFO)
        screen.setFormatter(CustomFormatter())
        #debug_log = logging.FileHandler('debug.log')
        #debug_log.setLevel(logging.INFO)
        #debug_log.setFormatter(CustomFormatter(ignore_color=True))
        l.addHandler(screen)
        #l.addHandler(debug_log)

    return args

class IISLog:
    def __init__(self, log_file, output_file):
        self.log_file = log_file
        self.output_file = output_file

    def read_headers(self):
        with open(self.log_file, 'r', encoding='utf-8') as input:
            for line in input:
                if line.startswith('#Fields:'):
                    # gather headers
                    headers = line[9:].replace('\n','').split(' ')
                    break

            return headers


    def parse(self):
        # get the values, need to iterate
        with open(self.log_file, 'r', encoding='utf-8') as input, open(self.output_file, 'w', encoding='utf-8', newline='') as output:
            # Get the header keys and combine the date/time fields into one. 
            raw_keys = self.read_headers()
            first_index = str(raw_keys[0]) + ' ' + str(raw_keys[1])
            keys = []
            keys.append(first_index)
            for key in raw_keys[2:]:
                keys.append(key)

            csv_writer = csv.DictWriter(output, fieldnames=keys, dialect='unix')
            csv_writer.writeheader()

            for line in input:
                if not line.startswith('#'):
                    # gather values
                    raw_values = line.replace('\n','').split(' ')

                    date_time = str(raw_values[0]) + ' ' + str(raw_values[1])
                    # combine the first and second index of values
                    values = []
                    values.append(date_time)
                    for value in raw_values[2:]:
                        values.append(value)

                    # transpose to dict
                    csv_line_dict = dict(zip(keys, values))
                    csv_writer.writerow(csv_line_dict)

def main():
    start = time.time()
    try:
        args = get_arguments()
        iis_log = IISLog(args.input_file, args.output_file)
        iis_log.parse()


    except Exception as e:
        l.error(f'ERROR: {e}\n{traceback.format_exc()}')

    end = time.time()
    print("Execution time:\t" + str(end - start))
if __name__ == '__main__':
    main()