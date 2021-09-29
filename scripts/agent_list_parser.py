import os
import sys
from pathlib import Path

import openpyxl
import tablib

BASE_DIR = Path(__file__).resolve().parent.parent
FILE_NAME = Path(__file__).stem


def parse_file(file_name: str):
    xlsx_book = openpyxl.load_workbook(filename=file_name, data_only=True)

    dataset = tablib.Dataset()
    sheet = xlsx_book.active

    rows = sheet.rows
    dataset.headers = [
        'Distributor',
        'Agent Wallet No',
        'DSO',
        'MA',
        'Agent Type',
        'Registration Capability Status_4 - Aug - 21',
        'Agent Status',
        'Region',
        'Area',
        'Agent Shop Name',
        'Agent Name',
        'Shop Address',
        'Updated Division',
        'Updated District',
        'Updated Thana / Upazila',
        'Updated Union / Paurashava',
        'GEO Code',
        'Registration Date',
    ]

    col_size = 18
    for index, row in enumerate(rows):
        if index == 0:
            # header
            continue
        else:
            # main content
            dataset.append([row[i].value for i in range(col_size)])

    # print(dataset)
    return dataset


def import_data(data: tablib.Dataset):
    from django.utils.timezone import make_aware
    from location.models import Region, Area, Division, District, Upazila, Union
    from agent.models import Distributor, Agent, DSO, MA

    date_format = '%m/%d/%Y'

    agent_type_map = {
        'AGENT': 'agent',
        'bKash Care Agent': 'bkash_care_agent',
        'DAO': 'dao'
    }

    registration_capability_map = {
        'No Registration Capability': 'no_reg',
        'Digital': 'digital',
        'Digital+USSD': 'digital_ussd'
    }

    agent_status_map = {
        'ACTIVE': 'active',
        'INACTIVE': 'inactive'
    }

    for index, agent_info in enumerate(data):
        if index % 100 == 0:
            print(f'Processing {index} of {len(data)}')

        agent = Agent(
            # Basic information
            name=agent_info[10],
            distributor=Distributor.objects.get_or_create(name=agent_info[0])[0],
            dso=DSO.objects.get_or_create(mobile=agent_info[2])[0],
            ma=MA.objects.get_or_create(mobile=agent_info[3])[0],
            wallet_no=agent_info[1],
            shop_name=agent_info[9],
            shop_address=agent_info[11],

            # Status
            agent_type=agent_type_map.get(agent_info[4], 'agent'),
            status=agent_status_map.get(agent_info[6], 'inactive'),
            reg_capability=registration_capability_map.get(agent_info[5], 'no_reg'),

            # Location details
            region=Region.objects.get_or_create(name=str(agent_info[7]).title())[0],
            area=Area.objects.get_or_create(name=str(agent_info[8]).title())[0],
            geo_code=agent_info[16] or str(),
            reg_date=make_aware(agent_info[17]),
        )

        if agent_info[12]:
            agent.division = Division.objects.get_or_create(name=str(agent_info[12]).title())[0]

        if agent_info[13]:
            agent.district = District.objects.get_or_create(name=str(agent_info[13]).title())[0]

        if agent_info[14]:
            agent.upazila = Upazila.objects.get_or_create(name=str(agent_info[14]).title())[0]

        if agent_info[15]:
            agent.union = Union.objects.get_or_create(name=str(agent_info[15]).title())[0]

        agent.save()


def _setup_django():
    sys.path.append(BASE_DIR.as_posix())
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agent_tracker.settings')

    import django
    django.setup()


if __name__ == '__main__':
    _setup_django()

    res = parse_file('/Users/office/Downloads/agent_list.xlsx')
    import_data(data=res)
