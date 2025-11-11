#!/bin/python3kX
import subprocess
import sys
import logging
import os
import argparse
from typing import Optional, Literal
import importlib

# Check for required modules
required_modules = {
    "pydantic": "pydantic",
    "pymysql": "PyMySQL",
    "pydantic_yaml": "pydantic-yaml",
    "yaml": "PyYAML",
    "cryptography": "cryptography"
}
missing_modules = []

for module, package in required_modules.items():
    try:
        importlib.import_module(module)
    except ImportError:
        missing_modules.append(package)

if missing_modules:
    print(f"Missing required modules: {', '.join(missing_modules)}. Installing in 10 seconds...")
    import time
    time.sleep(10)
    subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_modules])
    print("Modules installed. Please re-run the script.")
    sys.exit(255)

from pydantic import BaseModel, Field, field_validator, ValidationError
from pymysql import connect
import yaml

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) 
logger.addHandler(logging.StreamHandler(stream=sys.stderr))

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        args = {'prog': self.prog, 'message': message}
        self.exit(1, ('%(prog)s: error: %(message)s\n') % args)

parser = CustomArgumentParser(description="""
This tool can be used to generate an import script for MySQL or import into 
a MySQL database directory.
All logging will print to stderr.""",
exit_on_error=False, # We handle exit in our custom error method
formatter_class=argparse.ArgumentDefaultsHelpFormatter,
add_help=True)
parser.add_argument("-i", "--input-dir", help="Directory to scan for food files, or to source allowed_dietary_restrictions.txt for schema export.", action="store")
schemagroup = parser.add_argument_group('schema options')
schemagroup.description = """
    Export a schema to STDOUT (helpful for an AI to generate or organize data into an expected format).
    Can be combined with -i to include dietary restrictions from a specific file.
"""
schema_ex_group = schemagroup.add_mutually_exclusive_group(required=False)
schema_ex_group.add_argument("-y", "--yaml-schema", help="Output the expected yaml schema to STDOUT as yaml, then exit", action="store_true")
schema_ex_group.add_argument("-S", "--schema", help="Output the expected yaml schema to STDOUT as json, then exit", action="store_true")
parser.add_argument("-o", "--output", default=None, help="output SQL to file instead of importing", action="store")
parser.add_argument("-I", "--ignore-import-error", action="store_true", help="Ignore and skip over data files that failed to parse")
debug_group = parser.add_argument_group('Logging Options')
debug_group.description ="""
Changes logging output settings on the level of verbosity.
Default: Warnings and Errors only.
"""
ex_debug_group = debug_group.add_mutually_exclusive_group(required=False)
ex_debug_group.add_argument('-D','--debug',action="store_true",help="Enable debug logging")
ex_debug_group.add_argument('-q','--quiet',action="store_true",help="Disable logging (errors only)")
ex_debug_group.add_argument('-v','--verbose',action="store_true",help="Enable verbose logging")

db_group = parser.add_argument_group('database options')
db_group.description ="""
Instead of outputting a file or stdout, this will import into a MySQL database directly.
Not compatible with the --output option.
"""
db_group.add_argument("-H", "--host", default="localhost", help="database host")
db_group.add_argument("-P", "--port", default=3306, type=int, help="database port")
db_group.add_argument("-u", "--user", default="root", help="database user")
db_group.add_argument("-p", "--password", default="", help="database password")
db_group.add_argument("-d", "--database", default="allergysnatcher", help="database name")
db_group.add_argument("-s", "--ssl", default=False, action="store_true", help="enable SSL")

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

# Argument validation
if not args.input_dir and not (args.yaml_schema or args.schema):
    parser.error("No action requested. Use -i to import data, or --schema/--yaml-schema to export schema.")

if args.input_dir and not (args.yaml_schema or args.schema or db_arg_used or args.output):
    # If -i is specified, but no output action (schema, db, or file), assume they want to print SQL to stdout
    logger.info("No output specified with -i. Defaulting to printing SQL to STDOUT.")

if not args.input_dir and (db_arg_used or args.output):
    parser.error("-i/--input-dir is required when specifying an output (database or file).")

dbengine = None
if db_arg_used:
    try:
        dbengine = connect(host=args.host, port=args.port, user=args.user, password=args.password, database=args.database, ssl=args.ssl)
        logger.info("Connected to database")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        sys.exit(2)

if args.output and db_arg_used:
    parser.error("argument -o/--output: not allowed with database options")
    sys.exit(1)

if args.debug:
    logger.setLevel(logging.DEBUG)
    logger.debug("Debug logging enabled")
elif args.quiet:
    logger.setLevel(logging.ERROR)
elif args.verbose:
    logger.setLevel(logging.INFO)
    logger.debug("Verbose logging enabled")
else:
    logger.setLevel(logging.WARNING)
    logger.debug("Logging disabled")

from pydantic_yaml import parse_yaml_file_as

def create_models(input_dir: Optional[str] = None):
    """
    Dynamically creates the Pydantic models, loading dietary restrictions
    from the specified input directory if provided.
    """
    DietaryRestrictionEnum = str
    allowed_restrictions_list = []

    if input_dir and os.path.isdir(input_dir):
        restrictions_path = os.path.join(input_dir, 'allowed_dietary_restrictions.txt')
        if os.path.exists(restrictions_path):
            try:
                with open(restrictions_path, 'r') as f:
                    allowed_restrictions_list = [line.strip() for line in f if line.strip()]
                if allowed_restrictions_list:
                    DietaryRestrictionEnum = Literal[tuple(allowed_restrictions_list)]
                    logger.info(f"Loaded {len(allowed_restrictions_list)} dietary restrictions from {restrictions_path}")
            except Exception as e:
                logger.warning(f"Could not read {restrictions_path}: {e}. No restrictions will be validated in schema.")
        else:
            logger.warning(f"No 'allowed_dietary_restrictions.txt' found in '{input_dir}'.")
    elif args.yaml_schema or args.schema:
        logger.warning("No input directory provided with -i. No dietary restrictions will be added to the schema.")


    class Fats(BaseModel):
        total: float
        saturated: float
        trans: float

    class Servings(BaseModel):
        size: float = Field(description="Serving size in per the unit field")
        calories : float = Field(description="Calories per serving")
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
        name: str = Field(description="Name of the food", max_length=255)
        brand: str = Field(description="Brand of the food", max_length=100)
        ingredients: list[str] = Field(description="List of ingredients")
        nutrition: Nutrition = Field(description="Nutrition information (all fields expected in grams, convert prior to entry)")
        servings: Servings = Field(description="Serving information")
        category: str = Field(description="Category of the food (normalize at lowercase)", examples=["ingredient","frozen entry","grains","baking","fish","prepared meal"])
        cuisine: Optional[str] = Field(description="Cuisine of the food (normalize at lowercase)", examples=["american","italian","tex-mex","mexican"])
        dietary_restrictions: list[DietaryRestrictionEnum] = Field(default=[], description="List of dietary restrictions")
        
        @field_validator('dietary_restrictions')
        def check_dietary_restrictions(cls, v: list[str]):
            if not allowed_restrictions_list:
                return v # No validation possible
            if isinstance(v, list):
                for restriction in v:
                    if restriction not in allowed_restrictions_list:
                        raise ValueError(f"Dietary restriction '{restriction}' is not in the allowed list.")
            else:
                raise TypeError('dietary_restrictions must be a list.')
            return v

    return Food

Food = create_models(args.input_dir)

if args.yaml_schema or args.schema:
    schema = Food.model_json_schema() #Export schema
    if args.schema:
        import json
        print(json.dumps(schema, indent=2))
    else:
        print(yaml.dump(schema, default_flow_style=False))
    sys.exit(0)

inputDir = args.input_dir
if not os.path.isdir(inputDir) or not os.path.exists(inputDir):
    logger.error("Input directory does not exist")
    sys.exit(4)

# Get file list
file_list = []
for root, dirs, files in os.walk(inputDir):
    for file in files:
        if file.endswith(".yaml") or file.endswith(".yml") or file.endswith(".json"):
            file_list.append(os.path.join(root, file))

foods : list[Food] = []
# Parse yml files
for file in file_list:
    try:
        with open(file, 'r') as f:
            if file.endswith('.json'):
                food = Food.model_validate_json(f.read())
            else:
                food = parse_yaml_file_as(Food, f)
        foods.append(food)
        logger.info(f"Parsed and validated {file}")
        logger.debug(f"Validated {file}: Food({food})")
    except (ValueError, ValidationError, yaml.YAMLError) as e:
        if args.ignore_import_error:
            logger.warning(f"Failed to parse or validate {file}: {e}")
            continue
        else:
            logger.error(f"Failed to parse or validate {file}: {e}")
            sys.exit(3)

dbscript = """-- Allergy Snatcher Food Import Script
-- Generated by dataimport.py

-- Create a placeholder 'System' user for data attribution
-- and set a variable for its ID.
INSERT IGNORE INTO users (username, email, role, first_name) VALUES ('System', 'system@local.host', 'admin', 'System');
SET @system_user_id = (SELECT id FROM users WHERE username = 'System');

"""

def sql_str(value):
    """Safely formats a Python value for a SQL string literal."""
    if value is None:
        return "NULL"
    # Escape single quotes by doubling them up
    escaped_value = str(value).replace("'", "''")
    return f"'{escaped_value}'"

for food in foods:
    # --- Category and Cuisine Handling ---    
    category = food.category
    cuisine = food.cuisine
    
    dbscript += f"-- Processing food: {food.name}\n"
    if category:
        dbscript += f"INSERT IGNORE INTO categories (category) VALUES ({sql_str(category)});\n"
        dbscript += f"SET @category_id = (SELECT id FROM categories WHERE category = {sql_str(category)});\n"
    else:
        dbscript += "SET @category_id = NULL;\n"

    if cuisine:
        dbscript += f"INSERT IGNORE INTO cuisines (cuisine) VALUES ({sql_str(cuisine)});\n"
        dbscript += f"SET @cuisine_id = (SELECT id FROM cuisines WHERE cuisine = {sql_str(cuisine)});\n"
    else:
        dbscript += "SET @cuisine_id = NULL;\n"

    # --- Main Food Record Insert ---
    nutrition = food.nutrition
    fats = nutrition.fats
    servings = food.servings

    food_insert_sql = f"""INSERT INTO foods (
    name, brand, publication_status, cal, dietary_fiber, sugars, protein, carbs,
    cholesterol, sodium, trans_fats, total_fats, sat_fats, serving_amt, serving_unit,
    user_id, category_id, cuisine_id
) VALUES (
    {sql_str(food.name)},
    {sql_str(food.brand)},
    'public',
    {servings.calories},
    {nutrition.dietary_fiber},
    {nutrition.total_sugars},
    {nutrition.protein},
    {nutrition.carbohydrates},
    {nutrition.cholesterol},
    {nutrition.sodium},
    {fats.trans},
    {fats.total},
    {fats.saturated},
    {servings.size},
    {sql_str(servings.unit)},
    @system_user_id,
    @category_id,
    @cuisine_id
);\n"""
    dbscript += food_insert_sql
    dbscript += "SET @food_id = LAST_INSERT_ID();\n\n"

    # --- Ingredients Insert ---
    ingredients = food.ingredients
    if ingredients:
        dbscript += "-- Ingredients\n"
        for ingredient in ingredients:
            dbscript += f"INSERT INTO ingredients (food_id, ingredient_name) VALUES (@food_id, {sql_str(ingredient)});\n"
        dbscript += "\n"

    # --- Dietary Restrictions Insert ---
    restrictions = food.dietary_restrictions
    if restrictions:
        dbscript += "-- Dietary Restrictions\n"
        for restriction in restrictions:
            dbscript += f"INSERT IGNORE INTO dietary_restrictions (restriction) VALUES ({sql_str(restriction)});\n"
            dbscript += f"SET @restriction_id = (SELECT id FROM dietary_restrictions WHERE restriction = {sql_str(restriction)});\n"
            dbscript += f"INSERT IGNORE INTO diet_restrict_assoc (food_id, restriction_id) VALUES (@food_id, @restriction_id);\n"
        dbscript += "\n"

    dbscript += "\n"
dbscript += "UPDATE foods SET publication_status = 'public' WHERE user_id = @system_user_id;\n"

if args.output:
    with open(args.output, 'w') as f:
        f.write(dbscript)
else:
    if dbengine is not None:
        try:
            with dbengine.cursor() as cursor:
                # PyMySQL does not support multi-statement queries in a single .execute() call.
                # We must split the script into individual statements and execute them one by one.
                for statement in dbscript.split(';'):
                    # Skip empty statements that can result from splitting
                    if statement.strip():
                        cursor.execute(statement)
                dbengine.commit()
        except Exception as e:
            logger.error(f"Failed to execute database script: {e}")
            sys.exit(2)
    else:
        print(dbscript)
sys.exit(0)