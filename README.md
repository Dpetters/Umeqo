Version 2.0.0

*[Umeqo](https://www.umeqo.com) - a new faster and smarter way for recruiters to find potential student candidates.*

## WARNINGS

1. NEVER execute *python manage.py migrate* without the *--no-initial-data* flag on production. This will load in the existing fixtures (last dump of prod data) and has the potential of overwriting the latest production data.

## INSTALLATION

1. Create a python virtual environment named UMEQO somewhere using virtualenv by running `virtualenv --no-site-packages UMEQO`.
2. Execute `pip install -r requirements.txt` from the project root. You might get compilation errors. If you do, you're likely just missing some dev package. Google to find a fix.
3. Create a copy of *settings_local_template.py* in the project root and name it *settings_local.py*.
4. Open *settings_local.py* and add a tuple (*Your name*, *your email*) to the ADMINS variable.
5. Create a folder named *media* in the project root. Create a folder named *ckeditor* inside of that folder.
6. Install java if you don't have it.
7. In the project root, execute `fab create_database`, followed by `fab load_local_data`.
8. From the project root, execute `python manage.py runcserver`. You should get no errors.
9. Go to *localhost:8000* in your browser. The site landing page should load without any errors.

## WORKFLOW

###This workflow assumes you completed everything in the installation section.

1. Open three terminals.
2. In the first one run the search engine, Apache Solr, by executing `java -jar apache-solr-*/example/start.jar` from the project root.
3. In the second run the local server by executing `python manage.py runcserver`. You will use this to test whatever changes you make.
4. In the third run `git branch` and make sure you are on the dev branch. If there is no dev branch or you are not on it, run `git checkout dev`.
5. Make whatever changes you need to in this third terminal (or any other that you want).
6. Execute `git add <files to add>` to stage the files you changed.
7. Execute `git commit -m <commit message>` to commit your changes.
8. Execute `git push origin dev` to push the changes to staging.
9. Execute `fab staging update` locally to update staging.
10. Test the changes on staging.
11. If everything works as expected, execute `git checkout master` followed by `git merge dev` to merge your changes to the master branch.
12. Execute `git push origin master` to push your changes to master.
13. Run `fab prod update` locally to update prod.

## FABFILE COMMANDS

*Coming Soon*
