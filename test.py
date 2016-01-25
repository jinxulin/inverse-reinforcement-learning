__author__ = 'Kintoki'
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10 , 1000)
y = np.sin(x)
z = np.cos(x**2)
plt.figure(figsize=(8,4))