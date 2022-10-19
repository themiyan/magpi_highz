import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import ascii
from astropy.table import Table
import glob
import argparse


parser = argparse.ArgumentParser(description='Input galaxy name')

parser.add_argument('gal_name', type=str)
args = parser.parse_args()

print('galaxy is', args)

gal_name = args.gal_name

LSD_cat_catalogue = ascii.read(f'/Users/wnanayakkara/Dropbox/MagPi/LSDCat_outputs_to_groups/v22/{gal_name}_LSDCat.cat',  
                              names=['I' , 'ID' , 'X_PEAK_SN' , 'Y_PEAK_SN' , 'Z_PEAK_SN' , 'NPIX' , 'DETSN_MAX' ])

class_files = glob.glob(f'/Users/wnanayakkara/Dropbox/MagPi/LSDCat_classifications/v22/{gal_name}*class.dat')
print(class_files)
assert len(class_files)==2, 'there are more or less than 2 files'


class_p1 = ascii.read(class_files[0], 
          names=['I' , 'ID' , 'X_PEAK_SN' , 'Y_PEAK_SN' , 'Z_PEAK_SN' , 'NPIX' , 'DETSN_MAX' , 'Galaxy'] ).to_pandas().set_index('I')


class_p2 = ascii.read(class_files[1], 
          names=['I' , 'ID' , 'X_PEAK_SN' , 'Y_PEAK_SN' , 'Z_PEAK_SN' , 'NPIX' , 'DETSN_MAX' , 'Galaxy'] ).to_pandas().set_index('I')


all_classifications = pd.merge(class_p1, class_p2, left_index=True, right_index=True, 
                               how='outer', suffixes=('_p1', '_p2'))

all_classification_grades =  all_classifications[['Galaxy_p1', 'Galaxy_p2']]#, 'Galaxy_p3']]

print('N of detections ',  len(all_classification_grades))

## all common between the group
all_common = all_classification_grades.query('Galaxy_p1==Galaxy_p2')
print('There are ', len(all_common), ' common classifications')


agreed = all_classification_grades.query('(Galaxy_p1==Galaxy_p2)')
# agreed = all_classification_grades.query('(Galaxy_p3==Galaxy_p2)  | (Galaxy_p3==Galaxy_p1) | (Galaxy_p1==Galaxy_p2)')

print(len(agreed), ' sources are agreeable out of ', len(all_classification_grades))

agreed['agreed_grade'] = agreed.mode(axis=1)


print('There are ', len(agreed.query('agreed_grade==3')), 'source/s which need revisiting from the agreed list because they are classified as maybe')


to_be_agreed = all_classification_grades[~all_classification_grades.index.isin(agreed.index)]

print(len(to_be_agreed), 'sources with two different classifications')


to_be_discussed = all_classifications.reindex(to_be_agreed.index)
## add the maybe ones
to_be_discussed = pd.concat([to_be_discussed, all_classifications.reindex(agreed.query('agreed_grade==3').index)])

LSD_inds = [np.where(index==LSD_cat_catalogue['I'])[0][0] for index in to_be_discussed.index  ]


LSD_cat_catalogue[LSD_inds].write(f'/Users/wnanayakkara/Dropbox/MagPi/LSDCat_classifications/v22/{gal_name}_combine_catalogue_to_be_consolidated.dat', 
                       format='ascii.fixed_width_no_header', delimiter=None, )


print('ALL DONE FOR ', gal_name)
