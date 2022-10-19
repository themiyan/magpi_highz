import numpy as np
import astropy.io.fits as pf
import lsdcat


def make_LSDmask(cube,segin,num,lsdcatDir,exp_map,N_exp):

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
    phdu.writeto(f'{lsdcatDir}/MAGPI{num}_LSDmask.fits')

    