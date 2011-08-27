#! /bin/bash
source $1
cd $2
echo "`date`: EMITTING NOTICES"
python manage.py emit_notices 2>&1
