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

# python imports
from sys import argv
from csv import reader
from datetime import date
from decimal import Decimal

# django imports
import django
django.setup()

# from this project
from whenei.models import (
    EI_Economic_Place, Rate_For_Place_And_Time,
    )

MONTHS = ( "january", "february", "march", "april",
           "may", "june", "july", "august", "september",
           "october", "november", "december"
    )
MONTH_dict = {
    month.upper(): i
    for i, month in enumerate(MONTHS, 1)
    }

def convert_mon_day_pair(mon_day_string, year):
    (month_name, day_num) = mon_day_string.split(" ")
    return date( year, MONTH_dict[month_name], int(day_num) )

def main():
    places = {
        place.code: place
        for place in EI_Economic_Place.objects.all()
        }

    with open(argv[1]) as f:
        # buffer all the lines and reverse them
        lines = list(reader(f))
        lines.reverse()

        # first line is a title
        lines.pop()

        # second line provides year
        year_line = lines.pop()
        year = int(year_line[2])

        # third line start month and days
        start_month_days = lines.pop()
        start_month_days = start_month_days[2:]
        start_month_days = [
            start_mon_day.strip("/")
            for start_mon_day in start_month_days
            ]

        start_month_days = [
            convert_mon_day_pair(start_mon_day, year)
            for start_mon_day in start_month_days
            ]


        # forth line end month and days
        end_month_days = lines.pop()
        end_month_days = end_month_days[2:]
        end_month_days = [
            convert_mon_day_pair(end_month_day, year)
            for end_month_day in end_month_days
            ]

        # fith line headings
        lines.pop()

        lines.reverse()

        for line in lines:
            try:
                code = int(line[0])
            except ValueError: pass
            else:
                rates = line[2:]
                Rate_For_Place_And_Time.objects.bulk_create(
                    Rate_For_Place_And_Time(
                        economic_place=places[code],
                        start_date = start_month_days[i],
                        end_date = end_month_days[i],
                        unemployment_rate=Decimal(rate),
                        )
                    for i, rate in enumerate(rates)
                    )


if __name__ == "__main__":
    main()
