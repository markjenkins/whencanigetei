# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>

from bisect import bisect_left
from collections import OrderedDict

# from http://www.servicecanada.gc.ca/eng/ei/types/regular.shtml#Number 
# a dictionary where the keys are maximum unemployment rate and the required
# hours when a region has up to that rate
# meaning 6% or less is 700 hours
# 6 < n <= 7 is 665
#
# by using enumerate, we automatically get an interation of these key values
# starting from 6 pairs with our hours numbers for constructing this dictionary
unemp_rate_ranges_to_hours_table = OrderedDict(
    enumerate( (700, 665, 630, 595, 560, 525, 490, 455, 420), 6 )
    )

# cache all the keys from above for searching (6, 7, 8...)
unemp_rate_ranges_to_hours_table_ordered_keys = tuple(
    unemp_rate_ranges_to_hours_table.keys()
    ) # to work with python 3, not thread safe...
# http://blog.labix.org/2008/06/27/watch-out-for-listdictkeys-in-python-3

def unemp_rate_to_hours(unemp_rate):
    # find which of the keys in unemp_rate_ranges_to_hours_table_ordered_keys
    # that we're less than or equal to
    table_index = bisect_left( unemp_rate_ranges_to_hours_table_ordered_keys,
                               unemp_rate)
    # if bisect_left provides an index too large, we go with the last entry
    if table_index == len(unemp_rate_ranges_to_hours_table_ordered_keys):
        table_index = len(unemp_rate_ranges_to_hours_table_ordered_keys)-1

    rate_key = unemp_rate_ranges_to_hours_table_ordered_keys[table_index]

    # now that we have a rate key, use it to look up the hours
    return unemp_rate_ranges_to_hours_table[rate_key]

if __name__ == "__main__":
    from decimal import Decimal
    for i in range(5, 14+1):
        print Decimal(i), unemp_rate_to_hours(Decimal(i))
        print Decimal(i) + Decimal('0.5'), \
            unemp_rate_to_hours(Decimal(i) + Decimal('0.5'))
