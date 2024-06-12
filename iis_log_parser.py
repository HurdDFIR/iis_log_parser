import csv
import logging
import argparse
import time
import traceback
import sys
import glob
from pathlib import Path
import os
from log import l, logger_setup

l = logging.getLogger()
MAXINT = sys.maxsize
while True:
    try:
        csv.field_size_limit(MAXINT)
        break
    except OverflowError:
        MAXINT = int(MAXINT/10)

class IISLog:
    def __init__(self, log_file, output_file, append=False):
        self.log_file = log_file
        self.output_file = output_file
        if append:
            self.mode = 'a'            
        else:
            self.mode = 'w'

    def read_headers(self):
        with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as input:
            for line in input:
                if line.startswith('#Fields:'):
                    # gather headers
                    headers = line[9:].replace('\n','').split(' ')
                    break

            return headers


    def parse(self):
        with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as input, open(self.output_file, self.mode, encoding='utf-8', newline='', errors='ignore') as output:
            # Get the header keys and combine the date/time fields into one. 
            raw_keys = self.read_headers()
            first_index = str(raw_keys[0]) + ' ' + str(raw_keys[1])
            keys = []
            keys.append(first_index)
            for key in raw_keys[2:]:
                keys.append(key)

            csv_writer = csv.DictWriter(output, fieldnames=keys, dialect='unix')
            # New file == writeheader()
            if self.mode == 'w':            
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


class FileList:
    def __init__(self, glob_pattern):
        self.glob_pattern = glob_pattern
        self.file_list = self._make_file_list()

    def _make_file_list(self):
        return glob.glob(self.glob_pattern, recursive=True, include_hidden=True)

def main():
    start = time.time()
    try:
        __version__ = '2.0.0'
        __author__ = 'Stephen Hurd | @HurdDFIR'
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='iis_log_parser will parse an IIS log and convert it to CSV format. This program supports the usage of glob patterns as well as multiple files/patterns at the command line.',
            epilog=f'v{__version__} | Author: {__author__}')

        parser.add_argument('-f', '--files', dest='glob_patterns', 
            action='extend', nargs='+', type=str, default=None, required=True,
            help='IIS log file to parse. This supports globbing patterns and a mulitple files/patterns (space separated).')
        parser.add_argument('-o', '--output', dest='output', 
            action='store', type=str, default=None, required=True,
            help='Output directory. Output will be written in CSV format.')
        parser.add_argument('--reduce_files', required=False, action='store_true', default=False,
            help='Reduces the number of files to one large file per IIS log directory.')
        parser.add_argument('-v', '--verbose', required=False, action='store_true', 
            help='Turn on verbose logging.')
        parser.add_argument('-q', '--quiet', required=False, action='store_true', 
            help='Enable quiet mode for reduced logging.')
        parser.add_argument('-l', '--logfile', required=False, type=str, dest='logfile', action='store', 
            help='File name to pipe log output to. Writes the file to the output directory.')
        
        args = parser.parse_args()
        
        if args.logfile:
            log_file = Path(args.output + '\\' + args.logfile).resolve()
        else:
            log_file = None
        logger_setup(verbose=args.verbose, quiet=args.quiet, log_file=log_file)

        l.info(f"IIS Log Parser is initiallizing..")
        file_list = []
        for pattern in args.glob_patterns:
            l.debug(f"Ingesting glob pattern: {pattern}")
            file_list += FileList(pattern).file_list
        
        num_files = len(file_list)

        l.debug(f"Found {num_files} files")

        if args.quiet:
            for i in range(num_files):
                f = Path(file_list[i])
                if f.is_file():
                    parent = str(f.parents[0]).split('\\')[-1]
                    if args.reduce_files:
                        outfile = Path(args.output + '\\' + str(parent) + '\\' + parent + '.csv')
                    else:
                        outfile = Path(args.output + '\\' + str(parent) + '\\' + f.stem + '.csv')
                    #l.debug(f'Parsing: {f} to: {outfile}')         
                    if outfile.exists():
                        iis_log = IISLog(f, outfile, append=True)
                        iis_log.parse()
                    else:
                        if outfile.parents[0].exists() == False:
                            os.makedirs(outfile.parents[0])
                        iis_log = IISLog(f, outfile)
                        iis_log.parse()  
        
        else :
            i = 0
            toolbar_width = 40
            for i in range(num_files):
                f = Path(file_list[i])
                if f.is_file():
                    parent = str(f.parents[0]).split('\\')[-1]
                    if args.reduce_files:
                        outfile = Path(args.output + '\\' + str(parent) + '\\' + parent + '.csv')
                    else:
                        outfile = Path(args.output + '\\' + str(parent) + '\\' + f.stem + '.csv')
                    #l.debug(f'Parsing: {f} to: {outfile}')         
                    if outfile.exists():
                        iis_log = IISLog(f, outfile, append=True)
                        iis_log.parse()
                    else:
                        if outfile.parents[0].exists() == False:
                            os.makedirs(outfile.parents[0])
                        iis_log = IISLog(f, outfile)
                        iis_log.parse()
                
                i += 1
                sys.stdout.write(f"[#]  Progress: {i}/{num_files}")
                sys.stdout.flush()
                sys.stdout.write("\b" * (toolbar_width+1))                

    except Exception as e:
        l.error(f'ERROR: {e}\n{traceback.format_exc()}')

    end = time.time()
    l.debug("Execution time:\t" + str(end - start))
if __name__ == '__main__':
    main()