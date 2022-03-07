from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from imsApp.models import imsData
import string
from django.core.mail import send_mail
import json
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime as dt
from django.views.generic import View
from django.utils.decorators import method_decorator as mDecorator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from imsApp.forms import UpdateImsForm as imsForm
from datetime import datetime as dt
import random as rd
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def ims_data_table_view(request, *args, **kwargs):
     currentDt = dt.strptime(str(dt.today()).split(' ')[0], '%Y-%m-%d').strftime('%m/%d/%Y')     
     id = request.POST.get('id')

     if id:
          id = id[:-4]
          id = id[-len(str(id).replace(str(id)[:3], "")):]
          print(imsData.objects.get(pk=id).img)

     if request.is_ajax():
          if request.method == "POST":
               if request.POST.get('id'):
                    rcdId = id
                    obj = imsData.objects.filter(id=int(rcdId)).only()
                    cnt = serializers.serialize("json", obj,
                    fields=("MemberID","FirstName","MiddleName","LastName","SpouseFirstName",
                    "AddressLine1","AddressLine2","City","State","Zipcode","SatsangCategory",
                    "Mandal","Relation","SatsangReference","NativePlace","NativeCountry","ZoneName",
                    "OtherAppPersonID","PrimaryCellPhone","PrimaryHomePhone","PrimaryEmail","Gender",
                    "Karyakar","Volunteer","GraduationYear","Remarks","Language", "EnteredBy", "img")
                    )
                    obj_list = json.loads(cnt)
                    json_data = json.dumps(obj_list)
                    return HttpResponse(json_data, content_type='application/json')
                    #return JsonResponse(json.loads(cnt), safe=False)
               
               if request.POST.get('itemData'):
                    if request.POST.get('itemData') == 'imsContainerLarge':
                         lst = ['MemberID', 'Name','Phone', 'City, State']
                         y = 0
                         fldFinal = '<thead><tr class="gp-red gp-border" id="tableHeader">'
                         for x in lst:
                              y += 1
                              fld = '<th class="gp-button gp-hover-grayscale gp-medium" style="position: sticky; top: 0;">' + x
                              fld = fld + '<i onclick="sortTable(' + str(y) + ')" class="fa fa-sort gp-right gp-hide-small gp-hide-medium"></i></th>'
                              fldFinal = fldFinal + fld
                    
                         fldFinal = fldFinal + '</tr></thead>'
                              #      {% autoescape off %}{{ fldObjLargeScreen }}{% endautoescape %}
                              # </tr>
                              # </thead>

                         # Find all records and create table row for html
                         IMSData = imsData.objects.all().order_by('MemberID').reverse()
                         rwVlFinal = ''

                         for rw in IMSData:
                              fd = str(rd.randint(100, 1000))
                              sd = str(rd.randint(1000, 10000))
                              #updDate = dt.strptime(str(rw.UpdatedDate).split(' ')[0], '%Y-%m-%d').strftime('%m/%d/%y')
                              rwVl = '<tr class="tblRwId" href="?#'+rw.FirstName + rw.LastName +'" id='+fd+str(rw.id)+sd+' data-update-ref="/imsdata/">'
                              rwVl=rwVl + '<td>'+str(rw.MemberID)+'</td>'
                              rwVl=rwVl + '<td>'+ rw.FirstName + ' ' + rw.LastName+'</td>'
                              rwVl=rwVl + '<td>'+ (rw.PrimaryCellPhone if rw.PrimaryCellPhone is not None else rw.PrimaryHomePhone) +'</td>'
                              rwVl=rwVl + '<td>'+(rw.City if rw.City is not None else '')+ ', ' +(rw.State if rw.State is not None else '')+'</td>'
                              rwVl=rwVl + '</tr>'
                              rwVlFinal = rwVlFinal + rwVl

                         rwVlFinal = fldFinal + '<tbody class="gp-medium" id="tableBody">'+rwVlFinal+'</tbody>'

                         context = {"fldObjLargeScreen": fldFinal, "rcdObjLargeScreen": rwVlFinal}
                    
                    if request.POST.get('itemData') == 'imsContainerSmall':
                         y = 0
                         lst2 = ['Name','City, State','Phone'] 
                         fldFinal = '<thead><tr class="gp-red gp-border" id="tableHeader">'
                         for x in lst2:
                              y += 1
                              fld = '<th class="gp-button gp-hover-grayscale gp-medium" style="position: sticky; top: 0;">' + x
                              fld = fld + '<i onclick="sortTable(' + str(y) + ')" class="fa fa-sort gp-right gp-hide-small gp-hide-medium"></i></th>'
                              fldFinal = fldFinal + fld

                         fldFinal = fldFinal + '</tr></thead>'
                         # Find all records and create table row for html
                         IMSData = imsData.objects.all().order_by('MemberID').reverse()
                         rwVlFinal = ''
                         imsListHTML = ''
                         rwVlFinal2 = ''
                         #onclick="rwClick('+ str(rw.id) +')"
                         # data-update-ref="//sponsordata//sponsor_data_form//"
                         for rw in IMSData:
                              fd = str(rd.randint(100, 1000))
                              sd = str(rd.randint(1000, 10000))
                              imsListHTML = '<tr class="tblRwId" href="?#'+rw.FirstName + rw.LastName +'" id='+fd+str(rw.id)+sd+' data-update-ref="/imsdata/">'
                              imsListHTML = imsListHTML +'<td>'+ rw.FirstName + ' ' + rw.LastName
                              imsListHTML = imsListHTML +'</td><td>'+(rw.City if rw.City is not None else '')+ ', ' +(rw.State if rw.State is not None else '')
                              imsListHTML = imsListHTML +'</td><td>'+ (rw.PrimaryCellPhone if rw.PrimaryCellPhone is not None else rw.PrimaryHomePhone) +'</td></tr>'
                              rwVlFinal = rwVlFinal + imsListHTML
                         rwVlFinal = '<tbody>' + rwVlFinal + '</tbody>'
                         rwVlFinal = fldFinal + rwVlFinal
                    return HttpResponse(rwVlFinal)


     IMSForm = imsForm()
     if request.method =="POST":
          fieldsCapFirst=['FirstName','MiddleName','LastName','SpouseFirstName','SatsangCategory','SatsangReference'
          ,'Mandal','Relation','NativePlace','ZoneName','Gender','Karyakar','Volunteer','Language','Profession'
          ,'PrimaryEmail','Country','AddressLine1','AddressLine2','City','State','Remarks']
          context = {} 
          if id:
               context = {}
               rcdId = get_object_or_404(imsData, pk=id)
               IMSForm = imsForm(request.POST or None, request.FILES or None, instance=rcdId)
               #print(IMSForm)
               if IMSForm.is_valid():
                    print(IMSForm.img)
                    IMSForm = IMSForm.save(commit=False)
                    IMSForm.EnteredBy = '%s %s'%(request.user.first_name, request.user.last_name)
                    IMSForm.UpdateDate = currentDt
                    IMSForm.FirstName = (IMSForm.FirstName).title()
                    if IMSForm.MiddleName:
                         IMSForm.MiddleName = (IMSForm.MiddleName).title()
                    IMSForm.LastName = (IMSForm.LastName).title()
                    IMSForm.user = request.user
                    IMSForm.save()
                    return redirect('/ims/imsdata/')
               context = {"frmObj": IMSForm}
               return render(request, "ImsData/imsForm.html", context)

          IMSForm = imsForm(request.POST, instance=imsData())
          if IMSForm.is_valid():
               IMSForm = IMSForm.save(commit=False)
               IMSForm.EnteredBy = '%s %s'%(request.user.first_name, request.user.last_name)               
               IMSForm.UpdateDate = currentDt
               IMSForm.FirstName = (IMSForm.FirstName).title()
               if IMSForm.MiddleName:
                    IMSForm.MiddleName = (IMSForm.MiddleName).title()
               IMSForm.LastName = (IMSForm.LastName).title()
               IMSForm.user = request.user
               IMSForm.save()
               return HttpResponseRedirect('/ims/imsdata/')
          context = {"frmObj": IMSForm}
          return render(request, "ImsData/imsForm.html", context)
     elif request.method == "GET":            
          if id:
               rcdId = get_object_or_404(SponsorsData, id=id)
               #Find requested data
               IMSForm = imsForm(instance=rcdId)     
               context = {"frmObj": IMSForm}
               tem = "ImsData/imsForm.html"
          else:
               tem = "ImsData/imsdata.html"
               ImsForm = imsForm(request.POST)
               context = {"frmObj": ImsForm} 
               
          return render(request, tem, context)


     #context = {"objDict": 'xyz'}
     #return render(request, "ImsData/imsdata.html", context)

@login_required
def ims_form_view(request, *args, **kwargs):
     currentDt = dt.strptime(str(dt.today()).split(' ')[0], '%Y-%m-%d').strftime('%m/%d/%Y')     
     id = request.POST.get('id')

     if id:          
          id = id[:-4]
          id = id[-len(str(id).replace(str(id)[:3], "")):]
          print(imsData.objects.get(pk=id).img)

     if request.is_ajax():
          if request.method == "POST":
               if request.POST.get('id'):
                    rcdId = id
                    obj = imsData.objects.filter(id=int(rcdId)).only()
                    cnt = serializers.serialize("json", obj,
                    fields=("MemberID","FirstName","MiddleName","LastName","SpouseFirstName",
                    "AddressLine1","AddressLine2","City","State","Zipcode","SatsangCategory",
                    "Mandal","Relation","SatsangReference","NativePlace","NativeCountry","ZoneName",
                    "OtherAppPersonID","PrimaryCellPhone","PrimaryHomePhone","PrimaryEmail","Gender",
                    "Karyakar","Volunteer","GraduationYear","Remarks","Language", "EnteredBy", "img")
                    )
                    obj_list = json.loads(cnt)
                    json_data = json.dumps(obj_list)
                    return HttpResponse(json_data, content_type='application/json')
                    #return JsonResponse(json.loads(cnt), safe=False)

     IMSForm = imsForm()
     if request.method =="POST":
          fieldsCapFirst=['FirstName','MiddleName','LastName','SpouseFirstName','SatsangCategory','SatsangReference'
          ,'Mandal','Relation','NativePlace','ZoneName','Gender','Karyakar','Volunteer','Language','Profession'
          ,'PrimaryEmail','Country','AddressLine1','AddressLine2','City','State','Remarks']
          context = {} 
          if id:
               context = {}
               rcdId = get_object_or_404(imsData, pk=id)
               IMSForm = imsForm(request.POST or None, request.FILES or None, instance=rcdId)
               #print(IMSForm)
               if IMSForm.is_valid():
                    IMSForm = IMSForm.save(commit=False)
                    IMSForm.EnteredBy = '%s %s'%(request.user.first_name, request.user.last_name)
                    IMSForm.UpdateDate = currentDt
                    IMSForm.FirstName = (IMSForm.FirstName).title()
                    if IMSForm.MiddleName:
                         IMSForm.MiddleName = (IMSForm.MiddleName).title()
                    IMSForm.LastName = (IMSForm.LastName).title()
                    IMSForm.user = request.user
                    IMSForm.save()                    
                    return redirect('/ims/imsdata/')
               context = {"frmObj": IMSForm}
               return render(request, "ImsData/imsForm.html", context)

          IMSForm = imsForm(request.POST, instance=imsData())
          if IMSForm.is_valid():
               IMSForm = IMSForm.save(commit=False)
               IMSForm.EnteredBy = '%s %s'%(request.user.first_name, request.user.last_name)               
               IMSForm.UpdateDate = currentDt
               IMSForm.FirstName = (IMSForm.FirstName).title()
               if IMSForm.MiddleName:
                    IMSForm.MiddleName = (IMSForm.MiddleName).title()
               IMSForm.LastName = (IMSForm.LastName).title()
               IMSForm.user = request.user
               IMSForm.save()
               return HttpResponseRedirect('/ims/imsdata/')
          context = {"frmObj": IMSForm}
          return render(request, "ImsData/imsForm.html", context)
     elif request.method == "GET":            
          if id:
               rcdId = get_object_or_404(SponsorsData, id=id)
               #Find requested data
               IMSForm = imsForm(instance=rcdId)     
               context = {"frmObj": IMSForm}
               tem = "ImsData/imsForm.html"
          else:
               tem = "ImsData/imsForm.html"
               fldFinal = ''
               y = 0
               #fld = '<th class="gp-button gp-hover-grayscale gp-medium"> Name (First Middle Last)'
               #fld = fld + '<i onclick="sortTable(' + str(y) + ')" class="fa fa-sort gp-right gp-hide-small gp-hide-medium"></i></th>'
               #fldFinal = fldFinal + fld
               # Remove below header from the sponsor data         
               lst = ['MemberID', 'FirstName','LastName','PrimaryCellPhone', 'City','State'] 

               # Create a table header
               for x in imsData._meta.fields:
                    if x.name in lst:
                         # Find labels
                         lblName = imsData._meta.get_field(x.name).verbose_name
                         y += 1
                         fld = '<th class="gp-button gp-hover-grayscale gp-medium" style="position: sticky; top: 0;">' + lblName
                         fld = fld + '<i onclick="sortTable(' + str(y) + ')" class="fa fa-sort gp-right gp-hide-small gp-hide-medium"></i></th>'
                         fldFinal = fldFinal + fld

               # Find all records and create table row for html
               IMSData = imsData.objects.all().order_by('MemberID').reverse()
               rwVlFinal = ''; rwVlFinal2 = ''
               #onclick="rwClick('+ str(rw.id) +')" 
               # data-update-ref="//sponsordata//sponsor_data_form//"
               for rw in IMSData:
                    fd = str(rd.randint(100, 1000))
                    sd = str(rd.randint(1000, 10000))
                    #updDate = dt.strptime(str(rw.UpdatedDate).split(' ')[0], '%Y-%m-%d').strftime('%m/%d/%y')
                    rwVl = '<tr class="tblRwId" href="?#'+rw.FirstName + rw.LastName +'" id='+fd+str(rw.id)+sd+' data-update-ref="/imsdata/">'
                    rwVl=rwVl + '<td>'+str(rw.MemberID)+'</td>'
                    rwVl=rwVl + '<td>'+rw.FirstName +'</td><td>'+rw.LastName+'</td>'
                    rwVl=rwVl + '<td>'+ (rw.PrimaryCellPhone if rw.PrimaryCellPhone is not None else rw.PrimaryHomePhone) +'</td>'
                    rwVl=rwVl + '<td>'+(rw.City if rw.City is not None else '')+'</td><td>'+(rw.State if rw.State is not None else '')+'</td>'
                    rwVl=rwVl + '</tr>'
                    rwVlFinal = rwVlFinal + rwVl                    
                    # <td style="width: 2px;"><img src="/static/img/icons/Master/svg/Sponsor.svg" class="gp-left gp-circle gp-margin-right" style="width:25px"></td>
               ImsForm = imsForm(request.POST)
               context = {"frmObj": ImsForm}
               
          return render(request, tem, context)
