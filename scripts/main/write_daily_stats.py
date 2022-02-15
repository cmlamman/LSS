import fitsio
import datetime
import os

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--add", help="whether or not to add to the tracking file",default='n')
args = parser.parse_args()

today = datetime.date.today()

fn = 'temp.txt'
if args.add == 'y':
    fn = '/global/cfs/cdirs/desi/survey/catalogs/main/LSS/daily/LSScats/stats.txt'
   

if os.path.isfile(fn):
    fo = open(fn,'a')
else:
    fo = open(fn,'w')

fo.write('#####################\n')
fo.write('as of '+today.strftime("%B %d, %Y")+'\n')
fo.write('#####################\n')

tps = ['QSO','LRG','ELG','ELG_LOP','ELG_LOPnotqso','BGS_ANY','BGS_BRIGHT']

zcol = 'Z_not4clus'
for tp in tps:
    rt = fitsio.read_header('/global/cfs/cdirs/desi/survey/catalogs/main/LSS/daily/LSScats/test/'+tp+'zdone_1_full.ran.fits',ext=1)
    area = rt['NAXIS2']/2500
    dt = fitsio.read('/global/cfs/cdirs/desi/survey/catalogs/main/LSS/daily/LSScats/test/'+tp+'zdone_full.dat.fits')
    #wz = dt[zcol]*0 == 0
    #wz &= dt[zcol] != 999999
    wz = dt['ZWARN']*0 == 0
    wz &= dt['ZWARN'] != 1.e20
    wz &= dt['ZWARN'] != 999999
    wz &= dt['LOCATION_ASSIGNED'] == 1

    if tp == 'QSO':
        #good redshifts are currently just the ones that should have been defined in the QSO file when merged in full
        wg = dt[zcol]*0 == 0
        wg &= dt[zcol] != 999999
        wg &= dt[zcol] != 1.e20
    
    if tp[:3] == 'ELG':
        wg = dt['o2c'] > 0.9

    if tp == 'LRG':
        # Custom DELTACHI2 vs z cut from Rongpu
        wg = dt['ZWARN'] == 0
        drz = (10**(3 - 3.5*dt[zcol]))
        mask_bad = (drz>30) & (dt['DELTACHI2']<30)
        mask_bad |= (drz<30) & (dt['DELTACHI2']<drz)
        mask_bad |= (dt['DELTACHI2']<10)
        wg &= dt[zcol]<1.4
        wg &= (~mask_bad)


    if tp[:3] == 'BGS':
        wg = dt['DELTACHI2'] > 40
    fo.write(tp+':\n')
    fo.write('area: '+str(area)+'\n')
    fo.write('# of good z: '+str(len(dt[wz&wg]))+'\n')
    fo.write('completeness: '+str(round(len(dt[wz])/len(dt),3))+'\n')