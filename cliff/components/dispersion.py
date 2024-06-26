#!/usr/bin/env python
#

#from cliff.atomic_properties.polarizability import Polarizability, cutoff
from functools import reduce
import operator
import numpy as np
import cliff.helpers.constants as constants
import math
import logging


class Dispersion():
    'Dispersion class. Computes many-body dispersion'

    def __init__(self, options, _system, cell):
        # Set logger
        self.logger = options.logger 

        self.method = options.disp_method
        self.systems = [_system]
        self.energy = 0.0
        self.cell = cell
        self.radius = options.disp_radius
        self.beta = options.disp_beta
        self.scs_cutoff = options.pol_scs_cutoff
        self.pol_exponent = options.pol_exponent
        self.disp_coeffs = options.disp_coeffs

        self.decompose = True
        self.at_disp = np.zeros((0,0))

    def add_system(self, sys):
        self.systems.append(sys)
        
    def compute_dispersion(self, hirsh=None):

        # Driver for dispersion computations
        if self.method == "TT":
            
            disp = self.compute_tang_toennies()

            return disp * constants.au2kcalmol
            
    def compute_tang_toennies(self):
        '''
        Computes total dispersion energy using Tang-Toennies damping.
        Uses prefactor from Van Vleet 2018
        '''        
        # assume two systems
        sys_i = self.systems[0]                    
        sys_j = self.systems[1]                    

        # compute c coefficients
        c6_ab = self.compute_c6_coeffs()
        c8_ab = self.compute_c8_coeffs(c6_ab)
        c10_ab = self.compute_c10_coeffs(c6_ab, c8_ab)

       # print("Types ", sys_i.atom_types + sys_j.atom_types)

        if self.decompose:
            self.at_disp = np.zeros((len(sys_i.atom_types), len(sys_j.atom_types)))

        disp = 0.0
        for A, ele_A in enumerate(sys_i.atom_types):
            # valence decay rates
            b_A = 1.0 / (sys_i.valence_widths[A])
            for B, ele_B in enumerate(sys_j.atom_types):
                b_B = 1.0/(sys_j.valence_widths[B])

                # get interatomic distance
                coord_A = sys_i.coords[A]
                coord_B = sys_j.coords[B]
                vec = self.cell.pbc_distance(coord_A,coord_B) * constants.a2b
                rAB = np.linalg.norm(vec)

                # use combining rule
                b_AB = np.sqrt(b_A*b_B)
                
                f6 = self.compute_tt_damping(6, rAB, b_AB)
                f8 = self.compute_tt_damping(8, rAB, b_AB)
                f10 = self.compute_tt_damping(10, rAB, b_AB)

                en  = -1.0* f6*c6_ab[A][B]/(rAB**6.0) 
                en -= (f8*c8_ab[A][B]/(rAB**8.0) + f10*c10_ab[A][B]/(rAB**10.0)) * self.disp_coeffs[ele_A]*self.disp_coeffs[ele_B]

                disp += en

                if self.decompose:
                    self.at_disp[A,B] = en*constants.au2kcalmol
        
        

               # print(ele_A,ele_B, f6*c6_ab[A][B]/(rAB**6.0), (f8*c8_ab[A][B]/(rAB**8.0) + f10*c10_ab[A][B]/(rAB**10.0)))

        return disp


    def compute_tt_damping(self, n, rAB, b_AB):
        '''
        Computes Tang--Toennies damping for dispersion, thanks to MVV
        
        @params:
        
        n: Order of damping funcion, usually 6 or 8
    
        rab: The interatomic distance in au

        b_AB: the Bab parameter, computed as square root of product of
              the inverse of the valence widths for atoms A and B

        '''
        # compute x
        b2 = b_AB*b_AB

        x = b_AB*rAB - ((2.0*b2*rAB + 3*b_AB)*rAB / (b2*rAB*rAB + 3.0*b_AB*rAB + 3.0))

        # Compute damping function
        x_sum = 1.0
        # so far we are hard-coding use of C6 and C8 only
        for k in range(1, n+1):
            x_sum += (x**k)/math.factorial(k)

        return 1.0 - np.exp(-x)*x_sum


    def compute_c6_coeffs(self):

        nsys = len(self.systems)

        if nsys <= 1:
            raise Exception("Need at least two monomers")
        
        # assume two systems
        sys_i = self.systems[0]                    
        sys_j = self.systems[1]                    

        C6_AB = np.zeros([len(sys_i.elements), len(sys_j.elements)])

        # hirshfeld ratios
        hi = sys_i.hirshfeld_ratios
        hj = sys_j.hirshfeld_ratios

        for A,ele_A in enumerate(sys_i.elements):
            # get effective C6s from free-atom C6s
            c6_AA = constants.csix_free[ele_A]*hi[A]*hi[A]

            # get effective atomic polarizabilities
            a_A = hi[A] * constants.pol_free[ele_A]

            for B,ele_B in enumerate(sys_j.elements):
                c6_BB = constants.csix_free[ele_B]*hj[B]*hj[B]
                a_B = hj[B] * constants.pol_free[ele_B]
                
                C6_AB[A][B] = (2.0 * c6_AA * c6_BB) / ((a_B/a_A)*c6_AA + (a_A/a_B)*c6_BB)

        return C6_AB

    def compute_c8_coeffs(self, C6_AB):
        '''
        Computes C8 coefficients using the Starkschall recursion relation
        '''

        # 1. First copy the C6s in the C8s
        C8_AB = np.copy(C6_AB)

        # 2. Grab systems
        sys_i = self.systems[0]                    
        sys_j = self.systems[1]                    
        hi = sys_i.hirshfeld_ratios
        hj = sys_j.hirshfeld_ratios
        
        for A, ele_A in enumerate(sys_i.elements):
            # 3. For each atom, get free-atom  <r2> and <r4>
            r2_A = constants.atomic_r2[ele_A]
            r4_A = constants.atomic_r4[ele_A]
            r42A = r4_A / r2_A
            for B, ele_B in enumerate(sys_j.elements):
                # 3. For each atom, get free-atom  <r2> and <r4>
                r2_B = constants.atomic_r2[ele_B] 
                r4_B = constants.atomic_r4[ele_B]
                r42B = r4_B / r2_B
            
                # 4. Compute C8
                
                #C8_AB[A][B] *= (3.0/2.0) * (r42A + r42B) * self.scale8
        
                # from grimme:
                qa = math.sqrt(constants.atomic_number[ele_A]) * r42A
                qb = math.sqrt(constants.atomic_number[ele_B]) * r42B
                C8_AB[A][B] *= 3*math.sqrt(qa*qb)
        
                #C8_AB[A][B] *= 1.5 * math.sqrt(r42A + r42B) * self.scale8
                #C8_AB[A][B] *= 1.5 * (r42A + r42B) * self.scale8

                # Note: The above expression was derived from Starckschall and Gordon (1972)
                #       MEDFF uses a similar expression, but with the sum of the r42 terms
                #       with in a square root, not sure why. 
        return C8_AB


    def compute_c10_coeffs(self, C6_AB, C8_AB):

        # C10 coefficients are computed with the recursion relation:
        #
        #   C10 = (49/40) * C8^2 / C6

        C10_AB = np.copy(np.square(C8_AB))
        C10_AB = np.divide(C10_AB,C6_AB)
        C10_AB = np.multiply(C10_AB, (49.0/40.0))

        return C10_AB
