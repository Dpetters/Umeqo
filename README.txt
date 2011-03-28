###############
##-SBConnect-##
###############


--Initial Content--

The "initial_content" folder in this project holds the initial content for the site, 
It is there so that if you have to deleted the database file, you won't need to manually 
add all the data back in again. Instead just run the "setup_local_database.py" script.

Couple things to note:
-All the actual info should be put into contents.json files.
-Do not rename the "content" folder, or any of the folders immediately inside of it.
-Two types of content, Courses and Campus Orgs, should be put into individual folders.
 This is just what I decided to do because they will eventually have images too, and
 I didn't want one big folder full of images and .json files.
-If you change the name of a CampusOrg or Course, change it in both contents.json and in the folder name.
-If you're gonna add a 240 x 160 image, name it image.jpg and put it in the same folder 
 as the contents.json file. When setup_local_database.py is run, this image will be saved
 to the submitted_images directory in the media folder.