#!/usr/bin/env python
# coding: utf-8

# In[5]:


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
import os

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

empty_dict = [{},{},{}]


path="C:\\Users\\g.raut\\Desktop\\Python files\\00_Model_Datasources\\005_RP_RP_RP\\"
entries = os.listdir(path+"Nyquist\\")

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
                                                                                                               
                            jj = jj+1   # jj is used to count number of files or number of variation in models 
                                                    
                            # to write the ECM name in first cell along with number
                            data[0][0]=f'{jj}_{ECM}'

                            ## to name the file with parameters
                            parameters_details =  f'r1_{set_r[0]:.0E}_q1_{set_q[0]:.0E}_ap1_{set_ap[0]}_r2_{set_r[1]:.0E}_q2_{set_q[1]:.0E}_ap2_{set_ap[1]}_r3_{set_r[2]:.0E}_q3_{set_q[2]:.0E}_ap3_{set_ap[2]}'
                                                    
                            # importing Nyquist file with respect to current parameters details
                            for filename in entries:
                                if parameters_details in filename:
                                    ImportName=filename
                                    break
                                    
                            NyquistData = pd.read_csv(path+"Nyquist\\"+ImportName, header=None, sep='\t')
                            
                            DRT1 = pd.read_csv(path+"DRT_E_-2\\DRT_E_-2\\"+ImportName, header=0, sep='\t')
                            DRT2 = pd.read_csv(path+"DRT_E_-3\\DRT_E_-3\\"+ImportName, header=0, sep='\t')
                            DRT3 = pd.read_csv(path+"DRT_E_-4\\DRT_E_-4\\"+ImportName, header=0, sep='\t')
                            DRT4 = pd.read_csv(path+"DRT_E_-5\\DRT_E_-5\\"+ImportName, header=0, sep='\t')
                            DRT5 = pd.read_csv(path+"DRT_E_-6\\DRT_E_-6\\"+ImportName, header=0, sep='\t')
                            DRT6 = pd.read_csv(path+"DRT_E_-7\\DRT_E_-7\\"+ImportName, header=0, sep='\t')
                            
                            DRT1 = pd.DataFrame(empty_dict).append(DRT1, ignore_index=True, sort=False)
                            DRT2 = pd.DataFrame(empty_dict).append(DRT2, ignore_index=True, sort=False)
                            DRT3 = pd.DataFrame(empty_dict).append(DRT3, ignore_index=True, sort=False)
                            DRT4 = pd.DataFrame(empty_dict).append(DRT4, ignore_index=True, sort=False)
                            DRT5 = pd.DataFrame(empty_dict).append(DRT5, ignore_index=True, sort=False)
                            DRT6 = pd.DataFrame(empty_dict).append(DRT6, ignore_index=True, sort=False)
                                                       
                           
                            Joined_data = pd.concat([NyquistData,DRT1,DRT2,DRT3,DRT4,DRT5,DRT6], axis=1, ignore_index=True)
                                                        
                            # exporting joined data
                            Joined_data.to_csv(f'Nyquist+DRT\\{jj}_{ECM}_{parameters_details}.txt', header=None, index=None, sep='\t')

                            #"""
                            ########### code for ploting and exporting pdf starts here###########
                            
                            # to plot Nyquist graph
                            Joined_data_numeric = Joined_data.iloc[4:,:]
                            Joined_data_numeric = Joined_data_numeric.apply(pd.to_numeric,errors='ignore')
                            
                            plt.ioff() #to turn off interactive mode
                            
                            #to convert relaxation time into frequency
                            freq1_array = np.reciprocal(Joined_data_numeric.iloc[0:750,3])
                            freq2_array = np.reciprocal(Joined_data_numeric.iloc[0:750,5])
                            freq3_array = np.reciprocal(Joined_data_numeric.iloc[0:750,7])
                            freq4_array = np.reciprocal(Joined_data_numeric.iloc[0:750,9])
                            freq5_array = np.reciprocal(Joined_data_numeric.iloc[0:750,11])
                            freq6_array = np.reciprocal(Joined_data_numeric.iloc[0:750,13])
                            
                            with PdfPages(f"Results\\{jj}_{ECM}_{parameters_details}.pdf") as pdf:
                                
                                fig1 = plt.figure(dpi=300, facecolor='w', edgecolor='k')
                                fig1.subplots_adjust(left=0.1, right=0.95, hspace=0.5, bottom=0.1, top=0.95)
                                ax1 = fig1.add_subplot(111)
                                ax1.plot(Joined_data_numeric.iloc[0:241,1],-Joined_data_numeric.iloc[0:241,2], 'o', markersize=2)
                                ax1.set_xlabel("Z' [$\Omega$]")
                                ax1.set_ylabel("-Z'' [$\Omega$]")
                                ax1.grid(b=True, which='major', axis='both', color='#D3D3D3', linestyle='--')
                                ax1.ticklabel_format(axis="both", style="sci", scilimits=(0,3))
                                ax1.tick_params(axis='x', labelsize=4)
                                plt.title('Nyquist plot', fontsize=7)
                                plt.axis('square')
                                plt.tight_layout()
                                
                                pdf.savefig(fig1)
                                plt.cla()
                                plt.clf()
                                plt.close("all")
                                fig1.clear()
                                plt.close(fig1)
                            
                                # to plot Bode plot
                                fig1 = plt.figure(dpi=300, facecolor='w', edgecolor='k')
                                fig1.subplots_adjust(left=0.1, right=0.95, hspace=0.5, bottom=0.1, top=0.95)
                                ax2 = fig1.add_subplot(111)
                                ax2.semilogx(Joined_data_numeric.iloc[0:241,0],Joined_data_numeric.iloc[0:241,1],'o',label="Z' [$\Omega$]",markersize =3)              
                                ax2.set_xlabel("Frequency [Hz]")
                                ax2.set_ylabel("Z' [$\Omega$]")
                                ax3 = ax2.twinx()
                                ax3.plot(Joined_data_numeric.iloc[0:241,0],-Joined_data_numeric.iloc[0:241,2],'go',markersize =2,label="-Z'' [$\Omega$]")
                                ax3.set_ylabel("-Z'' [$\Omega$]")
                                ax3.set_yscale('log')
                                ax2.grid(b=True, which='major', axis='both', color='#D3D3D3', linestyle='--')
                                ax2.legend(loc=(.75,.90), fontsize=5, frameon=False)
                                ax3.legend(loc=(.75,.95), fontsize=5, frameon=False)
                                plt.title('Bode plot', fontsize=7)
                                plt.tight_layout()
                                
                                pdf.savefig(fig1)
                                plt.cla()
                                plt.clf()
                                plt.close("all")
                                fig1.clear()
                                plt.close(fig1)                                
                           
                           

                                # to plot DRT with all curves
                                
                                fig1 = plt.figure(dpi=300, facecolor='w', edgecolor='k')
                                fig1.subplots_adjust(left=0.1, right=0.95, hspace=0.5, bottom=0.1, top=0.95)
                                ax4 = fig1.add_subplot(111)
                                
                                try:
                                    ymax = max(Joined_data_numeric.iloc[0:750,4])
                                    xmax = freq1_array[np.argmax(Joined_data_numeric.iloc[0:750,4])]
                                    ax4.plot(freq1_array,Joined_data_numeric.iloc[0:750,4],label=f'λ = 1E-2 & Reso.Frequency = {xmax:.3E} Hz', linewidth=1.5)
                                except KeyError:
                                    ax4.plot(freq1_array,Joined_data_numeric.iloc[0:750,4],label=f'λ = 1E-2', linewidth=1.5)
                                    
                                try:    
                                    ymax = max(Joined_data_numeric.iloc[0:750,6])
                                    xmax = freq2_array[np.argmax(Joined_data_numeric.iloc[0:750,6])]
                                    ax4.plot(freq2_array,Joined_data_numeric.iloc[0:750,6],label=f'λ = 1E-3 & Reso.Frequency = {xmax:.3E} Hz', linewidth=1.4)
                                except KeyError:
                                    ax4.plot(freq2_array,Joined_data_numeric.iloc[0:750,6],label=f'λ = 1E-3', linewidth=1.4)
                                    
                                try:
                                    ymax = max(Joined_data_numeric.iloc[0:750,8])
                                    xmax = freq3_array[np.argmax(Joined_data_numeric.iloc[0:750,8])]
                                    ax4.plot(freq3_array,Joined_data_numeric.iloc[0:750,8],label=f'λ = 1E-4 & Reso.Frequency = {xmax:.3E} Hz', linewidth=1.3)
                                except KeyError:
                                    ax4.plot(freq3_array,Joined_data_numeric.iloc[0:750,8],label=f'λ = 1E-4', linewidth=1.3)
                                    
                                try:
                                    ymax = max(Joined_data_numeric.iloc[0:750,10])
                                    xmax = freq1_array[np.argmax(Joined_data_numeric.iloc[0:750,10])]
                                    ax4.plot(freq4_array,Joined_data_numeric.iloc[0:750,10],label=f'λ = 1E-5 & Reso.Frequency = {xmax:.3E} Hz', linewidth=01.2)
                                except KeyError:
                                    ax4.plot(freq4_array,Joined_data_numeric.iloc[0:750,10],label=f'λ = 1E-5', linewidth=01.2)
                                    
                                try:
                                    ymax = max(Joined_data_numeric.iloc[0:750,12])
                                    xmax = freq5_array[np.argmax(Joined_data_numeric.iloc[0:750,12])]
                                    ax4.plot(freq5_array,Joined_data_numeric.iloc[0:750,12],label=f'λ = 1E-6 & Reso.Frequency = {xmax:.3E} Hz', linewidth=0.9)
                                except KeyError:
                                    ax4.plot(freq5_array,Joined_data_numeric.iloc[0:750,12],label=f'λ = 1E-6', linewidth=0.9)
                                    
                                try:
                                    ymax = max(Joined_data_numeric.iloc[0:750,14])
                                    xmax = freq6_array[np.argmax(Joined_data_numeric.iloc[0:750,14])]
                                    ax4.plot(freq6_array,Joined_data_numeric.iloc[0:750,14],label=f'λ = 1E-7 & Reso.Frequency = {xmax:.3E} Hz', linewidth=0.7)
                                except KeyError:
                                    ax4.plot(freq6_array,Joined_data_numeric.iloc[0:750,14],label=f'λ = 1E-7', linewidth=0.7)
                                    
                                                            
                                ax4.set_xlabel("Frequency [Hz]")
                                ax4.set_ylabel("$\gamma$  [$\Omega$]")
                                ax4.grid(b=True, which='major', axis='both', color='#D3D3D3', linestyle='--')
                                ax4.yaxis.set_major_locator(plt.MaxNLocator(5))
                                ax4.legend(loc='best', fontsize=5, frameon=False)
                                ax4.ticklabel_format(axis="y", style="sci", scilimits=(0,2))
                                ax4.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
                                plt.title(f'r1={set_r[0]:.0E}   q1={set_q[0]:.0E}   $\\alpha$p1={set_ap[0]}   r2={set_r[1]:.0E}   q2={set_q[1]:.0E}   $\\alpha$p2={set_ap[1]}   r3={set_r[2]:.0E}   q3={set_q[2]:.0E}   $\\alpha$p3={set_ap[2]}', fontsize=6)
                                
                                ax4.set_xscale('log')
                                locmaj = mpl.ticker.LogLocator(base=10,numticks=14) 
                                ax4.xaxis.set_major_locator(locmaj)

                                locmin = mpl.ticker.LogLocator(base=10.0,subs=(0.2,0.4,0.6,0.8),numticks=14)
                                ax4.xaxis.set_minor_locator(locmin)
                                ax4.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
                                                                
                                plt.tight_layout()
                                
                                pdf.savefig(fig1)
                                plt.cla()
                                plt.clf()
                                plt.close("all")
                                fig1.clear()
                                plt.close(fig1)
                            
                            
                            
                                # to plot DRT with all  λ = 1E-2
                                fig1 = plt.figure(dpi=300, facecolor='w', edgecolor='k')
                                fig1.subplots_adjust(left=0.1, right=0.95, hspace=0.5, bottom=0.1, top=0.95)
                                ax5 = fig1.add_subplot(111)
                                ax5.plot(freq1_array,Joined_data_numeric.iloc[0:750,4],label='λ = 1E-2')
                                ax5.set_xlabel("Frequency [Hz]")
                                ax5.set_ylabel("$\gamma$  [$\Omega$]")
                                ax5.grid(b=True, which='major', axis='both', color='#D3D3D3', linestyle='--')
                                ax5.yaxis.set_major_locator(plt.MaxNLocator(5))
                                ax5.legend(loc='best', fontsize=5, frameon=False)
                                ax5.ticklabel_format(axis="y", style="sci", scilimits=(0,2))
                                ax5.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
                                try:
                                    ymax = max(Joined_data_numeric.iloc[0:750,4])
                                    xmax = freq1_array[np.argmax(Joined_data_numeric.iloc[0:750,4])]
                                    plt.title(f'maximum peak: $\gamma$ = {ymax:.5E} $\Omega$ at frequency = {xmax:.5E} Hz', fontsize=7)
                                except KeyError:
                                    plt.title('No peak found....!!!', fontsize=7)
                                    pass
                                ax5.set_xscale('log')
                                locmaj = mpl.ticker.LogLocator(base=10,numticks=14) 
                                ax5.xaxis.set_major_locator(locmaj)

                                locmin = mpl.ticker.LogLocator(base=10.0,subs=(0.2,0.4,0.6,0.8),numticks=14)
                                ax5.xaxis.set_minor_locator(locmin)
                                ax5.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
                                plt.tight_layout()
                                
                                pdf.savefig(fig1)
                                plt.cla()
                                plt.clf()
                                plt.close("all")
                                fig1.clear()
                                plt.close(fig1)
                            
                                                              
                            
                                # to plot DRT with all  λ = 1E-3
                                fig1 = plt.figure(dpi=300, facecolor='w', edgecolor='k')
                                fig1.subplots_adjust(left=0.1, right=0.95, hspace=0.5, bottom=0.1, top=0.95)
                                ax6 = fig1.add_subplot(111)
                                ax6.plot(freq2_array,Joined_data_numeric.iloc[0:750,6],label='λ = 1E-3')
                                ax6.set_xlabel("Frequency [Hz]")
                                ax6.set_ylabel("$\gamma$  [$\Omega$]")
                                ax6.grid(b=True, which='major', axis='both', color='#D3D3D3', linestyle='--')
                                ax6.yaxis.set_major_locator(plt.MaxNLocator(5))
                                ax6.legend(loc='best', fontsize=5, frameon=False)
                                ax6.ticklabel_format(axis="y", style="sci", scilimits=(0,2))
                                ax6.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
                                try:
                                    ymax = max(Joined_data_numeric.iloc[0:750,6])
                                    xmax = freq2_array[np.argmax(Joined_data_numeric.iloc[0:750,6])]
                                    plt.title(f'maximum peak: $\gamma$ = {ymax:.5E} $\Omega$ at frequency = {xmax:.5E} Hz', fontsize=7)
                                except KeyError:
                                    plt.title('No peak found....!!!', fontsize=7)
                                    pass
                                ax6.set_xscale('log')
                                locmaj = mpl.ticker.LogLocator(base=10,numticks=14) 
                                ax6.xaxis.set_major_locator(locmaj)

                                locmin = mpl.ticker.LogLocator(base=10.0,subs=(0.2,0.4,0.6,0.8),numticks=14)
                                ax6.xaxis.set_minor_locator(locmin)
                                ax6.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
                                plt.tight_layout()
                                
                                pdf.savefig(fig1)
                                plt.cla()
                                plt.clf()
                                plt.close("all")
                                fig1.clear()
                                plt.close(fig1)
                            
                                                           
                            
                                # to plot DRT with all  λ = 1E-4
                                fig1 = plt.figure(dpi=300, facecolor='w', edgecolor='k')
                                fig1.subplots_adjust(left=0.1, right=0.95, hspace=0.5, bottom=0.1, top=0.95)
                                ax7 = fig1.add_subplot(111)
                                ax7.plot(freq3_array,Joined_data_numeric.iloc[0:750,8],label='λ = 1E-4')
                                ax7.set_xlabel("Frequency [Hz]")
                                ax7.set_ylabel("$\gamma$  [$\Omega$]")
                                ax7.grid(b=True, which='major', axis='both', color='#D3D3D3', linestyle='--')
                                ax7.yaxis.set_major_locator(plt.MaxNLocator(5))
                                ax7.legend(loc='best', fontsize=5, frameon=False)
                                ax7.ticklabel_format(axis="y", style="sci", scilimits=(0,2))
                                ax7.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
                                try:
                                    ymax = max(Joined_data_numeric.iloc[0:750,8])
                                    xmax = freq3_array[np.argmax(Joined_data_numeric.iloc[0:750,8])]
                                    plt.title(f'maximum peak: $\gamma$ = {ymax:.5E} $\Omega$ at frequency = {xmax:.5E} Hz', fontsize=7)
                                except KeyError:
                                    plt.title('No peak found....!!!', fontsize=7)
                                    pass
                                ax7.set_xscale('log')
                                locmaj = mpl.ticker.LogLocator(base=10,numticks=14) 
                                ax7.xaxis.set_major_locator(locmaj)

                                locmin = mpl.ticker.LogLocator(base=10.0,subs=(0.2,0.4,0.6,0.8),numticks=14)
                                ax7.xaxis.set_minor_locator(locmin)
                                ax7.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
                                plt.tight_layout()
                                
                                pdf.savefig(fig1)
                                plt.cla()
                                plt.clf()
                                plt.close("all")
                                fig1.clear()
                                plt.close(fig1)
                            
                                                     
                            
                            
                                # to plot DRT with all  λ = 1E-5
                                fig1 = plt.figure(dpi=300, facecolor='w', edgecolor='k')
                                fig1.subplots_adjust(left=0.1, right=0.95, hspace=0.5, bottom=0.1, top=0.95)
                                ax8 = fig1.add_subplot(111)
                                ax8.plot(freq4_array,Joined_data_numeric.iloc[0:750,10],label='λ = 1E-5')
                                ax8.set_xlabel("Frequency [Hz]")
                                ax8.set_ylabel("$\gamma$  [$\Omega$]")
                                ax8.grid(b=True, which='major', axis='both', color='#D3D3D3', linestyle='--')
                                ax8.yaxis.set_major_locator(plt.MaxNLocator(5))
                                ax8.legend(loc='best', fontsize=5, frameon=False)
                                ax8.ticklabel_format(axis="y", style="sci", scilimits=(0,2))
                                ax8.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
                                try:
                                    ymax = max(Joined_data_numeric.iloc[0:750,10])
                                    xmax = freq4_array[np.argmax(Joined_data_numeric.iloc[0:750,10])]
                                    plt.title(f'maximum peak: $\gamma$ = {ymax:.5E} $\Omega$ at frequency = {xmax:.5E} Hz', fontsize=7)
                                except KeyError:
                                    plt.title('No peak found....!!!', fontsize=7)
                                    pass    
                                ax8.set_xscale('log')
                                locmaj = mpl.ticker.LogLocator(base=10,numticks=14) 
                                ax8.xaxis.set_major_locator(locmaj)

                                locmin = mpl.ticker.LogLocator(base=10.0,subs=(0.2,0.4,0.6,0.8),numticks=14)
                                ax8.xaxis.set_minor_locator(locmin)
                                ax8.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
                                plt.tight_layout()
                                
                                pdf.savefig(fig1)
                                plt.cla()
                                plt.clf()
                                plt.close("all")
                                fig1.clear()
                                plt.close(fig1)
                            
                                
                            
                                 # to plot DRT with all  λ = 1E-6
                                fig1 = plt.figure(dpi=300, facecolor='w', edgecolor='k')
                                fig1.subplots_adjust(left=0.1, right=0.95, hspace=0.5, bottom=0.1, top=0.95)
                                ax9 = fig1.add_subplot(111)
                                ax9.plot(freq5_array,Joined_data_numeric.iloc[0:750,12],label='λ = 1E-6')
                                ax9.set_xlabel("Frequency [Hz]")
                                ax9.set_ylabel("$\gamma$  [$\Omega$]")
                                ax9.grid(b=True, which='major', axis='both', color='#D3D3D3', linestyle='--')
                                ax9.yaxis.set_major_locator(plt.MaxNLocator(5))
                                ax9.legend(loc='best', fontsize=5, frameon=False)
                                ax9.ticklabel_format(axis="y", style="sci", scilimits=(0,2))
                                ax9.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
                                try:
                                    ymax = max(Joined_data_numeric.iloc[0:750,12])
                                    xmax = freq5_array[np.argmax(Joined_data_numeric.iloc[0:750,12])]
                                    plt.title(f'maximum peak: $\gamma$ = {ymax:.5E} $\Omega$ at frequency = {xmax:.5E} Hz', fontsize=7)
                                except KeyError:
                                    plt.title('No peak found....!!!', fontsize=7)
                                    pass
                                ax9.set_xscale('log')
                                locmaj = mpl.ticker.LogLocator(base=10,numticks=14) 
                                ax9.xaxis.set_major_locator(locmaj)

                                locmin = mpl.ticker.LogLocator(base=10.0,subs=(0.2,0.4,0.6,0.8),numticks=14)
                                ax9.xaxis.set_minor_locator(locmin)
                                ax9.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
                                plt.tight_layout()
                                
                                pdf.savefig(fig1)
                                plt.cla()
                                plt.clf()
                                plt.close("all")
                                fig1.clear()
                                plt.close(fig1)
                            
                            
                            

                                 # to plot DRT with all  λ = 1E-7
                                fig1 = plt.figure(dpi=300, facecolor='w', edgecolor='k')
                                fig1.subplots_adjust(left=0.1, right=0.95, hspace=0.5, bottom=0.1, top=0.95)
                                ax10 = fig1.add_subplot(111)
                                ax10.plot(freq6_array,Joined_data_numeric.iloc[0:750,14],label='λ = 1E-7')
                                ax10.set_xlabel("Frequency [Hz]")
                                ax10.set_ylabel("$\gamma$  [$\Omega$]")
                                ax10.grid(b=True, which='major', axis='both', color='#D3D3D3', linestyle='--')
                                ax10.yaxis.set_major_locator(plt.MaxNLocator(5))
                                ax10.legend(loc='best', fontsize=5, frameon=False)
                                ax10.ticklabel_format(axis="y", style="sci", scilimits=(0,2))
                                ax10.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
                                try:
                                    ymax = max(Joined_data_numeric.iloc[0:750,14])
                                    xmax = freq6_array[np.argmax(Joined_data_numeric.iloc[0:750,14])]
                                    plt.title(f'maximum peak: $\gamma$ = {ymax:.5E} $\Omega$ at frequency = {xmax:.5E} Hz', fontsize=7)
                                except KeyError:
                                    plt.title('No peak found....!!!', fontsize=7)
                                    pass   
                                ax10.set_xscale('log')
                                locmaj = mpl.ticker.LogLocator(base=10,numticks=14) 
                                ax10.xaxis.set_major_locator(locmaj)

                                locmin = mpl.ticker.LogLocator(base=10.0,subs=(0.2,0.4,0.6,0.8),numticks=14)
                                ax10.xaxis.set_minor_locator(locmin)
                                ax10.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
                                plt.tight_layout()
                                
                                pdf.savefig(fig1)
                                plt.cla()
                                plt.clf()
                                plt.close("all")
                                fig1.clear()
                                plt.close(fig1)
                            
                            
                            
                                                     
                            ###########code for exporting pdf ended here###########  
                            del ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8,ax9,ax10,fig1                       
                            
                            gc.collect()
                            

end_time = datetime.now()
print(' Execution is complete \n Duration: {}'.format(end_time - start_time))


# In[ ]:




