#!/bin/python3
import subprocess
import sys
import logging
import os
import argparse
from typing import Optional, Literal

try:
    from pydantic import BaseModel, Field, field_validator, ValidationError
except ImportError:
    logging.info("pydantic not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydantic"])
    from pydantic import BaseModel, Field, field_validator, ValidationError

try:
    from pymysql import connect
except ImportError:
    logging.info("PyMySQL not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyMySQL"])
    from pymysql import connect

try:
    import yaml
except ImportError:
    logging.info("PyYAML not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyYAML"])
    import yaml

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
parser.add_argument("-i", "--input-dir", help="directory to scan for food files", required=True, action="store")
parser.add_argument("-o", "--output", default=None, help="output SQL to file instead of importing", action="store")
parser.add_argument("-I", "--ignore-import-error", action="store_true", help="Ignore and skip over data files that failed to parse")
parser.add_argument('-D','--debug',action="store_true",help="Enable debug logging")

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
if not os.path.isdir(inputDir) or not os.path.exists(inputDir):
    logger.error("Input directory does not exist")
    sys.exit(4)

if args.debug:
    logger.setLevel(logging.DEBUG)

### START VALIDATION MODELS ###
class Fats(BaseModel):
    total: float
    saturated: float
    trans: float

class Servings(BaseModel):
    size: float
    unit: Literal['g','mg', 'oz','lb', 'tsp', 'tbsp', 'cup', 'item']

class Nutrition(BaseModel):
    fats: Fats
    cholesterol: float
    sodium: float
    carbohydrates: float
    dietary_fiber: float
    total_sugars: float
    added_sugars: float
    protein: float

class Food(BaseModel):
    name: str
    brand: str
    ingredients: list[str]
    nutrition: Nutrition
    servings: Servings
    category: str
    cuisine: Optional[str]
    dietary_restrictions: list[str] = Field(default=[])
    
    @field_validator('dietary_restrictions')
    def check_dietary_restrictions(cls, v: list[str]):
        allowed_restrictions_list = None
        if v == '[]':
            v = []
        if os.path.exists(f"{inputDir}/allowed_dietary_restrictions.txt"):
            with open(f"{inputDir}/allowed_dietary_restrictions.txt", 'r') as f:
                allowed_restrictions_list = f.readlines()
                allowed_restrictions_list = [x.strip() for x in allowed_restrictions_list]
        if allowed_restrictions_list is not None and isinstance(v, list):
            for restriction in v:
                if restriction not in allowed_restrictions_list:
                    raise ValueError(f"Dietary restriction '{restriction}' is not allowed.")
        elif not isinstance(v, list):
            raise ValueError(f"Dietary restrictions must be a list, but got '{type(v)}'.")
        return v
### END VALIDATION MODELS ###


# Get file list
file_list = []
for root, dirs, files in os.walk(inputDir):
    for file in files:
        if file.endswith(".yaml") or file.endswith(".yml"):
            file_list.append(os.path.join(root, file))

foods : list[Food] = []
# Parse yml files
for file in file_list:
    with open(file, 'r') as f:
        food = None
        try:
            food = yaml.load(f,yaml.FullLoader)
            logger.debug(f"Parsed {file}:{food}")
        except yaml.YAMLError as e:
            if args.ignore_import_error:
                logger.warning(f"Failed to parse {file}: {e}")
            else:
                logger.error(f"Failed to parse {file}: {e}")
                sys.exit(3)
        if food is not None:
            try:
                food = Food(**food)
                Food.model_validate(food)
                foods.append(food)
            except (ValueError, ValidationError) as e:
                if args.ignore_import_error:
                    logger.warning(f"Failed to validate {file}: {e}")
                    continue
                else:
                    logger.warning(f"Failed to validate {file}: {e}")
                    sys.exit(3)
