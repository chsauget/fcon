# Lakehouse to create or reuse in the current Fabric workspace
LAKEHOUSE_NAME = "Lakehouse_01"

# GitHub repository containing the CSV files
GITHUB_BASE_URL = "https://raw.githubusercontent.com/RuiRomano/workshop-fabcon-26-bcn/main"

# File paths relative to the repository root
CSV_FILES = [
    "resources/sample-data/dimension_city.csv",
    "resources/sample-data/dimension_customer.csv",    
    "resources/sample-data/fact_sale.csv",    
    "resources/sample-data/dimension_employee.csv",    
    "resources/sample-data/dimension_stock_item.csv",    
    "resources/sample-data/dimension_date.csv",    
]

import re
import time
from pathlib import PurePosixPath
from urllib.parse import quote
import requests


def table_name_from_file(file_path: str) -> str:
    """Create a valid table name from a CSV file name."""
    file_stem = PurePosixPath(file_path).stem
    table_name = re.sub(r"[^A-Za-z0-9_]", "_", file_stem)
    table_name = re.sub(r"_+", "_", table_name).strip("_").lower()

    if not table_name:
        raise ValueError(f"Cannot create a table name from: {file_path}")

    if table_name[0].isdigit():
        table_name = f"table_{table_name}"

    return table_name


def get_or_create_lakehouse(name: str):
    lakehouses = notebookutils.lakehouse.list()

    existing = next(
        (
            lakehouse
            for lakehouse in lakehouses
            if lakehouse.displayName.lower() == name.lower()
        ),
        None,
    )

    if existing:
        print(f"Using existing Lakehouse: {existing.displayName}")
        return existing

    created = notebookutils.lakehouse.create(
        name=name,
        description="Lakehouse used for the Fabric workshop",
    )

    print(f"Created Lakehouse: {created.displayName}")

    # Give OneLake a short period to make the new item available.
    time.sleep(10)

    return created

spark.conf.set('spark.sql.parquet.vorder.default', 'true')

lakehouse = get_or_create_lakehouse(LAKEHOUSE_NAME)

workspace_id = lakehouse.workspaceId
lakehouse_id = lakehouse.id

lakehouse_root = (
    f"abfss://{workspace_id}"
    f"@onelake.dfs.fabric.microsoft.com/{lakehouse_id}"
)

print(f"Workspace ID: {workspace_id}")
print(f"Lakehouse ID: {lakehouse_id}")

for csv_file in CSV_FILES:
    
    source_url = f"{GITHUB_BASE_URL.rstrip('/')}/{csv_file.lstrip('/')}"

    file_name = PurePosixPath(csv_file).name
    table_name = table_name_from_file(csv_file)

    raw_file_path = (
        f"{lakehouse_root}/Files/import/{file_name}"
    )
    table_path = (
        f"{lakehouse_root}/Tables/{table_name}"
    )

    print(f"Downloading {source_url}")

    response = requests.get(source_url, timeout=60)
    response.raise_for_status()

    # Keep a copy of the source CSV in the Files area.
    notebookutils.fs.put(
        raw_file_path,
        response.text,
        overwrite=True,
    )

    dataframe = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .option("mode", "FAILFAST")
        .csv(raw_file_path)
    )

    (
        dataframe.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .save(table_path)
    )

    print(f"Loaded {csv_file} into table {table_name}")