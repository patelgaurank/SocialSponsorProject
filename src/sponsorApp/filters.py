import django_filters
from .models import *
# SponsorsData, purposeData

# Sponsor Filters
class SponsorFilter(django_filters.FilterSet):
    class Meta:
        lst=[]
        model = SponsorsData
        for x in SponsorsData._meta.fields:
            if x.name != 'currentTimeStamp':
                lst.append(x.name)
        fields = lst
        wLst = ''
        
        fields = '__all__'

#purpose filters
class PurposeFilter(django_filters.FilterSet):
    class Meta:
        lst = []
        model = purposeData
        for x in purposeData._meta.fields:
            if x.name != 'currentTimeStamp':
                lst.append(x.name)
        fields = lst

        fields = '__all__'