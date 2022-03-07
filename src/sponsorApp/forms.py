from django import forms
from django.forms import Textarea
from .models import *
# SponsorsData, purposeData
from datetime import datetime as dt

# Assign date input type
class DateInput(forms.DateInput):
    input_type = 'date'

#Create a form for sponsor
class SponsorForm(forms.ModelForm):
    currentDt = dt.strptime(str(dt.today()).split(' ')[0], '%Y-%m-%d')
    sponsorshipDate = forms.DateField(widget=DateInput, initial=currentDt)
    Memo = forms.CharField(max_length=150,widget=forms.Textarea(),help_text='Enter Memo/Announce Note.')
    class Meta:
        lst = []
        model = SponsorsData
        # Remove field from the form
        #exclude = ['Country','City', 'State']
        for x in SponsorsData._meta.fields:
            if x.name != 'currentTimeStamp' and x.name != 'UpdatedDate':
                lst.append(x.name)
        fields = lst
        wLst = ''
        #widget = {
        #    fields: forms.TextInput(attrs={'class': 'gp-input gp-border'}),
        #}
    def __init__(self, *args, **kwargs):
        super(SponsorForm, self).__init__(*args, **kwargs)
        currentDt = dt.strptime(str(dt.today()).split(' ')[0], '%Y-%m-%d')
        for field in self.fields:
            #if field=='Gender':
            #    clsStr='gp-radio gp-boarder'
            #    typStr='radio'
            #else:
            if field != 'MiddleName':
                self.fields[field].required = True
            clsStr='gp-input gp-boarder spFormInput'
            typStr='text'
            plcStr=field   
            if field=='sponsorshipDate':
                self.fields[field].initial=currentDt
            self.fields[field].widget.attrs.update({'class': clsStr, 'type': typStr, 'placeholder':plcStr, 'style':'text-transform: capitalize'})
    
    # def clean(self, *args, **kwargs):
    #     for field in self.fields:
    #         self.fields[field] = self.fields[field].capitalize()

#Update sponsor
class UpdateSponsorForm(forms.ModelForm):
    currentDt = dt.strptime(str(dt.today()).split(' ')[0], '%Y-%m-%d').strftime('%m/%d/%Y')
    sponsorshipDate = forms.DateField(widget=DateInput, initial=currentDt)
    Memo = forms.CharField(max_length=150,widget=forms.Textarea(),help_text='Enter Memo/Announce Note.')
    class Meta:
        lst = []
        model = SponsorsData
        # Remove field from the form
        #exclude = ['Country','City', 'State']
        for x in SponsorsData._meta.fields:
            if x.name != 'currentTimeStamp' and x.name != 'UpdatedDate':
                lst.append(x.name)
        fields = lst
        wLst = ''
        #widget = {
        #    fields: forms.TextInput(attrs={'class': 'gp-input gp-border'}),
        #}
    def __init__(self, *args, **kwargs):
        super(UpdateSponsorForm, self).__init__(*args, **kwargs)
        currentDt = dt.strptime(str(dt.today()).split(' ')[0], '%Y-%m-%d').strftime('%m/%d/%Y')    
        for field in self.fields:
            #if field=='Gender':
            #    clsStr='gp-radio gp-boarder'
            #    typStr='radio'
            #else:
            #self.fields[field].required = True
            clsStr='gp-input gp-boarder spFormInput'
            typStr='text'
            plcStr=field   
            if field=='sponsorshipDate':
                self.fields[field].initial=currentDt
            self.fields[field].widget.attrs.update({'class': clsStr, 'type': typStr, 'placeholder':plcStr})

    # def clean(self, *args, **kwargs):
    #     for field in self.fields:
    #         self.fields[field] = self.fields[field].capitalize()

#Create a form for purpose data
class purposeForm(forms.ModelForm):
    # currentDt = dt.strptime(str(dt.today()).split(' ')[0], '%Y-%m-%d')
    # sponsorshipDate = forms.DateField(widget=DateInput, initial=currentDt)
    # Memo = forms.CharField(max_length=150,widget=forms.Textarea(),help_text='Enter Memo/Announce Note.')
    class Meta:
        lst = []
        model = purposeData
        for x in purposeData._meta.fields:
            if x.name != 'currentTimeStamp' and x.name != 'UpdatedDate':
                lst.append(x.name)
        fields = lst
        wLst = ''
        #widget = {
        #    fields: forms.TextInput(attrs={'class': 'gp-input gp-border'}),
        #}
    def __init__(self, *args, **kwargs):
        super(purposeForm, self).__init__(*args, **kwargs)
        currentDt = dt.strptime(str(dt.today()).split(' ')[0], '%Y-%m-%d')
        for field in self.fields:
            clsStr='gp-input gp-boarder spFormInput'
            typStr='text'
            plcStr=field
            self.fields[field].widget.attrs.update({'class': clsStr, 'type': typStr, 'placeholder':plcStr, 'style':'text-transform: capitalize'})
    
    # def clean(self, *args, **kwargs):
    #     for field in self.fields:
    #         self.fields[field] = self.fields[field].capitalize()