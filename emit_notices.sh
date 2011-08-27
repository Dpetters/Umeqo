#! /bin/bash
source $1
cd $2
python manage.py emit_notices 2>&1
echo "`date`: EMIT NOTICES SUCCESSFUL"
