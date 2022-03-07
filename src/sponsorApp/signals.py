from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
#from django.shortcuts import render_to_response
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import random as rd
from datetime import datetime as dt
from .models import LoggedUser, SponsorsData

#User/Data enter/update/delete status alert
bgUl = '<ul class="gp-ul gp-display-topmiddle gp-round-large" id="appStatus" style="width: auto; margin-top: 60px;">'
enUl = '</ul>'

#Sending a note/alert message
bgNote = '<div class="gp-panel gp-blue gp-display-container gp-display-topmiddle gp-round gp-large gp-zoom" '
bgNote = bgNote + 'style="width: 80vw; margin-top: 60px;">'
bgNote = bgNote + '<span onclick="this.parentElement.style.display=\'none\'" '
bgNote = bgNote + 'class="gp-button gp-display-topright gp-large">&times;</span><h3>Info!</h3><p>'
enNote = '</p></div>'

# User logged in
@receiver(user_logged_in)
def UserLoggedInStatus(sender, request, user, **kwargs):    
     if user:
          print(user.first_name)
          #print(request.META.get('REMOTE_ADDR'))
          uStatusListHTML = "<li class='gp-display-container gp-left-align gp-round' id='id_" + str(user) + "'>" + str(user) + "<span class='gp-transparent gp-display-right gp-text-red'>Online</span></li>"
          uStatusHTML = bgUl + "<li class='gp-blue gp-round'>" + str(user) + " Online</li>" + enUl
          #uStatusHTML = bgNote + "<h1'>" + str(user) + " Online</h1>" + enNote
          uName = user
          curretUserStatus = {
               "Desc": "User Log In/Out.",
               "type": "Online",
               "username": str(user),
               "uStatus": uStatusHTML,
               "uStatusList": uStatusListHTML
          }
          channel_layer = get_channel_layer()
          async_to_sync(channel_layer.group_send)(
               "uStatus", 
               {
                    "type": "user.uStatus",
                    "text": json.dumps(curretUserStatus)
               }
          )

          u = LoggedUser.objects.filter(username=str(user), loggedIn='Y', userAddr=str(request.META.get('REMOTE_ADDR')))
          #u = LoggedUser.objects.filter(username=str(user), loggedIn='Y')
          print(len(u))
          x = 0
          if len(u)>0:
               LoggedUser.objects.filter(username=str(user), loggedIn='Y', userAddr=str(request.META.get('REMOTE_ADDR'))).update(loggedIn='N')
               #u1 = LoggedUser.objects.filter(username=str(user), loggedIn='Y', userAddrs=str(request.META.get('REMOTE_ADDR')))[0]
          print(request.META.get('REMOTE_ADDR'))
          LoggedUser(username=str(user), loggedIn='Y', userAddr=str(request.META.get('REMOTE_ADDR'))).save()

# User logged in
@receiver(user_logged_out)
def UserLoggedOutStatus(sender, request, user, **kwargs):    
     if user:
          print(user)
          uStatusListHTML = "<li class='gp-display-container gp-left-align gp-round' id='id_" + str(user) + "'>" + str(user) + "<span class='gp-transparent gp-display-right gp-text-red'>Offline</span></li>"
          uStatusHTML = bgUl + "<li class='gp-blue gp-round'>" + str(user) + " Offline</li>" + enUl
          uName = user
          curretUserStatus = {
               "Desc": "User Log In/Out.",
               "type": "Offline",
               "username": str(user),
               "uStatus": uStatusHTML,
               "uStatusList": uStatusListHTML
          }
          channel_layer = get_channel_layer()
          async_to_sync(channel_layer.group_send)(
               "uStatus", 
               {
                    "type": "user.uStatus",
                    "text": json.dumps(curretUserStatus)
               }
          )
          u = LoggedUser.objects.filter(username=str(user), loggedIn='Y', userAddr=str(request.META.get('REMOTE_ADDR')))
          #u = LoggedUser.objects.filter(username=str(user), loggedIn='Y')
          x = 0
          if len(u)>0:
               LoggedUser.objects.filter(username=str(user), loggedIn='Y', userAddr=str(request.META.get('REMOTE_ADDR'))).update(loggedIn='N')
               #u1 = LoggedUser.objects.filter(username=str(user), loggedIn='Y', userAddrs=str(request.META.get('REMOTE_ADDR')))[0]

# user_logged_in.connect(login_user)
# user_logged_out.connect(logout_user)

@receiver(post_save, sender=SponsorsData)
def spDataAddUpdated(sender, instance, created, **kwargs):
     fd = str(rd.randint(100, 1000))
     sd = str(rd.randint(1000, 10000))
     if created:
          print('Created')
          print(instance.pk)
          #rcd = SponsorsData.objects.last()
          #print(rcd)          
          spName = str(instance.FirstName + ' ' + instance.LastName)
          spDate = str(instance.sponsorshipDate)
          spLocation = str(instance.City + ', ' + instance.State          )
          spId = str(instance.pk)
          spStatus = "Added New Sponsor for - %s" % (spName)
     else:
          print('Updated')
          print(instance.pk)          
          spName = str(instance.FirstName + ' ' + instance.LastName)
          spDate = str(instance.sponsorshipDate)
          spLocation = str(instance.City + ', ' + instance.State)
          spId = str(instance.pk)
          spStatus = "Updated Sponsor for - %s" % (spName)
     
     spListHTML = '<tr id='+fd+str(spId)+sd+'><td style="width: 2px;"><img src="/static/img/icons/Master/svg/Sponsor.svg" class="gp-left gp-circle gp-margin-right" style="width:25px"></td>'
     spListHTML = spListHTML + '<td>'+ spName +'</td><td>'+ spLocation +'</td><td>'+ spDate +'</td></tr>'
     spStatusHTML = bgUl + "<li class='gp-blue gp-round'>" + spStatus + "</li>" + enUl
     todaysSponsors = len(SponsorsData.objects.filter(sponsorshipDate=dt.today()))
     totalSponsors = len(SponsorsData.objects.filter(sponsorshipDate__year='%s'%(str(dt.today()).split('-')[0])))
     sponsorStatus = {
          "Desc": "Sponsor Added/Updated",
          "type": spStatus,
          "spName": spName,
          "spDate": spDate,
          "spListHTML": spListHTML,
          "spStatusHTML": spStatusHTML,
          "spTotal": totalSponsors,
          "spTodayTotal": todaysSponsors
     }
     channel_layer = get_channel_layer()
     async_to_sync(channel_layer.group_send)(
          "uStatus", 
          {
               "type": "user.uStatus",
               "text": json.dumps(sponsorStatus)
          }
     )