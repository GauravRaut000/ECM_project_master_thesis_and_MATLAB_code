#!/usr/bin/env python
# coding: utf-8

# In[11]:


"""
Information about giving parameters to elemnts:

series(Element1,Element2,Parallel_Elements,.......)
parallel(Element1,Element2,series_Elements,.......)

R(r) = R(Resistance) 

C(c, f) = C(capacitance of the capacitor, frequency)
P(q,a_p,f) = P(The admittance value,The exponential facto, frequency)
L(l, f) = L(inductance of the inductor, frequency)

W(Aw,f) = Wo(Warburg coefficient,frequency)
Wo(zw,tau,a_wo,f) = Wo(Warburg coefficient,time-constant parameter,exponential parameter,frequency)
Ws(zw,tau,a_ws,f) = Ws(Warburg coefficient,time-constant parameter,exponential parameter,frequency)

G(y,k,f) = G(admittance parameter,rate-constant parameter,frequency)
""" 

########################################################################################
################# define libraries and functions to import #############################
########################################################################################

from datetime import datetime
start_time = datetime.now()

import numpy as np
from ECM_Elements_functions import series,parallel,R,P,L,Ws,G
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib as mpl
import gc
from matplotlib.backends.backend_pdf import PdfPages
plt.rcParams.update({'font.size': 7})
mpl.rcParams['axes.formatter.useoffset'] = False
from itertools import combinations_with_replacement

########################################################################################
################# define ECM name and parameters ranges ################################
########################################################################################
"""
# Parameters of resistance R
r = np.logspace(-3,0,num=4)   # :.0E

# Parameters of Inductance
l = np.logspace(-9,-5,num=5)     # :.0E

# Parameters of CPE
q = np.logspace(-6,3,num=10)     # :.0E
ap = np.linspace(0.5,1.0,num=6)  # no need to format

# Parameters of FINITE WARBURG-IMPEDANCE (SHORT)
zw = np.logspace(-3,0,num=4)        # :.0E
tau = np.logspace(-3,1,num=5)       # :.0E
aw = np.linspace(0.5,1.0,num=6)     # no need to format

# Parameters of GERISCHER-ELEMENT
y = np.logspace(0,3,num=4)   # :.0E
k = np.linspace(0,1,num=11)  # :.1f
"""

## define ECM name
ECM="R1P1_R2P2_R3P3"

## Parameter of R1,R2,R3
r = np.logspace(-3,0,num=4)   # :.0E

## Parameters of P1,P2,P3
q = np.logspace(-6,3,num=5)     # :.0E
ap = np.linspace(0.5,1.0,num=6)  # no need to format

########################################################################################
####################### define frquency range for simulation ###########################
########################################################################################

freq =  np.logspace(-2.0, 6.0, num=241)

########################################################################################
####################### define structure of file to export Nyquist data ################
########################################################################################
# to create empty matrix
data = [[ '' for col in range(3)] for rows in range(len(freq)+4)]

# to write titles in third row
data[2][0]="Frequency"
data[2][1]="Z'"
data[2][2]="Z''"

# to write units in fourth row
data[3][0]="Hz"
data[3][1]="Ω"
data[3][2]="Ω"


a=b=c=d=e=f=g=h=i=j=k=l=m=n=ii=jj=0 # intializing indices for looping


##########################################################################################
###### Number of for loops = (number of parameters + 1)-->last loop is for frequency######
##########################################################################################

for set_r in combinations_with_replacement(r, 3):
    for set_q in combinations_with_replacement(q, 3):
        for set_ap in combinations_with_replacement(ap, 3):
                            for n in range(len(freq)):                               
                                                        ## element definition by giving parameters
                                                        #R1=R(r1[aaa])
                                                        #L1=L(l1[aaa],freq[n])
                                                        #P1=P(q1[aaa],ap1[aaa],freq[n])
                                                        #Ws1=Ws(zw1[aaa],tau1[aaa],aw1[k],freq[n])
                                                        #G1= G(y1[aaa],k1[aaa],freq[n])
                                                        
                                                        R1=R(set_r[0])
                                                        P1=P(set_q[0],set_ap[0],freq[n])
                                                        
                                                        R2=R(set_r[1])
                                                        P2=P(set_q[1],set_ap[1],freq[n])
                                                        
                                                        R3=R(set_r[2])
                                                        P3=P(set_q[2],set_ap[2],freq[n])
                                                                                                                
                                                        ## circuit definition
                                                        z = series(parallel(R1,P1),parallel(R2,P2),parallel(R3,P3))
                                                        
                                                        # to store the coloumns in matrix
                                                        data[ii+4][0] = freq[n]
                                                        data[ii+4][1] = z.real
                                                        data[ii+4][2] = z.imag
                                                        
                                                        
                                                        ii=ii+1  #this is counter to increase frequency
                                                                                                               
                            jj = jj+1   # jj is used to count number of files or number of variation in models 
                                                    
                            # to write the ECM name in first cell along with number
                            data[0][0]=f'{jj}_{ECM}'

                            ## to name the file with parameters
                            parameters_details =  f'r1_{set_r[0]:.0E}_q1_{set_q[0]:.0E}_ap1_{set_ap[0]}_r2_{set_r[1]:.0E}_q2_{set_q[1]:.0E}_ap2_{set_ap[1]}_r3_{set_r[2]:.0E}_q3_{set_q[2]:.0E}_ap3_{set_ap[2]}'
                                                    
                            # to write the parameters' details in the file in second row
                            data[1][0]=parameters_details
                            NyquistData = pd.DataFrame(data)
                                                                                                         
                            # exporting file with Nyquist plot
                            NyquistData.to_csv(f'Nyquist\\{jj}_{ECM}_{parameters_details}.txt', header=None, index=None, sep='\t')
                      
                            ii = 0
                            gc.collect()
                            

end_time = datetime.now()
print(' Execution is complete \n Duration: {}'.format(end_time - start_time))


# In[ ]:




