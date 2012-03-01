Version 0.1.51

Umeqo - an innovative recruiting resource for students and employers to discover one another.


INSTALLATION

IMPORTANT: If you are setting this up on windows, read the WINDOWS INSTALLATION PREP section below

1. Create a python virtual environment using virtualenv named UMEQO by running “virtualenv --no-site-packages UMEQO”
2. For convenience, create aliases such as the following in .bash_profile "alias ud='cd $UMEQO_HOME'" and "alias us='source $UMEQO_VIRTUAL_ENV_HOME/bin/activate'". This way you can just run “ud” “us” and be in the project root ready to go.
3. Once you have the environment activated (by running “us”), run "pip install –r requirements.txt" from the project root. You will probably get compilation errors. Let me know if you do.
4. Create a copy of settings_local_template.py in the project root and name it settings_local.py.
5. Open settings_local.py and add a tuple (“Your name”, “your email”) to ADMINS.
6. Create a “media” folder in the project root. Create a “ckeditor” folder inside of that folder.
7. Install java if you don’t have it.
8. Add two more aliases – "alias dap='cd $UMEQO_HOME/apache-solr-3.5.0’", "alias sap='java -jar start.jar'"
9. Run “dap” followed by “sap” in a separate terminal (to start the search engine)
10. Run “fab create_database”, followed by “fab load_local_data”
11. Run “python manage.py runcserver”
12. Go to localhost:8000. You’re set!


WINDOWS INSTALLATION PREP

1. If you do not have git installed, then install msysgit and add its bin as well as the mingw's bin folders to the path. Create HOME environment variable pointing to home directory.
2. Install setuptools
3. Install python-ldap and winpy32 from http://www.lfd.uci.edu/~gohlke/pythonlibs/
4. Install Visual Studio c++ 2008 Express


TYPICAL WORKFLOW

IMPORTANT: 
1. Open four terminals.
In the first one run - "us", "ud", "dap", "sap"
In the second one run - "us", "ud", "python manage.py runcserver"
In the third one run - "us", "ud", "memcached"
Leave fourth for making commits.
2. Run "git branch" and make sure you are on the dev branch. If there is no dev branch or you are not on it, run "git checkout dev"/
3. Make whatever changes you need to.
4. Run "git add -A" or "git add <files to add>" to stage the files you changed.
5. Run "git commit -m '<commit message>'" to commit your changes.
6. Run "git push origin dev" to push the changes to staging.
7. Run "fab staging update" locally to update staging.
8. Test the changes on staging.
9. Run "git checkout master" followed by "git merge dev" to merge your changes to the master branch.
10. Run "git push origin master" to push your changes to master.
11. Run "fab prod update" locally to update prod.


EXPLANATION OF FAB COMMANDS
