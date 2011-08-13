#! /bin/bash
source $1
cd $2
python manage.py emit_notices
