# iis_log_parser.py
## Description
iis_log_parser.py is a tool that will convert IIS logs into a csv file. 

## Syntax
    usage: iis_log_parser.py [-h] -f GLOB_PATTERNS [GLOB_PATTERNS ...] -o OUTPUT [--reduce_files] [-v] [-q] [-l LOGFILE]

    iis_log_parser will parse an IIS log and convert it to CSV format. This program supports the usage of glob patterns as well as multiple files/patterns at the command line.

    options:
    -h, --help            show this help message and exit
    -f GLOB_PATTERNS [GLOB_PATTERNS ...], --files GLOB_PATTERNS [GLOB_PATTERNS ...]
                            IIS log file to parse. This supports globbing patterns and a mulitple files/patterns (space separated). (default: None)
    -o OUTPUT, --output OUTPUT
                            Output directory. Output will be written in CSV format. (default: None)
    --reduce_files        Reduces the number of files to one large file per IIS log directory. (default: False)
    -v, --verbose         Turn on verbose logging. (default: False)
    -q, --quiet           Enable quiet mode for reduced logging. (default: False)
    -l LOGFILE, --logfile LOGFILE
                            File name to pipe log output to. Writes the file to the output directory. (default: None)

    v2.0.0 | Author: Stephen Hurd | @HurdDFIR

## Installation
Run this command to install the required packages for this program:

    pip install -r requirements.txt