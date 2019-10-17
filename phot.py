# order as in d.xls

import radialProfile
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import glob
from photutils import CircularAperture, aperture_photometry
import annulus_index

lam = '70'
num,xx,yy = np.loadtxt('target.txt',unpack=True)
#images = glob.glob('*.fits')
i = 0
f = open('photauto.txt','w')
for i in np.arange(len(num)):
    if num[i]<100:
        str_num = '0'+str(int(num[i]))
    else:
        str_num = str(int(num[i]))
    data, hdr = fits.getdata('destripe_l'+str_num+'_blue_wgls_rcal.fits', 0, header = True)
    delt = abs(hdr['CDELT1'])
    a = radialProfile.azimuthalAverage(data,center=[int(xx[i]),int(yy[i])])
    grid = annulus_index.go([data.shape[1],data.shape[0]],[int(xx[i]),int(yy[i])],25,10)
    bg = np.median(data[grid]) 


    if np.size(np.where(a-bg<0.1*(np.max(a[0:5])-bg))) == 0:
        print >> f, str_num, 'none'
        continue
    radius = np.min([ np.where(a-bg<0.1*(np.max(a[0:5])-bg))[0][0], np.where(a<=2*bg)[0][0] ])
    print radius,radius*abs(hdr['CDELT1'])*3600.
    
    position = (int(xx[i]),int(yy[i]))
    aperture = CircularAperture(position, r=radius)
    phot = aperture_photometry(data, aperture)
    print phot['aperture_sum'].data[0]
    
    
    print >> f,radius,radius*delt*3600.,(phot['aperture_sum'].data[0]-bg*np.pi*radius**2)*delt**2*304.61741978670857,bg*np.pi*radius**2*delt**2*304.61741978670857
    plt.plot(a[0:40]-bg)
    plt.savefig('radial_profile/'+str_num+'radial'+lam+'.eps')
    plt.clf()
    
    

    
    
f.close()
