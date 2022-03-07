from django_filters
from .models import *
# SponsorsData, purposeData

# Sponsor Filters
class ImsFilter(django_filters.FilterSet):
    class Meta:
        model = imsData
        fields = '__all__'