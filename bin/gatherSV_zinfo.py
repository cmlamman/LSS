'''
gather redshift info across all observations for a given target type; for now from a single tile
'''

#standard python
import sys
import os
import shutil
import unittest
from datetime import datetime
import json
import numpy as np
import fitsio
import glob
import argparse
from astropy.table import Table,join,unique,vstack
from matplotlib import pyplot as plt


parser = argparse.ArgumentParser()
parser.add_argument("--type", help="tracer type to be selected")
parser.add_argument("--tile", help="observed tile to use") #eventually remove this and just gather everything
args = parser.parse_args()
type = args.type
tile = args.tile


if type == 'LRG':
    tarbit = 0 #targeting bit
if type == 'QSO':
    tarbit = 2
if type == 'ELG':
    tarbit = 1

print('gathering type,tile')
print(type,tile)
tp = 'SV1_DESI_TARGET'
print('targeting bit,  target program type; CHECK THEY ARE CORRECT!')
print(tarbit,tp)

#location of inputs
coaddir = '/global/cfs/cdirs/desi/spectro/redux/blanc/tiles/'+tile
subsets = [x[0][len(coaddir):].strip('/') for x in os.walk(coaddir)] #something must work better than this, but for now...


#outputs
svdir = '/project/projectdirs/desi/users/ajross/catalogs/SV/'
version = 'test/'
dirout = svdir+'redshift_comps/'+version
outf = dirout +'/'+tile+'_'+type+'zinfo.fits'

if not os.path.exists(svdir+'redshift_comps'):
    os.mkdir(svdir+'redshift_comps')
    print('made '+svdir+'redshift_comps random directory')

if not os.path.exists(dirout):
    os.mkdir(dirout)
    print('made '+dirout)
  
expf = '/global/cfs/cdirs/desi/users/raichoor/fiberassign-sv1/sv1-exposures.fits'  
exposures = fitsio.read(expf) #this will be used in depth calculations    

ss = 0 #use to switch from creating to concatenating
for night in subsets:
    if len(night) > 0:
        print('going through subset '+night)
        specs = []
        #find out which spectrograph have data
        for si in range(0,10):
            try:
                fl = coaddir+'/'+night+'/zbest-'+str(si)+'-'+str(tile)+'-'+night+'.fits'
                #print(fl)
                fitsio.read(fl)
                specs.append(si)
            except:
                print('no spectrograph '+str(si)+ ' on subset '+night)
        tspec = Table.read(coaddir+'/'+night+'/zbest-'+str(specs[0])+'-'+str(tile)+'-'+night+'.fits',hdu='ZBEST')
        #this is all to get the effective coadded exposure depth; should eventually just be in the fibermap hdu
        zfm = Table.read(coaddir+'/'+night+'/zbest-'+str(specs[0])+'-'+str(tile)+'-'+night+'.fits',hdu='FIBERMAP')
        exps = np.unique(zfm['EXPID'])
        bd = []
        rd = []
        zd = []
        for exp in exps:
            info = exposures[exposures['EXPID'] == exp]
            bd.append(info['B_DEPTH'][0])
            rd.append(info['R_DEPTH'][0])
            zd.append(info['Z_DEPTH'][0])        
        bdt = np.zeros(500)
        rdt = np.zeros(500)
        zdt = np.zeros(500)
        for i in range(0,len(exps)):
            sel = zfm[i*500:(i+1)*500]
            w = sel['FIBERSTATUS'] == 0
            bdt[w] += bd[i]
            rdt[w] += rd[i]
            zdt[w] += zd[i]
        tf = Table.read(coaddir+'/'+night+'/coadd-'+str(specs[0])+'-'+str(tile)+'-'+night+'.fits',hdu='FIBERMAP')
        for i in range(1,len(specs)):
            tn = Table.read(coaddir+'/'+night+'/zbest-'+str(specs[i])+'-'+str(tile)+'-'+night+'.fits',hdu='ZBEST')
            tspec = vstack([tspec,tn])
            
            zfm = Table.read(coaddir+'/'+night+'/zbest-'+str(specs[i])+'-'+str(tile)+'-'+night+'.fits',hdu='FIBERMAP')
            exps = np.unique(zfm['EXPID'])
            bd = []
            rd = []
            zd = []
            for exp in exps:
                info = exposures[exposures['EXPID'] == exp]
                bd.append(info['B_DEPTH'][0])
                rd.append(info['R_DEPTH'][0])
                zd.append(info['Z_DEPTH'][0])        
            bdtn = np.zeros(500)
            rdtn = np.zeros(500)
            zdtn = np.zeros(500)
            for i in range(0,len(exps)):
                sel = zfm[i*500:(i+1)*500]
                w = sel['FIBERSTATUS'] == 0
                bdtn[w] += bd[i]
                rdtn[w] += rd[i]
                zdtn[w] += zd[i]
            bdt = np.concatenate([bdt,bdtn])
            rdt = np.concatenate([rdt,rdtn])
            zdt = np.concatenate([zdt,zdtn])    
            
            tnf = Table.read(coaddir+'/'+night+'/coadd-'+str(specs[i])+'-'+str(tile)+'-'+night+'.fits',hdu='FIBERMAP')            
            tf = vstack([tf,tnf])

        tspec = join(tspec,tf,keys=['TARGETID'])
        tspec['B_DEPTH'] = bdt
        tspec['R_DEPTH'] = rdt
        tspec['Z_DEPTH'] = zdt
        
        wtype = ((tspec[tp] & 2**tarbit) > 0)
        print(str(len(tspec))+' total entries '+str(len(tspec[wtype]))+' that are '+type)
        tspec = tspec[wtype]
        tspec['subset'] = night
        if ss == 0:
            tspect = tspec
            ss = 1
        else:
            tspect = vstack([tspect,tspec])
        print('there are now '+str(len(tspect)) +' entries with '+str(len(np.unique(tspect['TARGETID'])))+' unique target IDs')    

tspect.sort('TARGETID')
tspect.write(outf,format='fits', overwrite=True) 
print('wrote to '+outf)
        

