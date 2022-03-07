from django.db import models
from django.utils.timezone import get_current_timezone
from datetime import datetime
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User
# from purposecodeApp.models import Purpose

# User loged in and loged out modal


class LoggedUser(models.Model):
    username = models.CharField(max_length=30, blank=True, null=True)
    loggedIn = models.CharField(max_length=30, blank=True, null=True)
    userAddr = models.CharField(max_length=30, blank=True, null=True)
    userCity = models.CharField(max_length=30, blank=True, null=True)
    userState = models.CharField(max_length=2, blank=True, null=True)
    userLocDict = models.CharField(max_length=500, blank=True, null=True)
    currentTimeStamp = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.currentTimeStamp = datetime.now()
        return super(LoggedUser, self).save(*args, **kwargs)


class PurposeCode(models.Model):
    Purpose_Code = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.Purpose_Code


class Purpose(models.Model):
    Purpose = models.CharField(max_length=120, blank=True, null=True)
    Purpose_Code = models.ForeignKey(
        PurposeCode, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.Purpose


class DisplayPurpose(models.Model):
    DisplayPurpose = models.CharField(max_length=120, blank=True, null=True)
    Purpose_Code = models.ForeignKey(
        PurposeCode, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.DisplayPurpose


class PurposeIndex(models.Model):
    Purpose_Index = models.CharField(max_length=120, blank=True, null=True)
    Purpose_Code = models.ForeignKey(
        PurposeCode, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.Purpose_Index

# Create your models here.


class purposeData(models.Model):
    currentTimeStamp = models.DateField(auto_now=True, blank=True, null=True)
    Purpose = models.CharField(
        'Purpose', max_length=120, blank=True, null=True)
    Purpose_Code = models.CharField(
        'Purpose Code', max_length=120, blank=True, null=True)
    Purpose_Index = models.IntegerField('Purpose Index', blank=True, null=True)
    DisplayOnPPT = models.CharField(
        'Purpose Title', max_length=120, blank=True, null=True)
    AnnounceAs = models.CharField(
        'Annoucer Note', max_length=120, blank=True, null=True)
    UpdatedDate = models.DateTimeField(
        'Updated Date', auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.Purpose


class Country(models.Model):
    CountryName = models.CharField(
        'State Name', max_length=120, blank=True, null=True)

    def __str__(self):
        return self.CountryName


class State(models.Model):
    StateName = models.CharField(
        'State Name', max_length=120, blank=True, null=True)
    StateAbbr = models.CharField(
        'State Abbr', max_length=120, blank=True, null=True)
    CountryName = models.ForeignKey(
        Country, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.StateName


class City(models.Model):
    City = models.CharField('City', max_length=120, blank=True, null=True)
    StateName = models.ForeignKey(
        State, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.City


class County(models.Model):
    CountyName = models.CharField(
        'County Name', max_length=120, blank=True, null=True)
    City = models.ForeignKey(
        City, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.CountyName


class ZipCode(models.Model):
    ZipCode = models.CharField(
        'Zip Code', max_length=120, blank=True, null=True)
    City = models.ForeignKey(
        City, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.ZipCode

# Create your models here.


class LocationData(models.Model):
    Country = models.CharField(
        'Country', max_length=120, blank=True, null=True)
    StateAbbr = models.CharField(
        'State Abbr', max_length=120, blank=True, null=True)
    StateName = models.CharField(
        'State', max_length=120, blank=True, null=True)
    City = models.CharField('City', max_length=120, blank=True, null=True)
    CountyName = models.CharField(
        'County', max_length=120, blank=True, null=True)
    ZipCode = models.CharField(
        'Zip Code', max_length=120, blank=True, null=True)
    UpdatedDate = models.DateTimeField('Updated Date', auto_now=True)
    #user=models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.StateAbbr

# class PurposeCode(models.Model):
#     Purpose_Code=models.CharField(max_length=120, blank=True, null=True)

#     def __str__(self):
#         return self.Purpose_Code

# class PurposeIndex(models.Model):
#     Purpose_Index=models.CharField(max_length=120, blank=True, null=True)
#     Purpose_Code=models.ForeignKey(PurposeCode, on_delete=models.CASCADE,blank=True, null=True)

#     def __str__(self):
#         return self.Purpose_Index

# class Purpose(models.Model):
#     Purpose=models.CharField(max_length=120, blank=True, null=True)
#     Purpose_Code=models.ForeignKey(PurposeCode, on_delete=models.CASCADE,blank=True, null=True)

#     def __str__(self):
#         return self.Purpose

# class DisplayPurpose(models.Model):
#     DisplayPurpose=models.CharField(max_length=120, blank=True, null=True)
#     Purpose_Code=models.ForeignKey(PurposeCode, on_delete=models.CASCADE,blank=True, null=True)

#     def __str__(self):
#         return self.DisplayPurpose


# Create your models here.
class SponsorsData(models.Model):
    COUNTRY_CHOICES = (
        ('1', 'INDIA'),
        ('2', 'USA'),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    YESNO_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    CITY_CHOICES = (
        ('1', 'Atlanta'),
        ('2', 'Cumming'),
        ('3', 'Alpharetta')
    )
    STATE_CHOICES = (
        ('1', 'GA'),
        ('2', 'FL')
    )
    PURPOSE_CHOICES = (
        ('ravi sabha', 'Ravi Sabha'),
        ('all ravi sabha', 'All Ravi Sabha'),
        ('grand ravi sabha', 'Grand Ravi Sabha'),
    )
    FirstName = models.CharField(
        'First Name', max_length=120, blank=True, null=True)
    MiddleName = models.CharField(
        'Middle Name', max_length=120, blank=True, null=True)
    LastName = models.CharField(
        'Last Name', max_length=120, blank=True, null=True)
    MemberId = models.DecimalField(
        'Member Id', default=0, max_digits=20, decimal_places=0, blank=True, null=True)
    Gender = models.CharField(
        'Gender', max_length=1, blank=True, null=True, choices=GENDER_CHOICES, default='M')
    ZipCode = models.DecimalField(
        'Zip Code', max_digits=20, decimal_places=0, blank=True, null=True)
    #Country=models.ForeignKey(Country, on_delete=models.CASCADE,blank=True, null=True)
    #State=models.ForeignKey(State, on_delete=models.CASCADE,blank=True, null=True)
    #City=models.ForeignKey(City, on_delete=models.CASCADE,blank=True, null=True)
    # , choices=COUNTRY_CHOICES, default='US'), choices=STATE_CHOICES, default='Georgia'), choices=CITY_CHOICES, default='')
    City = models.CharField('City', max_length=120, blank=True, null=True)
    State = models.CharField('State', max_length=120, blank=True, null=True)
    Country = models.CharField(
        'Country', max_length=120, blank=True, null=True)
    #Purpose=models.CharField('Purpose',max_length=120,blank=True, null=True, choices=PURPOSE_CHOICES, default='NA')
    Purpose = models.ForeignKey(
        Purpose, on_delete=models.CASCADE, blank=True, null=True)
    Purpose_Code = models.CharField(
        'Purpose Code', max_length=120, blank=True, null=True)
    PurposeIndex = models.DecimalField(
        'Purpose Index', default=0, max_digits=20, decimal_places=0, blank=True, null=True)
    #Purpose_Code=models.ForeignKey(PurposeCode, on_delete=models.CASCADE,blank=True, null=True)
    #PurposeIndex=models.ForeignKey(PurposeIndex, on_delete=models.CASCADE,blank=True, null=True)
    Memo = models.CharField('Announcer Note(s)', default='NA',
                            blank=True, null=True, max_length=200)
    currentTimeStamp = models.DateTimeField(auto_now_add=True)
    sponsorshipDate = models.DateField(
        'Sponsor Date', default=timezone.now, blank=True, null=True)
    DisplayOnPPT = models.CharField(
        'PPT', max_length=3, blank=True, null=True, choices=YESNO_CHOICES, default='Y')
    Announce = models.CharField(
        'Announce', max_length=3, blank=True, null=True, choices=YESNO_CHOICES, default='Y')
    amountReceived = models.CharField(
        'Amount Received', max_length=3, blank=True, null=True, choices=YESNO_CHOICES, default='Y')
    EnteredBy = models.CharField(
        'Entered By', max_length=120, blank=True, null=True)
    UpdatedDate = models.DateTimeField('Updated Date', auto_now=True)
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return ('%s (%s %s)') % (self.id, self.FirstName, self.LastName)

    def save(self, *args, **kwargs):
        self.FirstName = self.FirstName.title()
        if self.MiddleName is not None:
            self.MiddleName = self.MiddleName.title()
        self.LastName = self.LastName.title()
        self.City = self.City.title()
        self.State = self.State.upper()
        self.Memo = self.Memo.title()
        return super(SponsorsData, self).save(*args, **kwargs)


class searchData(models.Model):
    inputSearch = models.CharField(
        'Search', max_length=120, blank=True, null=True)

    def __str__(self):
        return self.inputSearch

# Need to focus models here.


class needTofocusData(models.Model):
    currentTimeStamp = models.DateField(auto_now=True, blank=True, null=True)
    NeedToFocus = models.CharField(
        'Need To Focus', max_length=120, blank=True, null=True)
    StartDate = models.DateTimeField(
        'Updated Date', auto_now=True, blank=True, null=True)
    EndDate = models.DateField(
        'Sponsor Date', default=timezone.now, blank=True, null=True)
    UpdatedDate = models.DateTimeField('Updated Date', auto_now=True)

    def __str__(self):
        return self.NeedToFocus

# Need to focus models here.


class upcommingEventsData(models.Model):
    currentTimeStamp = models.DateField(auto_now=True, blank=True, null=True)
    upcommingEvents = models.CharField(
        'Upcoming Event', max_length=120, blank=True, null=True)
    StartDate = models.DateTimeField(
        'Updated Date', auto_now=True, blank=True, null=True)
    EndDate = models.DateField(
        'Sponsor Date', default=timezone.now, blank=True, null=True)
    UpdatedDate = models.DateTimeField('Updated Date', auto_now=True)

    def __str__(self):
        return self.upcommingEvents
