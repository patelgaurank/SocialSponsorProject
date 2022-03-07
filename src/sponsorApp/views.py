from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.forms.models import model_to_dict
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.utils.decorators import method_decorator as mDecorator
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.staticfiles.storage import staticfiles_storage
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Group
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime as dt
import requests as rqs
from geopy.geocoders import Nominatim
import random as rd
import platform
import json
import string
from .models import SponsorsData, LoggedUser, purposeData as pdM
from .models import Purpose as p, PurposeCode as pc, PurposeIndex as pi
from .models import State as st, City as ct, ZipCode as zc, Country as c
from imsApp.models import imsData
from .forms import *
# SponsorForm, UpdateSponsorForm, purposeForm
from .filters import *


# Sponsor Dashboard view
@login_required
def dashboard_view(request,*args, **kwargs):
     currentDt = dt.strptime(str(dt.today()).split(' ')[0], '%Y-%m-%d').strftime('%m/%d/%y')
     currentYr = '%s'%(str(dt.today()).split('-')[0])
     todaysSponsors = len(SponsorsData.objects.filter(sponsorshipDate=dt.today()))
     totalSponsors = len(SponsorsData.objects.filter(sponsorshipDate__year='%s'%(str(dt.today()).split('-')[0])))

     if request.is_ajax():
          if request.method == "POST":
               #rcdId = request.POST['id']
               if request.POST.get('locLatLag'):
                    #print(request.POST.get('locLatLag'))
                    geolocator = Nominatim(user_agent="SatsangApp")
                    location = geolocator.reverse(request.POST.get('locLatLag'))
                    rsDict = dict(locAddress=location.address.split(", ")[2:])
                    city = ''; state = ''
                    try:
                         city = rsDict['locAddress'][0]
                         state = rsDict['locAddress'][2]
                    except:
                         city = 'None'; state = 'None'
                         pass
                    rsDict = {'userCity': city, 'userState': state}
                    LoggedUser.objects.filter(username=request.user.username, loggedIn='Y', userAddr=str(request.META.get('REMOTE_ADDR'))).update(userCity=city)
                    LoggedUser.objects.filter(username=request.user.username, loggedIn='Y', userAddr=str(request.META.get('REMOTE_ADDR'))).update(userState=state)
                    return HttpResponse(json.dumps(rsDict),content_type="application/json")
                    #LoggedUser.objects.filter(username=str(user), loggedIn='Y', userAddr=str(request.META.get('REMOTE_ADDR'))).update(userLocDict=)
               elif request.POST.get('locAddress'):
                    locDict = request.POST.get('locAddress')
                    city = json.loads(locDict)['city']
                    state = json.loads(locDict)['region_code']
                    LoggedUser.objects.filter(username=request.user.username, loggedIn='Y', userAddr=str(request.META.get('REMOTE_ADDR'))).update(userCity=city)
                    LoggedUser.objects.filter(username=request.user.username, loggedIn='Y', userAddr=str(request.META.get('REMOTE_ADDR'))).update(userState=state)
                    rsDict = {'userCity': city, 'userState': state}
                    return HttpResponse(json.dumps(rsDict),content_type="application/json")


     # Find all records and create table row for html
     spData = SponsorsData.objects.all().order_by('sponsorshipDate').reverse()
     rwVlFinal = ''
     for rw in spData:
          spDate = dt.strptime(str(rw.sponsorshipDate), '%Y-%m-%d').strftime('%m/%d/%y')
          updDate = dt.strptime(str(rw.UpdatedDate).split(' ')[0], '%Y-%m-%d').strftime('%m/%d/%y')
          rwVl = '<tr id="'+str(rw.id)+'"><td>'+rw.FirstName +' '+rw.LastName+'</td>'
          rwVl=rwVl + '<td>'+(str(rw.City) if rw.City is not None else '')+'</td><td>'+(str(rw.State) if rw.State is not None else '')+'</td><td>'+(str(rw.Purpose) if rw.Purpose is not None else '')+'</td>'
          rwVl=rwVl + '<td>'+rw.Memo+'</td><td>'+rw.DisplayOnPPT+'</td><td>'+rw.Announce+'</td>'
          rwVl=rwVl + '<td>'+spDate+'</td><td>'+rw.EnteredBy+'</td><td>'+updDate+'</td>'
          rwVl=rwVl + '</tr>'
          rwVlFinal = rwVlFinal + rwVl

     listVl = "<li class='gp-display-container gp-left-align' id='id_'><span class='gp-transparent gp-display-right gp-text-red'>Online</span></li>"
     lstTimeStamp = dt.now()
     city = ''
     state = ''
     listVl1 = ''
     # User online
     if len(LoggedUser.objects.all())>0:
          luData = LoggedUser.objects.filter(loggedIn='Y')
          lastLoginCurrentUser = LoggedUser.objects.filter(username=request.user.username, loggedIn='N').order_by("-id")
          if len(lastLoginCurrentUser)>0:
               lastLoginCurrentUser = lastLoginCurrentUser[0]
               lstTimeStamp = lastLoginCurrentUser.currentTimeStamp
          idLoginUser = LoggedUser.objects.filter(username=request.user.username, loggedIn='Y').values('userAddr')
          city = LoggedUser.objects.filter(username=request.user.username, loggedIn='Y', userAddr=str(request.META.get('REMOTE_ADDR'))).values('userCity')[0]['userCity']
          state = LoggedUser.objects.filter(username=request.user.username, loggedIn='Y', userAddr=str(request.META.get('REMOTE_ADDR'))).values('userState')[0]['userState']
          for rw in luData:
               listVl = "<li class='gp-display-container gp-left-align' id='id_" + rw.username + "'>" + rw.username + "<span class='gp-transparent gp-display-right gp-text-red'>Online</span></li>"
               listVl1 = listVl1 + listVl

     # Find all records and create table row for html
     spData = SponsorsData.objects.filter(sponsorshipDate=dt.today()).order_by('UpdatedDate').reverse()[:10]
     rwVlFinal = ''
     #onclick="rwClick('+ str(rw.id) +')"
     # data-update-ref="//sponsordata//sponsor_data_form//"
     for rw in spData:
          fd = str(rd.randint(100, 1000))
          sd = str(rd.randint(1000, 10000))
          spListHTML = '<tr id='+fd+str(rw.id)+sd+'><td style="width: 2px;"><img src="/static/img/icons/Master/svg/Sponsor.svg" class="gp-left gp-circle gp-margin-right" style="width:25px"></td>'
          spListHTML = spListHTML + '<td>'+ rw.FirstName + ' ' + rw.LastName +'</td><td>'+ rw.City + ', ' + rw.State +'</td><td>'+ str(rw.sponsorshipDate) +'</td></tr>'
          rwVlFinal = rwVlFinal + spListHTML
     #style="font-size:1vw;"
     rwVlFinal = '<tbody id="dbSpTableBody">' + rwVlFinal + '</tbody>'

     context = {"tdSpObj": todaysSponsors, "ttSpObj": totalSponsors,
     "lstTimeStamp": lstTimeStamp,  "crtYrObj": currentYr,
     "crtDtObj": currentDt, "userList": listVl1, "CurrentSpData": rwVlFinal,
     "userCity": city, "userState": state}
     return render(request, "home/dashboard.html", context)

# Sposor data view
@login_required
def sponsorView(request, *args, **kwargs):
     currentDt = dt.strptime(str(dt.today()).split(' ')[0], '%Y-%m-%d').strftime('%m/%d/%Y')
     id = request.POST.get('id')
     if id:
          id = id[:-4]
          id = id[-len(str(id).replace(str(id)[:3], "")):]
     if request.is_ajax():
          if request.method == "POST":

               #rcdId = request.POST['id']
               if request.POST.get('id'):
                    rcdId = id
                    #rcdId = rcdId.split('m')[0].replace("d", "")
                    #obj = Profile.objects.get(id=int(rcdId))
                    obj = SponsorsData.objects.filter(id=int(rcdId)).only()
                    cnt = serializers.serialize("json", obj,
                    fields=('id', 'FirstName','MiddleName','LastName','MemberId','Gender','Purpose_Code','PurposeIndex', 'Country',
                    'City', 'State', 'Purpose', 'Memo', 'DisplayOnPPT', 'Announce', 'amountReceived', 'EnteredBy', 'sponsorshipDate', 'ZipCode')
                    )
                    obj_list = json.loads(cnt)
                    json_data = json.dumps(obj_list)
                    return HttpResponse(json_data, content_type='application/json')
                    #return JsonResponse(json.loads(cnt), safe=False)

               # Autocompalete list for Name
               if request.POST.get('lst'):
                    print(request.POST.get('lst'))
                    if request.POST.get('lst').split('-')[0][3:]=='FirstName':
                         fnList = list(imsData.objects.filter(
                              FirstName__startswith=request.POST.get('lst').split('-')[1]).values_list('FirstName', flat=True).distinct()[:10])
                    elif request.POST.get('lst').split('-')[0][3:]=='LastName':
                         fnList = list(imsData.objects.filter(
                              LastName__startswith=request.POST.get('lst').split('-')[1]).values_list('LastName', flat=True).distinct())
                    elif request.POST.get('lst').split('-')[0][3:]=='MiddleName':
                         fnList = list(imsData.objects.filter(
                              MiddleName__startswith=request.POST.get('lst').split('-')[1]).values_list('MiddleName', flat=True).distinct())
                    elif request.POST.get('lst').split('-')[0][3:]=='undefined':
                         fnList = ""
                    return HttpResponse(json.dumps(fnList))

               if request.POST.get('zipcode'):
                    zipcode_id = request.POST.get('zipcode')
                    #print(zipcode_id)
                    try:
                         ctId = zc.objects.order_by('ZipCode').filter(ZipCode=zipcode_id).values("City_id", "City")
                         ctNm = ct.objects.order_by('City').filter(id=ctId[0]['City']).values("City", "StateName", "county")
                         stNm = st.objects.order_by('StateName').filter(id=ctNm[0]['StateName']).values("StateAbbr", "CountryName")
                         cNm = c.objects.order_by('CountryName').filter(id=stNm[0]['CountryName']).values("CountryName")
                         rsDict = dict(id_Country=cNm[0]['CountryName'], id_State=stNm[0]['StateAbbr'], id_City=ctNm[0]['City'])
                    except Exception as inst:
                         rsDict = dict(id_Country='NA', id_State='NA', id_City='NA')
                    return HttpResponse(json.dumps(rsDict),content_type="application/json")

               # Auto populate list for Countyr
               if request.POST.get('country'):
                    country_id = request.POST.get('country')
                    obj = st.objects.order_by('StateName').filter(CountryName_id=country_id).values('id', 'StateName')
                    opt = '<option value="">-----------</option>'
                    for o in obj:
                         opt = opt+'<option value="%s">%s</option>'%(o['id'], o['StateName'])
                    return HttpResponse(opt)

               # Auto populate list for City
               if request.POST.get('city'):
                    state_id = request.POST.get('city')
                    obj = ct.objects.order_by('City').filter(StateName_id=state_id).values('id', 'City')
                    opt = '<option value="">-----------</option>'
                    for o in obj:
                         opt = opt+'<option value="%s">%s</option>'%(o['id'], o['City'])
                    return HttpResponse(opt)

               # Auto populate list for Purpose
               if request.POST.get('purpose'):
                    purposeList = []
                    purpose_id = request.POST.get('purpose')
                    pV = p.objects.order_by('Purpose').filter(id=purpose_id)
                    # obj = pc.objects.order_by('Purpose_Code').filter(purpose=pV[0]).values("Purpose_Code")
                    # purposeList.append(obj[0]['Purpose_Code'])
                    # obj = pc.objects.order_by('Purpose_Code').filter(purpose=pV[0]).values("purposeindex")
                    # purposeList.append(obj[0]['purposeindex'])
                    # print(obj[0]['purposeindex'])
                    obj = pdM.objects.filter(Purpose=pV[0])
                    # print(obj)
                    # purposeList.append(obj[0]['AnnounceAs'])
                    return HttpResponse(serializers.serialize('json', obj), content_type ="application/json")

               # Auto populate list for Purpose code and indes
               if request.POST.get('purpose2'):
                    purpose_id = request.POST.get('purpose2')
                    pV = p.objects.order_by('Purpose').filter(id=purpose_id)
                    obj = pc.objects.order_by('Purpose_Code').filter(purpose=pV[0]).values("purposeindex")
                    return HttpResponse(obj[0]['purposeindex'])

               if request.POST.get('itemData'):
                    if request.POST.get('itemData') == 'spContainerLarge':
                         fldFinal = ''
                         y = 0
                         fld = '<th class="gp-button gp-hover-grayscale gp-medium"> Name (First Middle Last)'
                         fld = fld + '<i onclick="sortTable(' + str(y) + ')" class="fa fa-sort gp-right gp-hide-small gp-hide-medium"></i></th>'
                         fldFinal = fldFinal + fld

                         lst = ['id', 'currentTimeStamp', 'FirstName','MiddleName',
                         'LastName','MemberId','Gender','Purpose_Code','PurposeIndex', 'Country', 'ZipCode', 'user']

                         # Create a table header
                         for x in SponsorsData._meta.fields:
                              if x.name not in lst:
                                   lblName = SponsorsData._meta.get_field(x.name).verbose_name
                                   y += 1
                                   fld = '<th class="gp-button gp-hover-grayscale gp-medium">' + lblName
                                   fld = fld + '<i onclick="sortTable(' + str(y) + ')" class="fa fa-sort gp-right gp-hide-small gp-hide-medium"></i></th>'
                                   fldFinal = fldFinal + fld
                         fldFinal='<thead><tr class="gp-red gp-border">'+fldFinal+'</tr></thead>'

                         # Find all records and create table row for html
                         spData = SponsorsData.objects.all().order_by('sponsorshipDate').reverse()
                         rwVlFinal = ''
                         rwVlFinal2 = ''
                         #onclick="rwClick('+ str(rw.id) +')"
                         # data-update-ref="//sponsordata//sponsor_data_form//"
                         for rw in spData:
                              fd = str(rd.randint(100, 1000))
                              sd = str(rd.randint(1000, 10000))
                              spDate = dt.strptime(str(rw.sponsorshipDate), '%Y-%m-%d').strftime('%m/%d/%y')
                              updDate = dt.strptime(str(rw.UpdatedDate).split(' ')[0], '%Y-%m-%d').strftime('%m/%d/%y')
                              rwVl = '<tr class="tblRwId" href="?#'+(rw.FirstName if rw.FirstName is not None else '') + (rw.LastName if rw.LastName is not None else '') +'" id='+fd+str(rw.id)+sd+' data-update-ref="/sponsordata/"><td>'+(rw.FirstName if rw.FirstName is not None else '') +' '+(rw.LastName if rw.LastName is not None else '')+'</td>'
                              rwVl=rwVl + '<td>'+(str(rw.City) if rw.City is not None else '')+'</td><td>'+(str(rw.State) if rw.State is not None else '')+'</td><td>'+(str(rw.Purpose) if rw.Purpose is not None else '')+'</td>'
                              rwVl=rwVl + '<td>'+rw.Memo+'</td><td>'+spDate+'</td><td>'+rw.DisplayOnPPT+'</td><td>'+rw.Announce+'</td>'
                              rwVl=rwVl + '<td>'+rw.amountReceived+'</td>'
                              rwVl=rwVl + '<td>'+rw.EnteredBy+'</td><td>'+updDate+'</td>'
                              rwVl=rwVl + '</tr>'
                              rwVlFinal = rwVlFinal + rwVl
                         #style="font-size:1vw;"
                         rwVlFinal = '<tbody id="dbSpTableBody1">' + rwVlFinal + '</tbody>'
                         rwVlFinal = fldFinal+rwVlFinal
                    if request.POST.get('itemData') == 'spContainerSmall':
                         # Find all records and create table row for html
                         spData = SponsorsData.objects.all().order_by('sponsorshipDate').reverse()
                         rwVlFinal = ''
                         rwVlFinal2 = ''
                         for rw in spData:
                              fd = str(rd.randint(100, 1000))
                              sd = str(rd.randint(1000, 10000))
                              spDate = dt.strptime(str(rw.sponsorshipDate), '%Y-%m-%d').strftime('%m/%d/%y')
                              updDate = dt.strptime(str(rw.UpdatedDate).split(' ')[0], '%Y-%m-%d').strftime('%m/%d/%y')
                              spListHTML = '<tr id='+fd+str(rw.id)+sd+'><td style="width: 2px;"><img src="/static/img/icons/Master/svg/Sponsor.svg" class="gp-left gp-circle gp-margin-right" style="width:25px"></td>'
                              spListHTML = spListHTML + '<td>'+ rw.FirstName + ' ' + rw.LastName +'</td><td>'+ rw.City + ', ' + rw.State +'</td><td>'+ str(rw.sponsorshipDate) +'</td></tr>'
                              rwVlFinal2 = rwVlFinal2 + spListHTML
                         #style="font-size:1vw;"
                         rwVlFinal = '<tbody id="dbSpTableBody1">' + rwVlFinal2 + '</tbody>'

                    return HttpResponse(rwVlFinal)

     sponsorForm = UpdateSponsorForm()
     if request.method =="POST":
          fieldsCapFirst=['FirstName','MiddleName','LastName','Memo']
          context = {}
          if id:
               context = {}
               rcdId = get_object_or_404(SponsorsData, pk=id)
               sponsorForm = UpdateSponsorForm(request.POST, instance=rcdId)
               if sponsorForm.is_valid():
                    sponsorForm = sponsorForm.save(commit=False)
                    sponsorForm.EnteredBy = '%s %s'%(request.user.first_name, request.user.last_name)
                    sponsorForm.UpdateDate = currentDt
                    sponsorForm.FirstName = (sponsorForm.FirstName).title()
                    if sponsorForm.MiddleName:
                         sponsorForm.MiddleName = (sponsorForm.MiddleName).title()
                    sponsorForm.LastName = (sponsorForm.LastName).title()
                    sponsorForm.Memo = (sponsorForm.Memo).title()
                    sponsorForm.user = request.user
                    sponsorForm.save()
                    return redirect('/sponsor/sponsordata/')
               context = {"frmObj": sponsorForm}
               return render(request, "SponsorsData/sponsorForm.html", context)

          sponsorForm = UpdateSponsorForm(request.POST, instance=UpdateSponsorForm())
          if sponsorForm.is_valid():
               sponsorForm = sponsorForm.save(commit=False)
               sponsorForm.EnteredBy = '%s %s'%(request.user.first_name, request.user.last_name)
               sponsorForm.UpdateDate = currentDt
               sponsorForm.FirstName = (sponsorForm.FirstName).title()
               if sponsorForm.MiddleName:
                    sponsorForm.MiddleName = (sponsorForm.MiddleName).title()
               sponsorForm.LastName = (sponsorForm.LastName).title()
               sponsorForm.Memo = (sponsorForm.Memo).title()
               sponsorForm.user = request.user
               sponsorForm.save()
               return HttpResponseRedirect('/sponsor/sponsordata/')
          context = {"frmObj": sponsorForm}
          return render(request, "SponsorsData/sponsorForm.html", context)
     elif request.method == "GET":
          if id:
               rcdId = get_object_or_404(SponsorsData, id=id)
               #Find requested data
               sponsorForm = UpdateSponsorForm(instance=rcdId)
               context = {"frmObj": sponsorForm}
               tem = "SponsorsData/sponsorForm.html"
          else:
               tem = "SponsorsData/sponsordata.html"
               sponsorForm = UpdateSponsorForm(request.POST)
               context = {"frmObj": sponsorForm}
          return render(request, tem, context)

# Sponsor form view
@login_required
def sponsor_form_view(request,*args, **kwargs):
     currentDt = dt.strptime(str(dt.today()).split(' ')[0], '%Y-%m-%d').strftime('%m/%d/%Y')
     sponsorForm = SponsorForm()
     if request.is_ajax():

          # Autocompalete list for Name
          if request.POST.get('lst'):
               print(request.POST.get('lst'))
               if request.POST.get('lst').split('-')[0][3:]=='FirstName':
                    fnList = list(imsData.objects.filter(
                         FirstName__startswith=request.POST.get('lst').split('-')[1]).values_list('FirstName', flat=True).distinct()[:10])
               elif request.POST.get('lst').split('-')[0][3:]=='LastName':
                    fnList = list(imsData.objects.filter(
                         LastName__startswith=request.POST.get('lst').split('-')[1]).values_list('LastName', flat=True).distinct())
               elif request.POST.get('lst').split('-')[0][3:]=='MiddleName':
                    fnList = list(imsData.objects.filter(
                         MiddleName__startswith=request.POST.get('lst').split('-')[1]).values_list('MiddleName', flat=True).distinct())
               elif request.POST.get('lst').split('-')[0][3:]=='undefined':
                    fnList = ""

               return HttpResponse(json.dumps(fnList))

          # Auto populate list for Country
          if request.POST.get('country'):
               country_id = request.POST.get('country')
               obj = st.objects.order_by('StateName').filter(CountryName_id=country_id).values('id', 'StateName')
               opt = '<option value="">-----------</option>'
               for o in obj:
                    opt = opt+'<option value="%s">%s</option>'%(o['id'], o['StateName'])
               return HttpResponse(opt)

          # Auto populate list for City
          if request.POST.get('city'):
               state_id = request.POST.get('city')
               obj = ct.objects.order_by('City').filter(StateName_id=state_id).values('id', 'City')
               opt = '<option value="">-----------</option>'
               for o in obj:
                    opt = opt+'<option value="%s">%s</option>'%(o['id'], o['City'])
               return HttpResponse(opt)

          # Auto populate list for Purpose
          if request.POST.get('purpose'):
               purposeList = []
               purpose_id = request.POST.get('purpose')
               pV = p.objects.order_by('Purpose').filter(id=purpose_id)
               # obj = pc.objects.order_by('Purpose_Code').filter(purpose=pV[0]).values("Purpose_Code")
               # purposeList.append(obj[0]['Purpose_Code'])
               # obj = pc.objects.order_by('Purpose_Code').filter(purpose=pV[0]).values("purposeindex")
               # purposeList.append(obj[0]['purposeindex'])
               # print(obj[0]['purposeindex'])
               obj = pdM.objects.filter(Purpose=pV[0])
               # print(obj)
               # purposeList.append(obj[0]['AnnounceAs'])
               return HttpResponse(serializers.serialize('json', obj), content_type ="application/json")

          # Auto populate list for Purpose code and indes
          if request.POST.get('purpose2'):
               purpose_id = request.POST.get('purpose2')
               pV = p.objects.order_by('Purpose').filter(id=purpose_id)
               obj = pc.objects.order_by('Purpose_Code').filter(purpose=pV[0]).values("purposeindex")
               return HttpResponse(obj[0]['purposeindex'])

          # Auto populate list for Zipcode
          if request.POST.get('zipcode'):
               zipcode_id = request.POST.get('zipcode')
               try:
                    ctId = zc.objects.order_by('ZipCode').filter(ZipCode=zipcode_id).values("City_id", "City")
                    ctNm = ct.objects.order_by('City').filter(id=ctId[0]['City']).values("City", "StateName", "county")
                    stNm = st.objects.order_by('StateName').filter(id=ctNm[0]['StateName']).values("StateAbbr", "CountryName")
                    cNm = c.objects.order_by('CountryName').filter(id=stNm[0]['CountryName']).values("CountryName")
                    rsDict = dict(id_Country=cNm[0]['CountryName'], id_State=stNm[0]['StateAbbr'], id_City=ctNm[0]['City'])
               except Exception as inst:
                    rsDict = dict(id_Country='NA', id_State='NA', id_City='NA')
               return HttpResponse(json.dumps(rsDict),content_type="application/json")


     if request.method =="POST":
          sponsorForm = SponsorForm(request.POST)
          if sponsorForm.is_valid():
               sponsorForm.save()
               sponsorForm = SponsorForm()

     fnList = imsData.objects.values_list('FirstName', flat=True).distinct()
     #fnList = serializers.serialize('json', list(fnList))
     fnList = list(fnList)

     context = {"frmObj": sponsorForm, 'fnList': fnList}
     return render(request, "SponsorsData/sponsorForm.html", context)

# Slide page view
@login_required
def display_view(request,*args, **kwargs):
     currentDt = dt.strptime(str(dt.today()).split(' ')[0], '%Y-%m-%d').strftime('%m/%d/%y')
     currentYr = '%s'%(str(dt.today()).split('-')[0])
     dateList = [dt.today(), dt(dt.now().year, 12, 31)]
     nos = 0
     inData = SponsorsData.objects.filter(sponsorshipDate__in=dateList).order_by('PurposeIndex').values('PurposeIndex').distinct()
     if len(inData)>0:
          #print(inData.values_list('PurposeIndex', flat=True).distinct())
          #inCount = SponsorsData.objects.filter(sponsorshipDate=dt.today()).filter(PurposeIndex=inData[0]['PurposeIndex']).values('PurposeIndex')
          #print(inCount.values_list('PurposeIndex', flat=True).distinct())
          nos = 0
          noRcd = 8
          nosr = {}
          indNumber = inData.order_by('PurposeIndex').values_list('PurposeIndex', flat=True).distinct()
          for x in indNumber:
               pdData = pdM.objects.filter(Purpose_Index=x).values('DisplayOnPPT')[0]
               if len(pdData['DisplayOnPPT']) > 39: noRcd = 6
               else:noRcd = 8
               indNum = int(x)
               inCount = SponsorsData.objects.filter(sponsorshipDate__in=dateList).filter(PurposeIndex=x).values('PurposeIndex')
               #print('%s- %s'%(inCount, len(inCount)))
               addOne = 0
               n = nos
               if len(inCount)%noRcd>0: addOne = 1
               y = addOne + len(inCount)//noRcd
               nos = nos + y
               sp = 0
               ep = 0
               while n <= (len(inCount)//noRcd)-1:
                    #print('(%s) %s: [%s, %s]'%(len(inCount)//noRcd, n, indNum, noRcd))
                    ep = ep + noRcd
                    nosr[n] = [indNum, noRcd, [sp, ep]]
                    sp = noRcd
                    n+=1
               if addOne==1: ep = ep + len(inCount)%noRcd; nosr[n]=[indNum, len(inCount)%noRcd, [sp, ep]]
     if request.is_ajax():
          if request.method == "POST":
               #rcdId = request.POST['id']
               if request.POST.get('sldNumToOpen'):
                    #print(nos)
                    sldTitle = '<div>No Sponsor Found.</div>'
                    #tblVlFinal = '<h1 class="alert-message gp-display-middle">There are no sponsors added for today\'s date.</h1>'
                    tblVlFinal = '<h1>None sponsor record found.</h1>'
                    if nos>0:
                         getDataFor = (request.POST.get('sldNumToOpen')).split("-")[0]
                         num = int((request.POST.get('sldNumToOpen')).split("-")[1])
                         lst = nosr[num-1]
                         rwVlFinal = ''
                         pdData = pdM.objects.filter(Purpose_Index=lst[0]).values('DisplayOnPPT')[0]
                         if len(pdData['DisplayOnPPT']) > 39: tmt = 199
                         else:tmt = 120
                         #print(pdData['DisplayOnPPT'])
                         sldTitle = '<div>' + pdData['DisplayOnPPT'] + '</div>'
                         # Find all records and create table row for html
                         spData = SponsorsData.objects.filter(sponsorshipDate__in=dateList).filter(PurposeIndex=lst[0]).order_by('FirstName', 'LastName', 'City')[lst[2][0]:lst[2][1]]
                         for rw in spData:
                              fd = str(rd.randint(100, 1000))
                              sd = str(rd.randint(1000, 10000))
                              spDate = dt.strptime(str(rw.sponsorshipDate), '%Y-%m-%d').strftime('%m/%d/%y')
                              updDate = dt.strptime(str(rw.UpdatedDate).split(' ')[0], '%Y-%m-%d').strftime('%m/%d/%y')
                              if getDataFor == 'display':
                                   rwVl = '<tr class="gp-transparent">'
                                   rwVl=rwVl + '<td class="slFClm" id="'+fd+str(rw.id)+sd+'">'
                                   rwVl=rwVl + rw.FirstName + ' ' + rw.LastName+'</td>'
                                   rwVl=rwVl +'<td class="slSClm">'
                                   rwVl=rwVl + str(rw.City) + ', ' + str(rw.State) +'</td>'
                                   rwVl=rwVl + '</tr>'
                                   rwVlFinal = rwVlFinal + rwVl
                              elif getDataFor == 'announce':
                                   rwVl = '<tr class="gp-transparent">'
                                   rwVl=rwVl + '<td class="anFClm gp-mobile" id="'+fd+str(rw.id)+sd+'">'
                                   rwVl=rwVl + rw.FirstName + ' ' + rw.LastName+' - '+rw.Memo+'('+str(rw.City)+', '+str(rw.State)+')</td>'
                                   rwVl=rwVl + '</tr>'
                                   rwVlFinal = rwVlFinal + rwVl

                         tblVlFinal =  '<div class="gp-responsive" id="sldTbl"><table class="gp-table-all"><div class="gp-row">'
                         tblVlFinal = tblVlFinal + '<col span="1" style="width:60%;border-width:0.001em;border-style:solid;border-color:rgb(169,16,169);">'
                         tblVlFinal = tblVlFinal + '<col span="1" style="width:40%;border-width:0.001em;border-style:solid;border-color:rgb(169,16,169);">'
                         tblVlFinal = tblVlFinal + '</div>' + rwVlFinal + '</table></div>'
                    rsDict = dict(cngDpTable=tblVlFinal, cngDpTitle=sldTitle, nos=nos, tblMarginTop=tmt)
                    return HttpResponse(json.dumps(rsDict),content_type="application/json")
                    #       <div class="gp-responsive">
                    #       <table class="gp-table-all">
                    #         <div class="gp-row">
                    #           <col span="1" style="width:70%;border-width:0.001em;border-style:solid;border-color:rgb(169,16,169);">
                    #           <col span="1" style="width:30%;border-width:0.001em;border-style:solid;border-color:rgb(169,16,169);">
                    #         </div>
                    #      </table>
                    #     </div>
# style="margin-bottom:150px;"  gp-display-bottommiddle
     tblVlFinal = '<div class="gp-container gp-hide-small" id="ttSetting">'
     tblVlFinal = tblVlFinal + '<div class="gp-button gp-padding gp-orange gp-card-4 gp-round gp-margin-right gp-text-black">'
     tblVlFinal = tblVlFinal + '<i class="material-icons" onclick="openFullscreen(\'pptSlidesContainer\', \'pptDisplay\');AutoSlideShow();changeData(\'display\')">replay_10</i>'
     tblVlFinal = tblVlFinal + '<p>Slideshow</p>'
     tblVlFinal = tblVlFinal + '</div>'
     tblVlFinal = tblVlFinal + '<div class="gp-button gp-padding gp-blue gp-card-4 gp-round gp-margin-right gp-text-black">'
     tblVlFinal = tblVlFinal + '<i class="material-icons" onclick="openFullscreen(\'pptSlidesContainer\', \'pptDisplay\');SlideShow(\'display\')">slideshow</i>'
     tblVlFinal = tblVlFinal + '<p>Slideshow</p>'
     tblVlFinal = tblVlFinal + '</div>'
     tblVlFinal = tblVlFinal + '<div class="gp-button gp-padding gp-yellow gp-card-4 gp-round gp-margin-right gp-text-black">'
     tblVlFinal = tblVlFinal + '<i class="material-icons" onclick="openFullscreen(\'pptSlidesContainer\', \'pptDisplay\');SlideShow(\'announce\')">slideshow</i>'
     tblVlFinal = tblVlFinal + '<p>Announce</p>'
     tblVlFinal = tblVlFinal + '</div>'
     tblVlFinal = tblVlFinal + '<div class="gp-button gp-padding gp-green gp-card-4 gp-round gp-margin-right gp-text-black">'
     tblVlFinal = tblVlFinal + '<i class="material-icons">format_list_numbered</i>'
     tblVlFinal = tblVlFinal + '<p>Index</p>'
     tblVlFinal = tblVlFinal + '</div>'
     tblVlFinal = tblVlFinal + '<div class="gp-button gp-padding gp-indigo gp-card-4 gp-round gp-text-black">'
     tblVlFinal = tblVlFinal + '<i class="material-icons">settings</i>'
     tblVlFinal = tblVlFinal + '<p>Setting</p>'
     tblVlFinal = tblVlFinal + '</div></div>'

     city = ''
     state = ''
     # User online
     if len(LoggedUser.objects.all())>0:
          city = LoggedUser.objects.filter(username=request.user.username, loggedIn='Y',
          userAddr=str(request.META.get('REMOTE_ADDR'))).values('userCity')[0]['userCity']
          state = LoggedUser.objects.filter(username=request.user.username, loggedIn='Y',
          userAddr=str(request.META.get('REMOTE_ADDR'))).values('userState')[0]['userState']

     context = {"spObj": tblVlFinal, "NoOfSlides": nos,
     "userCity": city, "userState": state}
     return render(request, "display/display.html", context)

# Purpose code page view
@login_required
def purposecode_view(request,*args, **kwargs):
     PurposeForm = purposeForm()
     if request.is_ajax():
          if request.method == "POST":
               if request.POST.get('itemData'):
                    if request.POST.get('itemData') == 'pContainerLarge':
                         fldFinal = ''
                         y = 0
                         # , DisplayOnPPT, AnnounceAs
                         lst = ['Purpose_Index','Purpose_Code','Purpose', '']
                         # Create a table header
                         for x in lst:
                              if x in purposeData._meta.fields:
                                   lblName = purposeData._meta.get_field(x).verbose_name
                              else:
                                   lblName = x
                              y += 1
                              # gp-button <i onclick="sortTable(' + str(y) + ')" class="fa fa-sort gp-right gp-hide-small gp-hide-medium"></i>
                              fld = '<th class="gp-hover-grayscale gp-medium">' + lblName
                              fld = fld + '</th>'
                              fldFinal = fldFinal + fld
                         fldFinal='<thead><tr class="gp-red gp-border">'+fldFinal+'</tr></thead>'

                         # Find all records and create table row for html
                         pData = purposeData.objects.all().order_by('Purpose_Index')
                         rwVlFinal = ''
                         rwVlFinal2 = ''
                         #onclick="rwClick('+ str(rw.id) +')"
                         # data-update-ref="//sponsordata//sponsor_data_form//"
                         for rw in pData:
                              fd = str(rd.randint(100, 1000))
                              sd = str(rd.randint(1000, 10000))
                              rwVl = '<tr class="tblRwId" href="?#'+(rw.Purpose_Code if rw.Purpose_Code is not None else '') +'" id='+fd+str(rw.id)+sd+' data-update-ref="/sponsordata/">'
                              rwVl=rwVl + '<td>'+str(rw.Purpose_Index)+'</td>'
                              rwVl=rwVl + '<td>'+rw.Purpose_Code+'</td>'
                              rwVl=rwVl + '<td><p> Puprpose : '+rw.Purpose+'</p><p> Display As : '+rw.DisplayOnPPT+'</p><p> Announce As : '+rw.AnnounceAs+'</p></td>'
                              rwVl=rwVl + '<td><span class="gp-button gp-red" id="updatePurpose">Update</span></td>'
                              rwVl=rwVl + '</tr>'
                              rwVlFinal = rwVlFinal + rwVl
                         #style="font-size:1vw;"
                         rwVlFinal = '<tbody id="dbPTableBody1">' + rwVlFinal + '</tbody>'
                         rwVlFinal = fldFinal+rwVlFinal

                    if request.POST.get('itemData') == 'pContainerSmall':
                         fldFinal = ''
                         y = 0
                         # , DisplayOnPPT, AnnounceAs
                         # lst = ['Purpose_Index','Purpose_Code','Purpose', '']
                         lst = ['']
                         # Create a table header
                         for x in lst:
                              if x in purposeData._meta.fields:
                                   lblName = purposeData._meta.get_field(x).verbose_name
                              else:
                                   lblName = x
                              y += 1
                              fld = '<th class="gp-button gp-hover-grayscale gp-medium">' + lblName
                              fld = fld + '<i onclick="sortTable(' + str(y) + ')" class="fa fa-sort gp-right gp-hide-small gp-hide-medium"></i></th>'
                              fldFinal = fldFinal + fld
                         fldFinal='<thead><tr class="gp-red gp-border">'+fldFinal+'</tr></thead>'
                         fldFinal = ''
                         # Find all records and create table row for html
                         pData = purposeData.objects.all().order_by('Purpose_Index')
                         rwVlFinal = ''
                         rwVlFinal2 = ''
                         x = 0; y = 1
                         #onclick="rwClick('+ str(rw.id) +')"
                         # data-update-ref="//sponsordata//sponsor_data_form//"
                         for rw in pData:
                              fd = str(rd.randint(100, 1000))
                              sd = str(rd.randint(1000, 10000))
                              # rwVl = '<tr class="tblRwId" href="?#'+(rw.Purpose_Code if rw.Purpose_Code is not None else '') +'" id='+fd+str(rw.id)+sd+' data-update-ref="/sponsordata/">'
                              # rwVl=rwVl + '<td>'+str(rw.Purpose_Index)+'</td>'
                              # rwVl=rwVl + '<td>'+rw.Purpose_Code+'</td>'
                              # rwVl=rwVl + '<td><p> Puprpose : '+rw.Purpose+'</p><p> Display As : '+rw.DisplayOnPPT+'</p><p> Announce As : '+rw.AnnounceAs+'</p></td>'
                              # rwVl=rwVl + '<td><span class="gp-button gp-red">Update</span></td>'
                              # rwVl=rwVl + '</tr>'<span class="gp-left gp-padding">'+str(rw.Purpose_Index)+'</span><span class="gp-right gp-padding">'+rw.Purpose_Code+'</span>
                              rwVl = '<div class="gp-card gp-round" href="?#'+(rw.Purpose_Code if rw.Purpose_Code is not None else '') +'" id='+fd+str(rw.id)+sd+' data-update-ref="/sponsordata/">'
                              rwVl=rwVl + '<div class="gp-row gp-display-container gp-blue-grey"><div class="gp-col s3 gp-left">'+str(rw.Purpose_Index)+'</div>'
                              rwVl=rwVl + '<div class="gp-col s3 gp-padding"></div>'
                              rwVl=rwVl + '<div class="gp-col s3 gp-padding"></div>'
                              rwVl=rwVl + '<div class="gp-col s3">'+rw.Purpose_Code+'</div></div>'
                              rwVl=rwVl + '<div class="gp-container gp-display-container gp-white"><div class="gp-block gp-center gp-padding dp'+str(x)+'" id="1"><strong>Puprpose</strong><p class="gp-center">'+rw.Purpose+'</p></div>'
                              rwVl=rwVl + '<div class="gp-block gp-center gp-padding gp-hide dp'+str(x)+'" id="2"><strong>Display On PPT</strong><p class="gp-center">'+rw.DisplayOnPPT+'</p></div>'
                              rwVl=rwVl + '<div class="gp-block gp-center gp-padding gp-hide dp'+str(x)+'" id="3"><strong>AnnounceAs</strong><p class="gp-center">'+rw.AnnounceAs+'</p></div>'
                              rwVl=rwVl + '<button class="gp-button gp-display-left gp-transparent gp-border-0 fas" id="prvBtn'+str(x)+'" style="width:50%;height:100%;position:absolute;opacity:0;z-index:0;">&#xf100;</button>'
                              rwVl=rwVl + '<button class="gp-button gp-display-right gp-transparent gp-border-0 fas" id="nxtBtn'+str(x)+'" style="width:50%;height:100%;;position:absolute;opacity:0;z-index:0;">&#xf101;</button>'
                              rwVl=rwVl + '</div>'
                              rwVl=rwVl + '<div class="gp-row gp-display-container gp-light-gray gp-border-top">'
                              rwVl=rwVl + '<div class="gp-col gp-small gp-padding" id="updatePurpose" style="width:50%;"></div>'
                              rwVl=rwVl + '<div class="gp-col gp-red gp-small gp-border-left" id="updatePurpose" style="width:50%;">Update</div></div>'
                              rwVl=rwVl + '</div><div class="gp-padding-small"></div>'
                              rwVlFinal = rwVlFinal + rwVl
                              x+=1
                         #style="font-size:1vw;"
                         # rwVlFinal = '<tbody id="dbPTableBody1">' + rwVlFinal + '</tbody>'
                         rwVlFinal = fldFinal+rwVlFinal

                    return HttpResponse(rwVlFinal)

     if request.method =="POST":
          PurposeForm = purposeForm(request.POST)
          if PurposeForm.is_valid():
               PurposeForm.save()
               PurposeForm = purposeForm()
     context = {"objPurposeForm": PurposeForm}
     return render(request, "purposecode/purpose.html", context)

# Team page view
@login_required
def team_group_view(request,*args, **kwargs):
    groupList = []
    #for g in request.user.groups.all():
    #    print(g.name)
    #print(staticfiles_storage.path('img/icons/Master/svg/Team.svg'))
    lstTag = ''
    lst2 = ''
    noItem = 4
    user = get_user_model()
    userCounter = 0
    for u in user.objects.all().order_by('first_name'):
        query_set = Group.objects.filter(user = u)
        for g in query_set:
            #print(g.name) # or id or whatever Group field that you want to display
            groupList.append(g.name)
        str1 = ', '.join(groupList)
        groupList.clear()
        userCounter += 1

        #print('%s %s' %((u.first_name).upper(), (u.last_name).upper()))
        lst = "<div class='gp-col l3 m6 s6 gp-zoom' style='height:20vh; margin-top: 2vh'>"
        lst = lst + " <img src='\static\img\icons\Master\svg\Team.svg' style='width:35%;' class='gp-circle gp-hover-opacity tmImg'>"
        # <imgs src='\static\img\icons\Master\svg\Team.svg' style='width:5vw' class='gp-circle gp-hover-opacity'>"
        lst = lst + " <br><div class='gp-text-white tmName' style='padding:1px;font-size:95%'>" + "%s %s" %((u.first_name).upper(), (u.last_name).upper()) +"</div>"
        #lst = lst + " <p class='gp-text-white tmGroup' style='padding:1px;font-size:80%'>"+ str1 +"</p>"
        lst = lst + " </div>"
        lst2 = lst2 + lst
        if userCounter % noItem == 0:
            lstBng = "<div class='gp-row' style='margin: 0'>"
            lstEnd = "</div>"
            lstTag = lstTag + lstBng + lst2 + lstEnd
            lst2 = ''

        if userCounter == len(user.objects.all()):
            if userCounter % noItem > 0:
                userCounter = noItem
                lstBng = "<div class='gp-row' style='margin: 0'>"
                lstEnd = "</div>"
                lstTag = lstTag +lstBng + lst2 + lstEnd
                lst2 = ''

    context = {"objTeamLstTag": lstTag}
    return render(request, "Team/team.html", context)

# Announcer page view
@login_required
def announcer_view(request,*args, **kwargs):
     context = {"objDict": 'xyz'}
     return render(request, "announcer/comingsoon.html", context)