import datetime
from dataclasses import dataclass
import os 

@dataclass 
class MonthInfo:
    name: str
    first_day: datetime.date
    last_day: datetime.date
    num_of_days: str


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
    month_data = MonthInfo(
        name=month_name,
        first_day=first_day_of_previous_month,
        last_day=last_day_of_previous_month,
        num_of_days=length_of_previous_month
    )
    return month_data


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


