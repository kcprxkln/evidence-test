import datetime
from dataclasses import dataclass
import os
import shutil
import re
import yaml 


@dataclass 
class MonthInfo:
    name: str
    first_day: datetime.date
    last_day: datetime.date
    num_of_days: str
    year: int


def get_last_month_info() -> MonthInfo:
    """
    Get information about the previous month.

    Returns:
        MonthInfo: An object containing information about the previous month.
    """
    current_date = datetime.date.today()
    first_day_of_current_month = current_date.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - datetime.timedelta(days=1)
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
    length_of_previous_month = (last_day_of_previous_month - first_day_of_previous_month).days + 1
    month_name = first_day_of_previous_month.strftime("%B")
    year = first_day_of_previous_month.year
    month_data = MonthInfo(
        name=month_name,
        first_day=first_day_of_previous_month,
        last_day=last_day_of_previous_month,
        num_of_days=length_of_previous_month, 
        year = year 
    )
    return month_data


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def create_env_value(month_data: MonthInfo):
    month_name = month_data.name
    year = month_data.year

    new_month_env_value = month_name.lower() + "_" + str(year)
    return new_month_env_value


def replace_placeholders_in_md_template(new_file_name, md_filepath = "./evidence_template.md", output_path_prefix = "../evidence_project/pages/"):
    
    with open(md_filepath, 'r') as file:
        content = file.read()

    replaced_content = re.sub(r'PLACEHOLDER', new_file_name, content)

    os.makedirs(output_path_prefix, exist_ok=True)

    output_filepath = output_path_prefix + new_file_name + ".md"
    with open(output_filepath, 'w') as file:
        file.write(replaced_content)


def add_data_connection_yaml_file(new_file_name, output_path_prefix = "../evidence_project/sources/"):
    
    data = {
        # "# This file was automatically generated": None,
        "name": new_file_name,
        "type": "csv",
        "options": {}
    }

    output_filepath = output_path_prefix + new_file_name + "/connection.yaml"

    os.makedirs(output_path_prefix + new_file_name, exist_ok=True)

    with open(output_filepath, 'w') as yaml_file:
                yaml.dump(data, yaml_file)





