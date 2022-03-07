# This script will work only in django shell

import pandas as pd
from imsApp.models import imsData as id # Import model
fl = 'C:\\MandirProject\\SponsorProject\\IMS_Data\\July2019.xlsx'
dfID = pd.DataFrame(pd.read_excel(fl, sheet_name='IMS'))
id.objects.all().delete()
for i, v in dfID.iterrows():
    id1 = id(MemberID=v['MemberID'],FirstName=v['FirstName'],MiddleName=v['MiddleName'],
    LastName=v['LastName'],SpouseFirstName=v['SpouseFirstName'],AddressLine1=v['AddressLine1'],
    AddressLine2=v['AddressLine2'],City=v['City'],State=v['State'],Zipcode=v['Zipcode'],
    SatsangCategory=v['SatsangCategory'],Mandal=v['Mandal'],Relation=v['Relation'],
    SatsangReference=v['SatsangReference'],NativePlace=v['NativePlace'],NativeCountry=v['NativeCountry'],
    ZoneName=v['ZoneName'],OtherAppPersonID=v['OtherAppPersonID'],PrimaryCellPhone=v['PrimaryCellPhone'],
    PrimaryHomePhone=v['PrimaryHomePhone'],PrimaryEmail=v['PrimaryEmail'],Gender=v['Gender'],
    Karyakar=v['Karyakar'],Volunteer=v['Volunteer'],GraduationYear=v['GraduationYear'],
    Remarks=v['Remarks'],Language=v['Language'])
    id1.save()