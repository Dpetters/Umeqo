from haystack import indexes, site
from student.models import Student

class StudentIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(use_template=True, document=True)
    content_auto = indexes.EdgeNgramField(use_template = True)
    
    obj_id = indexes.IntegerField(model_attr="id")
    
    gpa = indexes.FloatField(model_attr="gpa", null=True)    
    sat_t = indexes.IntegerField(model_attr="sat_t", null=True)
    sat_m = indexes.IntegerField(model_attr="sat_m", null=True)
    sat_v = indexes.IntegerField(model_attr="sat_v", null=True)
    sat_w = indexes.IntegerField(model_attr="sat_w", null=True)
    act = indexes.IntegerField(model_attr="act", null=True)

    school_year = indexes.CharField(model_attr="school_year__id", null=True)
    graduation_year = indexes.CharField(model_attr="graduation_year__id", null=True)
    first_major = indexes.CharField(model_attr="first_major__id", null=True)
    second_major = indexes.CharField(model_attr="second_major__id", null=True)
    
    looking_for = indexes.MultiValueField() 
    campus_involvement = indexes.MultiValueField()
    languages = indexes.MultiValueField()
    countries_of_citizenship = indexes.MultiValueField()
    previous_employers = indexes.MultiValueField()
    industries_of_interest = indexes.MultiValueField()
    
    older_than_21 = indexes.BooleanField(model_attr="older_than_21")
    
    last_updated = indexes.DateTimeField(model_attr='last_updated')
        

    def prepare_looking_for(self, obj):
        return [employment_type.id for employment_type in obj.looking_for.all()]
    
    def prepare_campus_involvement(self, obj):
        return [campus_org.id for campus_org in obj.campus_involvement.all()]
    
    def prepare_languages(self, obj):
        return [language.id for language in obj.languages.all()]
    
    def prepare_countries_of_citizenship(self, obj):
        return [country.iso for country in obj.countries_of_citizenship.all()]
    
    def prepare_previous_employers(self, obj):
        return [employer.id for employer in obj.previous_employers.all()]
    
    def prepare_industries_of_interest(self, obj):
        return [industry.id for industry in obj.industries_of_interest.all()]
    
    def prepare_older_than_21(self, obj):
        return obj.older_than_21=="Y"
        
site.register(Student, StudentIndex)