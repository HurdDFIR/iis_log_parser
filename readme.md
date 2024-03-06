# iis_log_parser.py
## Description
iis_log_parser.py is a tool that will convert IIS logs into a csv file. 

## Syntax
    usage: iis_log_parser.py [-h] -f INPUT_FILE -o OUTPUT_FILE [-v]

    iis_log_parser.py will go through an input IIS log and convert it to CSV format.

    options:
    -h, --help            show this help message and exit
    -f INPUT_FILE, --file INPUT_FILE
                            IIS log file to parse.
    -o OUTPUT_FILE, --output OUTPUT_FILE
                            Output file path. Output will be written in CSV format.
    -v, --verbose         Turn on verbose logging.

