This software was written for the Canadian Open Data Experience hackathon
https://canadianopendataexperience.com/

Premise: You are working as a temp or have otherwise insecure unemployement. For the sake of your prayers you ask, "How much longer do I have to work until I have the security of EI elegibility?"
("merciful god! May this job last at least that long")

In our EI system, the answer can be complicated depending on your work history and history with the EI system.

But, in the simple cases it comes down to how many hours you've worked in the last year, how many hours a week you are working now, and where in the country you are. In places with high unemployment rates, less EI eligible hours are required, in places with low unemployment rates, more are hours required.

If you're a time traveler trying to answer this for some poor soul in the past, you can find lots of historic unemployment rates for the different regions here:
http://data.gc.ca/data/en/dataset/aad2bcd4-9f45-4013-b2a6-8367106dc0b2

If you care about the rates of today, you should refer to this Service Canada table:
http://srv129.services.gc.ca/eiregions/eng/rates_cur.aspx
which I have copy-pasted to unemployement_rates_feb9_march8_2014.csv

The initial versions of this application will be based on that. Time permitting, I may also add a time-travel feature so that the data from data.gc.ca can have a purpose.

-----------
So, how do you use this?
You need to download and install Django 1.7 (which is currently in alpha stage)
https://www.djangoproject.com/download/

Install it somewhere that's in your default sys.path or set PYTHON_PATH to include it and this source code directory.

Also have the django-admin from this available in PATH

Customize sqlite_test_settings.py to your likeing and put DJANGO_SETTINGS_MODULE=sqlite_test_settings in your environment.

create your database
$ django-admin syncdb

check out the SQL schema this has created
$ django-admin sqlall

load the CSV file
./load_unemployement_rates.py unemployement_rates_feb9_march8_2014.csv \
 2014-2-9 2014-3-8

Look at the pretty data dump
django-admin dumpdata

And well that's all we've got so far. Happy hacking.
