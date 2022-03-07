# This script will work only in django shell

import pandas as pd
from sponsorApp.models import Country as cnt # Import model
from sponsorApp.models import State as st # Import model
from sponsorApp.models import City as ct # Import model
from sponsorApp.models import County as c # Import model
from sponsorApp.models import ZipCode as zc # Import model
from sponsorApp.models import LocationData as ld
fl = 'C:\\MandirProject\\SponsorProject\\LocationData\\FinalLocationData.xlsx'
dfAl = pd.DataFrame(pd.read_excel(fl, sheet_name='US_IN_Location'))
dfCnt = pd.DataFrame(pd.read_excel(fl, sheet_name='Country'))
dfSt = pd.DataFrame(pd.read_excel(fl, sheet_name='State'))
ctList = []
cntList = []
stList = []
zcList = []
cnt.objects.all().delete()
st.objects.all().delete()
ct.objects.all().delete()
c.objects.all().delete()
zc.objects.all().delete()
for i, v in dfCnt[dfCnt.Country.eq('US')].iterrows():
    cnt1 = cnt(CountryName=v['Country'])
    cnt1.save()
    print(v['Country'])
    x = 1
    for i1, v1 in dfSt[dfSt.Country.eq(v['Country'])].iterrows():
        ctList.clear()
        cntList.clear()
        stList.clear()
        zcList.clear()
        st1 = st(StateName=v1['State'], StateAbbr=v1['StateAbbr'], CountryName=cnt1)
        st1.save()
        print(x)
        print(v1['State'])
        x = 1
        for i2, v2 in dfAl[(dfAl.Country==v['Country']) & (dfAl.State==v1['State'])].iterrows():
            if v2['City'] not in ctList:
                ctList.append(v2['City'])
                ct1 = ct(City=v2['City'], StateName=st1)
                ct1.save()
                c1 = c(CountyName=v2['County'], City=ct1)
                c1.save()
                x += 1
                for i3, v3 in dfAl[(dfAl.Country==v['Country']) & (dfAl.State==v1['State']) & (dfAl.City==v2['City'])].iterrows():
                    if v3['ZipCode'] not in zcList:
                        zc1 = zc(ZipCode=v3['ZipCode'], City=ct1)
                        zc1.save()
                        ld1 = ld(Country=v['Country'], StateAbbr=v1['StateAbbr'], StateName=v1['State'], City=ct1, CountyName=v2['County'], ZipCode=v3['ZipCode'])
                        ld1.save()
                        zcList.append(v3['ZipCode'])

#Purpose Code
# iterat throug excel data and update it to model
import pandas as pd
from sponsorApp.models import PurposeCode as pc # Import model
from sponsorApp.models import Purpose as p # Import model
from sponsorApp.models import DisplayPurpose as dp # Import modelPurposeIndex
from sponsorApp.models import PurposeIndex as pi # Import model
from sponsorApp.models import purposeData as ppd # Import model
fl = 'C:\\MandirProject\\venv\Purpose\\Purpose.xlsx'
dfP = pd.DataFrame(pd.read_excel(fl, sheet_name='Purpose'))
pList = []
pc.objects.all().delete()
p.objects.all().delete()
pi.objects.all().delete()
dp.objects.all().delete()
ppd.objects.all().delete()
for i, v in dfP.iterrows():
    pd1 = ppd(Purpose=v['Purpose'], Purpose_Code=v['Purpose_Code'], Purpose_Index=v['Index'], DisplayOnPPT=v['DisplayOnPPT'], AnnounceAs=v['AnnounceAs'])
    pd1.save()
    pc1 = pc(Purpose_Code=v['Purpose_Code'])
    pc1.save()
    for i1, v1 in dfP[dfP.Purpose_Code==v['Purpose_Code']].iterrows():
        p1 = p(Purpose=v1['Purpose'], Purpose_Code=pc1)
        p1.save()
        dp1 = dp(DisplayPurpose=v1['DisplayOnPPT'], Purpose_Code=pc1)
        dp1.save()
        pi1 = pi(Purpose_Index=v1['Index'], Purpose_Code=pc1)
        pi1.save()