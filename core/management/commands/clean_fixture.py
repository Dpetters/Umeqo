import json

from django.core.management.base import CommandError, LabelCommand

class Command(LabelCommand):
    args = '<appname.model.field>'
    help = ("Temporary work-around for django ticket #9279. Deleted model fields that are present \
             in fixtures break loaddata. Use this script to delete these fields from the global \
             and the app-specific initial_data fixture.")

    def handle_label(self, label, **options):
        try:
            appname, model, field = map(str.lower, label.split("."))
        except ValueError:
            raise CommandError("Please provide a field label in the form of <appname.model.field>.\
            \nYou provided: %s" % (label))
        
        # Check global initial_data fixture
        filepath = "initial_data.json"
        try:
            f = file(filepath, "rb")
        except IOError:
            print "Warning: we couldn't find a global initial_data fixture"
        else:
            try:
                json_data = json.load(f)
                f.close()
            except ValueError:
                print "Warning: the global initial_data fixture had invalid json"
            else:
                num_removed = remove_unwanted_field(json_data, appname, model, field)
                if num_removed:
                    f = file(filepath, "rb")
                    json.dump(json_data, f, indent=1)
                    print "Successfully parsed the global initial_data fixture and removed"
                    print "%d instances of the field." % num_removed
                else:
                    print "Successfully parsed the global initial_data fixture but didn't find"
                    print "any instances of the field."

        # Check app-specific initial_data file
        filepath = "%s/fixtures/initial_data.json" % appname
        try:
            f = file(filepath, "rb")
        except IOError:
            print "Warning: we couldn't find an initial_data file for the app %s" % (appname)
            print "We looked in '%s'" % filepath 
        else:
            try:
                json_data = json.load(f)
                f.close()
            except ValueError:
                print "Warning: the initial_data file for the app %s contained invalid json!" \
                % (appname)
            else:
                num_removed = remove_unwanted_field(json_data, appname, model, field)
                if num_removed:
                    f = file(filepath, "wb")
                    json.dump(json_data, f, indent=1)
                    print "Successfully parsed the initial_data fixture for the app"
                    print "'%s' and removed %d instances of the field." % (appname, num_removed)
                else:
                    print "Successfully parsed the initial_data fixture for the app"
                    print "'%s' but didn't find any instances of the field." % (appname)

def remove_unwanted_field(json_data, appname, model, field):
    num = 0
    for instance in json_data:
        label = instance.get("model", None)
        if label and label=="%s.%s" %(appname, model):
            fields = instance.get("fields") 
            if fields.has_key(field):
                num += 1
                fields.pop(field)
    return num