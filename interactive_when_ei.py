#!/usr/bin/env python

# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>

# python imports
from collections import OrderedDict
from datetime import date

# django imports
import django
django.setup()
from django.db import transaction

# from this project
from whenei.models import (
    EI_Economic_Place, Rate_For_Place_And_Time,
    )
from whenei.provinces import PROVINCES_AND_TERITORIES_ABREV_TO_NAME
from whenei.unemp_rate_to_hours import unemp_rate_to_hours

def print_provinces():
    print '\n'.join(
        '%s: %s' % (key, value)
        for key, value in PROVINCES_AND_TERITORIES_ABREV_TO_NAME.iteritems()
        )

def print_places(places):
    print '\n'.join('%s: %s' % (place.code, place.name)
                    for place in places.values() )
        
def main():
    province = None
    while province not in PROVINCES_AND_TERITORIES_ABREV_TO_NAME:
        print_provinces()
        province = raw_input("When province are you from? > ").upper()
        print

    places_cache = OrderedDict(
        (place.code, place)
        for place in 
        EI_Economic_Place.objects.filter(province=province)
        )

    place_choice = -1
    while place_choice not in places_cache:
        print_places(places_cache)
        try:
            place_choice = int( raw_input("And where exactly? > "))
        except ValueError: pass
        print
    
    today = date.today()
    rate = Rate_For_Place_And_Time.objects.get(
        start_date__lte=today,
        end_date__gte=today,
        economic_place=place_choice
        ).unemployment_rate
    
    print "you need %s hours in %s with it's %s%% unemployment rate" % (
        unemp_rate_to_hours(rate), places_cache[place_choice].name, rate)

if __name__ == "__main__":
    main()
