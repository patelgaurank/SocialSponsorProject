from django.db import models
from django.core.files.storage import FileSystemStorage


fs = FileSystemStorage(location='/media/IMSProfileImage')

# Create your models here.
class imsData(models.Model):
	currentTimeStamp=models.DateField(auto_now=True)
	MemberID=models.DecimalField(default=0, max_digits=20, decimal_places=0,blank=True, null=True) 
	FirstName=models.CharField(max_length=120,blank=True, null=True) 
	MiddleName=models.CharField(max_length=120,blank=True, null=True) 
	LastName=models.CharField(max_length=120,blank=True, null=True) 
	SpouseFirstName=models.CharField(max_length=120,blank=True, null=True) 
	SpouseMemberID=models.DecimalField(default=0, max_digits=20, decimal_places=0,blank=True, null=True) 
	SatsangCategory=models.CharField(max_length=50,blank=True, null=True) 
	SatsangReference=models.CharField(max_length=50, default='NA',blank=True, null=True) 
	Mandal=models.CharField(max_length=50,blank=True, null=True) 
	Relation=models.CharField(max_length=50,blank=True, null=True) 
	FatherMemberID=models.DecimalField(default=0, max_digits=20, decimal_places=0,blank=True, null=True) 
	MotherMemberID=models.DecimalField(default=0, max_digits=20, decimal_places=0,blank=True, null=True) 
	NativePlace=models.CharField(max_length=50,blank=True, null=True) 
	NativeCountry=models.CharField(max_length=50,blank=True, null=True) 
	ZoneName=models.CharField(max_length=50,blank=True, null=True) 
	OtherAppPersonID=models.CharField(max_length=50,blank=True, null=True) 
	Gender=models.CharField(max_length=5, default='NA',blank=True, null=True) 
	Karyakar=models.CharField(max_length=5, default='NA',blank=True, null=True) 
	Volunteer=models.CharField(max_length=5, default='NA',blank=True, null=True) 
	GraduationYear=models.CharField(max_length=5,blank=True, null=True)
	Language=models.CharField(max_length=200,blank=True, null=True) 
	Profession=models.CharField(max_length=120, default='NA',blank=True, null=True) 
	PrimaryEmail=models.CharField(max_length=120, default='xyz@xyz.com',blank=True, null=True) 
	PrimaryCellPhone=models.CharField(max_length=14, default='(000)-000-0000',blank=True, null=True) 
	PrimaryHomePhone=models.CharField(max_length=14, default='(000)-000-0000',blank=True, null=True) 
	Country=models.CharField(max_length=50, default='USA',blank=True, null=True) 
	AddressLine1=models.CharField(max_length=120,blank=True, null=True) 
	AddressLine2=models.CharField(max_length=120,blank=True, null=True) 
	City=models.CharField(max_length=120,blank=True, null=True) 
	State=models.CharField(max_length=120,blank=True, null=True) 
	Zipcode=models.CharField(max_length=50, default='00000',blank=True, null=True) 
	Remarks=models.CharField(max_length=500,blank=True, null=True) 
	img=models.ImageField(upload_to='IMSProfileImage/', blank=True, null=True) 
	UpdatedDate=models.DateTimeField('Updated Date', auto_now=True) 
	EnteredBy=models.CharField(max_length=50, default='Unkown',blank=True, null=True)
	
	def __str__(self):
		return self.id
	def save(self, *args, **kwargs):
		self.FirstName = self.FirstName.title()
		# if self.MiddleName is not None:
		# 	self.MiddleName = self.MiddleName.title()
		self.LastName = self.LastName.title()
		self.City = self.City.title()
		self.State = self.State.upper()
		return super(imsData, self).save(*args, **kwargs)
