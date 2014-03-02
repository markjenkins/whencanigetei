# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>


from json import dumps as json_dumps
from datetime import date

from django.http import HttpResponse

from whenei.models import (
    EI_Economic_Place, Rate_For_Place_And_Time,
    )
from whenei.unemp_rate_to_hours import unemp_rate_to_hours
from .util import convert_date_string

def handle_request(request):
    place = EI_Economic_Place.objects.get(code=int(request.GET['regionCode']))

    da_date = (
        date.today() if 'rate_date' not in request.GET
        else convert_date_string(request.GET['rate_date']) )

    rate_place = Rate_For_Place_And_Time.objects.get(
        start_date__lte=da_date,
        end_date__gte=da_date,
        economic_place=place,
        )

    hours_required = unemp_rate_to_hours(rate_place.unemployment_rate)
    try:
        hours_worked = int(request.GET['hoursWorked'])
    except ValueError:
        hours_worked = 0
    hours_remaining = (
        0 if hours_required <= hours_worked
        else hours_required - hours_worked )

    response = HttpResponse(
        json_dumps( {
                'regionName': place.name,
                'hours': str(hours_required),
                'unemp_rate': str(rate_place.unemployment_rate),
                'hoursToGo': str(hours_remaining),
                'start_date': str(rate_place.start_date),
                'end_date': str(rate_place.end_date),
                }),
        content_type="application/json; charset=utf-8")
    # we're cross site y'all, don't care 'bout that origin
    # https://developer.mozilla.org/en/docs/HTTP/Access_control_CORS
    response['Access-Control-Allow-Origin'] = '*'
    return response

