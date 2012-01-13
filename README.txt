Version 0.1.49

Umeqo - an innovative recruiting resource for students and employers to discover one another.


INSTALLATION

Install virtualenv
1. Create a python virtual environment using virtualenv named UMEQO by running “virtualenv --no-site-packages UMEQO”
2. For convenience, create aliases such as the following in .bash_profile "alias ud='cd '" and "alias us='source /bin/activate'". This way you can just run “ud” “us” and be in the project root ready to go.
3. Once you have the environment activated (by running “us”), run "pip install –r requirements.txt" from the project root. You will probably get compilation errors. Let me know if you do.
4. Create a copy of settings_local_template.py in the project root and name it settings_local.py.
5. Open settings_local.py and add a tuple (“Your name”, “your email”) to ADMINS.
6. Create a “media” folder in the project root. Create a “ckeditor” folder inside of that folder.
7. Install java if you don’t have it.
8. Add two more aliases – "alias dap='cd /apache-solr-1.4.1’", "alias sap='java -jar start.jar'"
9. Run “dap” followed by “sap” in a separate terminal (to start the search engine)
10. Run “fab create_database”, followed by “fab load_local_data”
11. Run “python manage.py runcserver”
12. Go to localhost:8000. You’re set!


TYPICAL WORKFLOW

1. Open four terminals.

In the first one run -
us
ud
dap
sap

In the second one run -
us
ud
python manage.py runcserver

In the third one run -
us
ud
memcached

leave fourth for making commits.


2. Run "git branch" and make sure you are on the dev branch. If there is no dev branch or you are not on it, run "git checkout dev"
