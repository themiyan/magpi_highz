import numpy as np
import astropy.io.fits as pf

def make_LSDmask(cube,segin,num,exp_map,N_exp):

    d = pf.open(cube)
    d = d[2].data

    d= d[1600:1680,:,:]
    d = np.nansum(d,axis=0)

    smap = pf.open(segin)
    smap = smap[0].data

    out = np.ones((d.shape[0],d.shape[1]))
    r,c = np.where((smap != 0)|(d == 0))
    out[r,c] = 0


    emap = pf.open(exp_map)
    emap = emap[0].data

    out[emap<N_exp] = 0

    phdu = pf.PrimaryHDU(out)
    phdu.writeto(f'MAGPI{num}_LSDmask.fits')

    
if __name__ == '__main__':

    N_exp = 3 # minmum number of exposures needed to be used for LSDCat
    gal = '1206'
    cube = f'../data/v22/MAGPI{gal}.fits'
    exp_map = f'../data/v22/MAGPI{gal}_exposure_map.fits'
    seg = f'../data/v22/MAGPI{gal}_manual_segmap.fits'

    make_LSDmask(cube,seg,gal, exp_map, N_exp)
