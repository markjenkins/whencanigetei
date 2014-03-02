#!/usr/bin/env python
 
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>

# first argument is CSV file to load that has first column province,
# second column economic region code, third column region name,
# 4th column ei rate
# first line in file is ignore and assumed to contain field names
#
# second argument is start date this data applies to third argument is
# end date this applies to

# pytho imports
from sys import argv
from datetime import datetime
from csv import DictReader
from decimal import Decimal

# django imports
import django
django.setup()
from django.db import transaction

# from this project
from whenei.models import (
    EI_Economic_Place, Rate_For_Place_And_Time,
    )
from whenei.provinces import PROVINCES_AND_TERITORIES_NAME_TO_ABREV
from whenei.util import convert_date_string

def strip_suffix_if_present(place_name, suffix_to_strip):
    return (place_name if not place_name.endswith(suffix_to_strip)
            else place_name[:-len(suffix_to_strip)]
            ) # end ternary expression

def iso8859_1_to_utf8(msg):
    return msg.decode('iso-8859-1').encode('utf8')

def main():
    start_date, end_date = \
        convert_date_string(argv[2]), convert_date_string(argv[3])

    # to have your mind blown, READ PEP 343
    # http://legacy.python.org/dev/peps/pep-0343/
    with open(argv[1]) as f:
        # Not much RAM involved here, just buffer the whole thing into a
        # a tuple
        # drop the first dictionary by slicing because it contains the
        # line with
        csv_data_points = tuple(
            DictReader(f,
                       ('province', 'economic_region_code',
                        'economic_region_name', 'unemp_rate')
                       ))[1:]

    # again, to have your mind blown, READ PEP 343
    # http://legacy.python.org/dev/peps/pep-0343/
    with transaction.atomic():
        # first pass we load the EI_Economic_Place's out of this
        # with a generator expression passed to bulk_create
        EI_Economic_Place.objects.bulk_create(
            EI_Economic_Place(
                code=d['economic_region_code'],
                province=PROVINCES_AND_TERITORIES_NAME_TO_ABREV[
                    d['province'] ],
                name=iso8859_1_to_utf8(strip_suffix_if_present(
                            d['economic_region_name'], " (map)")),
                ) # EI_Economic_Place
            for d in csv_data_points
            )

        # second pass we load the Rate_For_Place_And_Time
        Rate_For_Place_And_Time.objects.bulk_create(
            Rate_For_Place_And_Time(
                economic_place=EI_Economic_Place.objects.get(
                    code=d['economic_region_code']),
                start_date=start_date,
                end_date=end_date,
                unemployment_rate=Decimal(d['unemp_rate']),
                )
            for d in csv_data_points
            )

if __name__ == "__main__":
    main()
