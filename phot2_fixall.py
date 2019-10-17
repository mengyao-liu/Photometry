import numpy as np
from astropy.io import fits
from astropy import wcs
from astropy import units as u
from astropy.coordinates import SkyCoord
from photutils import CircularAperture, aperture_photometry
import annulus_index

source = 'AFGL437'
lamda = [3.6,    4.5,    5.8,    7.7,    8. ,   19.7,   31.5,   37.1, 70. ,  160. ,  250. ,  350. ,  500.]
name = ['SPITZER_I1_6610176_0000_7_A42476568_maics','SPITZER_I2_6610176_0000_7_A42476183_maics','SPITZER_I3_6610176_0000_7_A42476607_maics','AFGL437_SOFIA_7.7um_cal_ast','SPITZER_I4_6610176_0000_7_A42476637_maics','AFGL437_SOFIA_19.7um_cal_ast','AFGL437_SOFIA_31.5um_cal_ast','AFGL437_SOFIA_37.1um_cal_ast','unimap_l140_blue_wglss_rcal','unimap_l140_red_wglss_rcal','unimap_l140_PSW_wglss_rcal','unimap_l140_PMW_wglss_rcal','unimap_l140_PLW_wglss_rcal']
aper = 32.



f = open('flux_adjacent_bgmedian_fixall.dat','w')
g = open('../Yichen RT Model/SEDfit/idl/data/'+source+'flux_fix_bgmedian_fixall.txt','w')
    
    
for i in np.arange(np.size(lamda)):  
    ra = 46.852292
    dec = 58.514656
    data, hdr = fits.getdata(name[i]+'.fits', 0, header = True)
    if i in (0,1,2,4):
        delt = abs(hdr['PXSCAL1'])/3600. 
    else:
        delt = abs(hdr['CDELT1'])
    r_pix = aper/delt/3600.
    w = wcs.WCS(hdr)
    if lamda[i]>=70.:
        coordiante = SkyCoord(ra*u.deg, dec*u.deg, frame='fk5')
        ra = coordiante.galactic.l.degree
        dec = coordiante.galactic.b.degree
    phot_center = w.wcs_world2pix(ra, dec, 1)
    aperture = CircularAperture(phot_center, r=r_pix)
    phot = aperture_photometry(data, aperture)

    # bg as median in an annulus
    grid = annulus_index.go([data.shape[1],data.shape[0]],phot_center,r_pix*2,r_pix)
    bgdata = np.ndarray(shape=data.shape)
    bgdata[:,:] = np.median(data[grid])   
    bgphot = aperture_photometry(bgdata, aperture) 
    if i in (3,5,6,7):
        flux = phot['aperture_sum'].data[0]
        bg = bgphot['aperture_sum'].data[0]
    else:
        flux = phot['aperture_sum'].data[0]*delt**2*304.61741978670857
        bg = bgphot['aperture_sum'].data[0]*delt**2*304.61741978670857
    
    print flux
    print bg
        
    
    print >> f,'%0.1f'%lamda[i],flux-bg,flux,'%0.2f'%aper
    print >> g,'%0.1f'%lamda[i],flux-bg,flux,'%0.2f'%aper
        
f.close()
g.close()
