Version 2.0.0

*[Umeqo](https://www.umeqo.com) - a new faster and smarter way for recruiters to find potential student candidates.*

## WARNINGS

1. NEVER execute *python manage.py migrate* without the *--no-initial-data* flag on production. This will load in the existing fixtures (last dump of prod data) and has the potential of overwriting the latest production data.

## INSTALLATION

1. Install python 2.7.
2. Install virtualenv by running "pip install virtualenv". If you don't have pip install it by running "easy_install pip". If you don't have easy_install, google "python setuptools" and install that to get it.
3. Create whatever name directory you want to work in ("workstation" or "dev"), cd into it, and run "git clone git@github.com:Dpetters/Umeqo.git".
4. Create a python virtual environment named UMEQO somewhere using virtualenv by running `virtualenv --no-site-packages UMEQO`.
5. Execute `pip install -r requirements.txt` from the project root. You might get compilation errors. If you do, you're likely just missing some dev package. Google to find a fix.
6. Create a copy of *settings_local_template.py* in the project root and name it *settings_local.py*.
7. Open *settings_local.py* and add a tuple (*Your name*, *your email*) to the ADMINS variable.
8. Create a folder named *media* in the project root. Create a folder named *ckeditor* inside of that folder.
9. Install java if you don't have it.
10. In the project root, execute `fab create_database`, followed by `fab load_local_data`.
11. From the project root, run `python manage.py clear_prod_stripe_ids`. We don't want to use prod employer stripe ids locally and there is no way to keep them from getting committed atm.
12. From the project root, execute `python manage.py runcserver`. You should get no errors.
13. Go to *localhost:8000* in your browser. The site landing page should load without any errors.

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

## MANAGEMENT COMMANDS

These are custom commands that can be run using `python manage.py <command-name>` from the project root.

`clear_stripe_test_customers` - clears all test mode customers from the Umeqo stripe account.

`clear_prod_stripe_ids` - clears all employer Stripe customer ids that got committed from prod.

## FABFILE COMMANDS

[http://docs.fabfile.org/en/1.5/](Tutorial)

`restart` - restarts apache. Can be run on staging prod or demo. Needs to be called whenever python code is updated and is thus called by `update`.

`restart_all` - restarts nginx and apache. Can be run on raging prod or demo. Ty

`migrate` - runs all available migrations for all apps. Is called by `update`.

`create_database` - deletes existing database, creates a new one, runs migrations, and loads in production data. Can only be called locally and on staging.

`schemamigrate` - runs through all the apps and checks for schema changes. Creates migrations for any new ones.

## PRODUCTION LOGS

We ideally want to set up something that monitors all the logs below and lets us know of any issues. Sentry only reports part of `/var/www/umeqo/logs/umeqo.log`.

`/var/log/umeqo_cron.log` - all cronjobs log to here.
`/var/log/nginx/umeqo.access.log` - nginx logs all requests to here.
`/var/log/nginx/error.log` - nginx logs all errors here.
`/var/log/apache2/access.log` - apache logs all requests to here.
`/var/log/apache2/error.log` - apache logs all errors to here.
`/var/www/umeqo/logs/solr-reboots.log` - is incorrectly named (should just be solr.log). The solr process logs to here. If search queries are failing, this is the first place to check.
`/var/www/umeqo/logs/umeqo.log` - everything that you see in sentry + more gets logged to here.
