# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>

from django.db.models import (
    Model, PositiveIntegerField, CharField, DateField, DecimalField,
    ForeignKey,
    )

from .provinces import PROVINCES_AND_TERITORIES_ABREV_TO_NAME

# Create your models here.
class EI_Economic_Place(Model):
    code = PositiveIntegerField(
        primary_key=True)
    province = CharField(
        max_length=2,
        choices=tuple(PROVINCES_AND_TERITORIES_ABREV_TO_NAME.iteritems()),
        )
    name = CharField(max_length=100, unique=True)

class Rate_For_Place_And_Time(Model):
    economic_place = ForeignKey(EI_Economic_Place)

    # hey, is there someway we can get the DBMS to enforce that start_date
    # is before end_date?
    start_date = DateField()
    end_date = DateField()

    # unemployement rate is at most 100%, so four digits allows that and
    # the 0 after the decimal point
    unemployment_rate = DecimalField(decimal_places=1, max_digits=4)

    class Meta:
        unique_together = (
            ("economic_place", "start_date", "end_date"),
            )
