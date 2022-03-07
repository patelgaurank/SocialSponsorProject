from django import forms
from django.forms import Textarea
from .models import imsData
from datetime import datetime as dt
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

# Assign date input type
class DateInput(forms.DateInput):
    input_type = 'date'
    
#Create a form for sponsor
class imsForm(forms.ModelForm):
    currentDt = dt.strptime(str(dt.today()).split(' ')[0], '%Y-%m-%d').strftime('%m/%d/%Y')
    #sponsorshipDate = forms.DateField(widget=DateInput, initial=currentDt)
    img = forms.ImageField(required=False)
    class Meta:
        lst = []
        model = imsData
        # Remove field from the form
        #exclude = ['Country','City', 'State']
        for x in imsData._meta.fields:
            if x.name != 'currentTimeStamp' and x.name != 'UpdatedDate':
                lst.append(x.name)
        fields = lst
        wLst = ''
        #widget = {
        #    fields: forms.TextInput(attrs={'class': 'gp-input gp-border'}),
        #}
    def __init__(self, *args, **kwargs):
        super(imsForm, self).__init__(*args, **kwargs)
        currentDt = dt.strptime(str(dt.today()).split(' ')[0], '%Y-%m-%d').strftime('%m/%d/%Y')    
        for field in self.fields:
            print(self.fields[field].widget.attrs)
            #if field=='Gender':
            #    clsStr='gp-radio gp-boarder'
            #    typStr='radio'
            #else:
            if field != 'MiddleName':
                self.fields[field].required = True
            clsStr='gp-input gp-boarder imsFormInput'
            # if field=='img':
            #     clsStr = clsStr + ' gp-hide'
                #styStr = 'display: none;'
            
            styStr = 'text-transform: capitalize;'
            typStr='text'
            plcStr=field   
            self.fields[field].widget.attrs.update({'class': clsStr, 'type': typStr, 'placeholder':plcStr, 'style':styStr})            
    
    # def clean(self, *args, **kwargs):
    #     for field in self.fields:
    #         self.fields[field] = self.fields[field].capitalize()

#Update sponsor
class UpdateImsForm(forms.ModelForm):
    currentDt = dt.strptime(str(dt.today()).split(' ')[0], '%Y-%m-%d').strftime('%m/%d/%Y')    
    #sponsorshipDate = forms.DateField(widget=DateInput, initial=currentDt)
    img = forms.ImageField(required=False)
    class Meta:
        lst = []
        model = imsData
        # Remove field from the form
        #exclude = ['Country','City', 'State']
        for x in imsData._meta.fields:
            if x.name != 'currentTimeStamp' and x.name != 'UpdatedDate':
                lst.append(x.name)
        fields = lst
        wLst = ''
        #widget = {
        #    fields: forms.TextInput(attrs={'class': 'gp-input gp-border'}),
        #}
    def __init__(self, *args, **kwargs):
        super(UpdateImsForm, self).__init__(*args, **kwargs)
        currentDt = dt.strptime(str(dt.today()).split(' ')[0], '%Y-%m-%d').strftime('%m/%d/%Y')    
        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = True
            #if field=='Gender':
            #    clsStr='gp-radio gp-boarder'
            #    typStr='radio'
            #else:
            #self.fields[field].required = True
            clsStr='gp-input gp-boarder imsFormInput'
            # if field=='img':
            #     clsStr = clsStr + ' gp-hide'
                #styStr = 'display: none;'

            styStr = 'text-transform: capitalize;'
            typStr='text'
            plcStr=field   
            self.fields[field].widget.attrs.update({'class': clsStr, 'type': typStr, 'placeholder':plcStr, 'style':styStr})

    # def clean(self, *args, **kwargs):
    #     for field in self.fields:
    #         self.fields[field] = self.fields[field].capitalize()
