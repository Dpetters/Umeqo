#! /bin/bash
source $1
cd $2
echo "`date`: ZIPPING ALL RESUMES"
python manage.py zip_resumes 2>&1