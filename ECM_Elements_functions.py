#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from mpmath import*  # to use coth,tanh
# importing "cmath" for complex number operations 
import cmath 
import math

# to define series operation
def series(*args):
    z = complex(0,0)
    for elem in args:
        z += elem
    return z


# to define parallel operation
def parallel(*args):
    z = complex(0,0)
    for elem in args:
        z += (1/elem)
    return 1/z


# to define resistance
def R(r):
    z = complex(r,0);
    return z


# to define capacitance
def C(c, f):
    omega = 2*math.pi*f
    z = 1.0/(1j*c*omega)
    return z


# to define Constant Phase Element (CPE)
def P(q,alpha_p,f):
    omega = 2*math.pi*f
    z = 1.0/(q*(1j*omega)**alpha_p)
    return z


# to define inductance
def L(l, f):
    omega = 2*math.pi*f
    z = 1j*l*omega
    return z


# to define INFINITE WARBURG-IMPEDANCE
def W(Aw,f):
    omega = 2*math.pi*f
    z = (Aw/omega**0.5)-(1j*(Aw/omega**0.5))
    return z



# to define FINITE WARBURG-IMPEDANCE (OPEN)
def Wo(zw,tau,alpha_wo,f):
    omega = 2*math.pi*f
    z = (zw*mp.coth((1j*omega*tau)**alpha_wo))/((1j*omega*tau)**alpha_wo)
    return z


# to define FINITE WARBURG-IMPEDANCE (SHORT)
def Ws(zw,tau,alpha_ws,f):
    omega = 2*math.pi*f
    z = (zw*mp.tanh((1j*omega*tau)**alpha_ws))/((1j*omega*tau)**alpha_ws)
    return z


# to define GERISCHER-ELEMENT
def G(y,k,f):
    omega = 2*math.pi*f
    z = 1/(y*(k+(1j*omega))**0.5)
    return z


# In[ ]:




