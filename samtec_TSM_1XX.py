#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path

import argparse
from kicad_mod import KicadMod, createNumberedPadsSMD

parser = argparse.ArgumentParser()
parser.add_argument('pincount', help='number of pins of the jst connector', type=int, nargs=1)
parser.add_argument('-v', '--verbose', help='show extra information while generating the footprint', action='store_true') #TODO
args = parser.parse_args()

# http://www.jst-mfg.com/product/pdf/eng/eSH.pdf

pincount = int(args.pincount[0])

pad_spacing = 2.54
pad_separation = 2.3
pad_length = 2.8
pad_width = 1.4
start_pos_x = -(pincount-1)*pad_spacing/2.
end_pos_x = (pincount-1)*pad_spacing/2.

# SMT type shrouded header, Top entry type
footprint_name = 'TSM-1{pincount:02g}-DV_Pitch2.54mm_SMD'.format(pincount=pincount)

kicad_mod = KicadMod(footprint_name)
kicad_mod.setDescription("http://www.farnell.com/datasheets/2186767.pdf")
kicad_mod.setAttribute('smd')
kicad_mod.setTags('connector samtec pin header')

#kicad_mod.setCenterPos({'x':start_pos_x, 'y':pad_spacing+pad_separation})
kicad_mod.setCenterPos({'x':0, 'y':(pad_spacing+pad_separation)/2})

# set general values
kicad_mod.addText('reference', 'REF**', {'x':start_pos_x+1, 'y':-pad_length}, 'F.SilkS')
kicad_mod.addText('value', footprint_name, {'x':0, 'y':pad_separation+pad_length+2.3}, 'F.Fab')

##### create Silkscreen
kicad_mod.addRectLine(
	{'x':start_pos_x-pad_spacing/2, 'y':pad_separation+pad_length+1.5},
	{'x':end_pos_x+pad_spacing/2, 'y':-1.7},
	'F.SilkS', 0.12)

kicad_mod.addLine(
	{'x':start_pos_x-pad_spacing/2-.15, 'y':pad_separation+pad_length+1.5},
	{'x':start_pos_x-pad_spacing/2-.15, 'y':pad_separation/2+pad_length},
	'F.SilkS', 0.12)

kicad_mod.addRectLine(
	{'x':start_pos_x-pad_spacing/2, 'y':pad_separation+pad_length+1.5},
	{'x':end_pos_x+pad_spacing/2, 'y':-1.7},
	'F.Fab', 0.10)


##### create Courtyard
kicad_mod.addRectLine(
		{'x':start_pos_x-pad_spacing/2, 'y':pad_separation+pad_length+1.5},
		{'x':end_pos_x+pad_spacing/2, 'y':-1.7},
		'F.CrtYd', 0.05)

##### create pads
pad_structure = {'x': pad_width, 'y': pad_length}
createNumberedPadsSMD(kicad_mod, pincount, pad_spacing, pad_structure, 0, 1, 2)
createNumberedPadsSMD(kicad_mod, pincount, pad_spacing, pad_structure, pad_spacing+pad_separation, 0, 2)

##### output kicad model
print(kicad_mod)
