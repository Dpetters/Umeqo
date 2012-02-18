#! /bin/bash
source $1
cd $2
echo "`date`: SENDING MONTHLY NEWLETTER"
python manage.py send_monthly_newsletter 2>&1