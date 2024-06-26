#!/usr/bin/env python

# Atomic units to kcal/mol
au2kcalmol    = 627.5095
# angstrom to bohr
a2b           = 1.8897268
# Bohr to Angstrom
b2a           = 0.529177
# Multipole conversion: Hartree and bohr to kcal/mol (332.064)
hbohr2kcalmol = 332.063595

# Some mathematical constants
sqrt_3      = 1.732050808

# Degrees to radian
deg2rad     = 0.017453292519943295

# au to debye
au2debye    = 2.541746231
debye2au    = 0.393430307

atomic_number = {
  'H'  : 1,
  'B'  : 5,
  'C'  : 6,
  'N'  : 7,
  'O'  : 8,
  'F'  : 9,
  'P'  :15,
  'S'  :16,
  'Cl' :17,
  'Br' :35,
  'I'  :53,
}

pol_free = {
  'H' :  4.50,
  'He':  1.38,
  'C' : 12.00,
  'N' :  7.40,
  'O' :  5.40,
  'F' :  3.80,
  'Ne':  2.67,
  'Si': 37.00,
  'P' : 25.00,
  'S' : 19.60,
  'Cl': 15.00,
  'Ar': 11.10,
  'Br': 20.00,
  'Kr': 16.80,
  'I' : 35.00,
}

csix_free  = {
  'H' :  6.50,
  'He':  1.46,
  'C' : 46.60,
  'N' : 24.20,
  'O' : 15.60,
  'F' :  9.52,
  'Ne':  6.38,
  'Si': 305.0,
  'P' : 185.0,
  'S' : 134.0,
  'Cl': 94.60,
  'Ar': 64.30,
  'Br': 162.0,
  'Kr': 130.0,
  'I' : 385.0,
}

rad_free = {
  'H' : 3.10,
  'He': 2.65,
  'C' : 3.59,
  'N' : 3.34,
  'O' : 3.19,
  'F' : 3.04,
  'Ne': 2.91,
  'Si': 4.20,
  'P' : 4.01,
  'S' : 3.86,
  'Cl': 3.71,
  'Ar': 3.55,
  'Br': 3.93,
  'Kr': 3.82,
  'I' : 4.39,
}

atomic_r2 = {
 'C': 14.046740332406095,
'Cl': 27.651441841502898,
 'F': 10.601441421661603,
 'H': 3.1589186627858976,
 'N': 12.419553635522538,
 'O': 11.566513469042524,
 'S': 29.17364957903178,
'Br':40.3810331885329
}


atomic_r4 = {
  'C':  109.39192409419,
 'Cl':  187.29318856137,
  'F':  41.707556384507,
  'H':  26.818416656404,
  'N':  71.475971390365,
  'O':  56.180301267329,
  'S': 239.014016575349,
 'Br': 288.05982633399606
}

atomic_weight = {
  'H'  : 1.008,
  'B'  : 10.81,
  'C'  : 12.01,
  'N'  : 14.01,
  'O'  : 16.00,
  'F'  : 19.00,
  'P'  : 31.00,
  'S'  : 32.06,
  'Cl' : 35.45,
  'Br' : 79.90,
  'I'  : 126.90,
}

# Covalent radii
cov_rad = {
    'H' : 0.31,
    'C' : 0.70,
    'N' : 0.71,
    'O' : 0.66,
    'F' : 0.57,
    'P' : 1.07,
    'S' : 1.05,
    'Cl': 1.02,
    'Br': 1.20,
    'I' : 1.39,
}

# Hbond interaction: Strength k_hbnd (according to Grimme)
k_hbnd = {
    'N' : 0.8,
    'O' : 0.3,
    'F' : 0.1,
    'P' : 2.0,
    'S' : 2.0,
    'Cl': 2.0,
    'Br': 2.0,
    'I' : 2.0,
}

# Map multipole coefficient to index
map_mtp_coeff = {
  'Q10'  : 2,
  'Q11c' : 0,
  'Q11s' : 1,
  'Q20'  : 0,
  'Q21c' : 1,
  'Q21s' : 2,
  'Q22c' : 3,
  'Q22s' : 4,
}

# Charge penetration
# Follows Wang et al. JCTC (2017) DOI: 10.1021/acs.jctc.5b00267
# effective core charge
cp_Z = {
  'H'  : 1,
  'B'  : 3,
  'C'  : 4,
  'N'  : 5,
  'O'  : 6,
  'F'  : 7,
  'P'  : 5,
  'S'  : 6,
  'Cl' : 7,
  'Br' : 7,
}

# valence-alpha set [Ang^-1]
cp_alpha = {
  'H'  : 2.0,
  'C'  : 4.0,
  'N'  : 5.0,
  'O'  : 6.0,
  'F'  : 7.0,
  'P'  : 5.0,
  'S'  : 6.0,
  'Cl' : 7.0,
  'Br' : 7.0,
}

# Free-atom valence widths [Bohr^-1]
val_width_free = {
    'H': 0.5094,
    'C': 0.5242,
    'N': 0.4415,
    'O': 0.3882,
}

# Free-atom valence charges
val_charge_free = {
    'H': -1.00000061,
    'C': -4.31910903,
    'N': -5.35306426,
    'O': -6.36289409,
}

ml_metric = {
    'gaussian': 'euclidean',
    'laplacian': 'cityblock'
}

ml_prefactor = {
    'gaussian': 2.0,
    'laplacian': 1.0
}

ml_power = {
    'gaussian': 2,
    'laplacian': 1
}

ml_chg_correct_error = {
    'H'  : 1.0,
    'C'  : 2.5145,
    'N'  : 3.2101,
    'O'  : 2.0108,
    'S'  : 5.108, 
    'Cl' : 2.703,
    'F'  : 1.138, 
    'Br'  : 1.138 
}

## Default damping parameters 
##for CP-corrected electrostatics
elst_cp_exp = {
'Cl'  : 3.44023059   ,
'F'   : 4.31571359   ,
'S1'  : 3.06183507   ,
'S2'  : 3.10344458   ,
'HS'  : 3.59744193   ,
'HC'  : 3.59818006   ,
'HN'  : 3.25541421   , 
'HO'  : 3.12549216   ,
'C4'  : 3.39104975   ,
'C3'  : 3.33249879   ,
'C2'  : 3.10571679   ,
'N3'  : 3.4371398    , 
'N2'  : 3.0371811    ,
'N1'  : 3.37851869   ,
'O1'  : 3.60313323   , 
'O2'  : 3.87600408   ,
'Br'  : 3.69423496  }

# Default short-range induction parameters
indu_sr_params = {
'Cl' : 0.846826917    , 
'F'  : 1.5280835      , 
'S1' : 0.986212886    , 
'S2' : 0.769937266    ,
'HS' : 0.603066647    ,
'HC' : 0.378052494    , 
'HN' : 0.595208067    , 
'HO' : 0.685558974    , 
'C4' : 2.11963996e-05 , 
'C3' : 0.284097106    , 
'C2' : 0.784309524    ,
'N3' : 1.75459668     , 
'N2' : 1.52105862     , 
'N1' : 0.813744201    , 
'O1' : 1.6371991      , 
'O2' : 1.14769962     , 
'Br' : 1.16121111  
}

exch_int_params = {
'Cl'  :  3.8151908   , 
'F'   :  7.60360362  , 
'S1'  :  3.17730052  , 
'S2'  :  3.28418743  ,
'HS'  :  0.790918621 ,
'HC'  :  0.989040149 , 
'HN'  :  0.69099863  , 
'HO'  :  0.599608839 , 
'C4'  :  2.26488385  , 
'C3'  :  2.45658457  , 
'C2'  :  2.80231434  ,
'N3'  :  4.46603838  , 
'N2'  :  4.62514186  , 
'N1'  :  3.48963039  , 
'O1'  :  5.34349334  , 
'O2'  :  5.85377182  ,
'Br'  :  4.10079141
}

disp_coeffs = {
'Cl'  : 0.628936576 , 
'F'   : 0.593460843 , 
'S1'  : 0.724969324 , 
'S2'  : 0.689804317 ,
'HS'  : 4.25713031e-06,
'HC'  : 0.161948995 , 
'HN'  : 0.142004497 , 
'HO'  : 8.03872825e-07, 
'C4'  : 0.348912752 , 
'C3'  : 0.380138542 , 
'C2'  : 0.474737451 ,
'N3'  : 0.251517245 , 
'N2'  : 0.921337229 , 
'N1'  : 0.814292607 , 
'O1'  : 0.779432259 , 
'O2'  : 0.547957036 , 
'Br'  : 0.499319918
}


# Default smearing coefficient for induction (Thole model)
indu_smearing_coeff = 0.38539063 


