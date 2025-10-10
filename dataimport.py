from pydantic import BaseModel, Field
from typing import Optional
from pymysql import connect
import argparse
import sys
import logging
import File
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) 
logger.addHandler(logging.StreamHandler())
 
parser = argparse.ArgumentParser(prog="Allergy Snatcher Food Import Tool",
                                 description="""
This tool can be used to generate an import script for MySQL or import into 
a MySQL database directory.""",
exit_on_error=True,
formatter_class=argparse.ArgumentDefaultsHelpFormatter,
add_help=True)
parser.add_argument("-i", "--input-dir", help="directory to scan for food files", required=True)
parser.add_argument("-o", "--output", default=None, help="output SQL to file instead of importing")
parser.add_argument("-I", "--ignore-import-error", action="store_true", help="Ignore and skip over data files that failed to parse")

db_group = parser.add_argument_group('database options')
db_group.add_argument("-H", "--host", default="localhost", help="database host")
db_group.add_argument("-P", "--port", default=3306, type=int, help="database port")
db_group.add_argument("-u", "--user", default="root", help="database user")
db_group.add_argument("-p", "--password", default="", help="database password")
db_group.add_argument("-d", "--database", default="allergysnatcher", help="database name")
db_group.add_argument("-s", "--ssl", action="store_true", help="enable SSL")

parser.epilog = """
Exit codes:
    0 = success
    1 = invalid arguments
    2 = database connection error
    3 = data files parsing error have occurred
    4 = input directory not found
"""

args = parser.parse_args()

db_opts = ['-H', '--host', '-P', '--port', '-u', '--user', '-p', '--password', '-d', '--database', '-s', '--ssl']
db_arg_used = any(arg in sys.argv for arg in db_opts)

if args.output and db_arg_used:
    parser.error("argument -o/--output: not allowed with database options")
    sys.exit(1)

inputDir = args.input_dir
if os.path.isdir(inputDir) and os.path.exists(inputDir):
    logger.error("Input file does not exist")
    sys.exit(4)


