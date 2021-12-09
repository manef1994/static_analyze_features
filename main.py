import bisect
import math
import statistics
from shapely.geometry import LineString
import antropy as ant
import numpy as np
from matplotlib import *
from pathlib import Path
import matplotlib.pyplot as plt

path = "/home/manef/tests/siena_vs_fantasia/overlopping/"
ID = "14-2"

# == load the epileptic patient
with open(path + "App-PN" + ID + "-10.txt", 'r') as file1:
    app = [float(i) for line in file1 for i in line.split('\n') if i.strip()]

# with open(path + "Sample-PN" + ID + "-10.txt", 'r') as file1:
#     sample = [float(i) for line in file1 for i in line.split('\n') if i.strip()]

# with open(path + "SDNN-PN" + ID + "-10.txt", 'r') as file1:
#     SDNN = [float(i) for line in file1 for i in line.split('\n') if i.strip()]

with open(path + "NN50-PN" + ID + "-10.txt", 'r') as file1:
    NN50 = [float(i) for line in file1 for i in line.split('\n') if i.strip()]

# with open(path + "RMSSD-PN" + ID + "-10.txt", 'r') as file1:
#     RMSSD = [float(i) for line in file1 for i in line.split('\n') if i.strip()]
#
# with open(path + "spectral-PN" + ID + "-10.txt", 'r') as file1:
#     spectral = [float(i) for line in file1 for i in line.split('\n') if i.strip()]

# == load healthy subjects
# path = "/home/manef/tests/siena_vs_fantasia/fantasia_features/"
#
# ID = "f1y06-60_120"

# with open(path + "App-" + ID + "-10.txt", 'r') as file1:
#     app = [float(i) for line in file1 for i in line.split('\n') if i.strip()]

# with open(path + "Sample-" + ID + "-10.txt", 'r') as file1:
#     sample = [float(i) for line in file1 for i in line.split('\n') if i.strip()]

# with open(path + "NN50-" + ID + "-10.txt", 'r') as file1:
#     NN50 = [float(i) for line in file1 for i in line.split('\n') if i.strip()]

# with open(path + "RMSSD-" + ID + "-10.txt", 'r') as file1:
#     RMSSD = [float(i) for line in file1 for i in line.split('\n') if i.strip()]
#
# with open(path + "spectral-" + ID + "-10.txt", 'r') as file1:
#     spectral = [float(i) for line in file1 for i in line.split('\n') if i.strip()]
#
# with open(path + "SDNN-" + ID + "-10.txt", 'r') as file1:
#     SDNN = [float(i) for line in file1 for i in line.split('\n') if i.strip()]

# peaks = []
# with open(path + "peaks-" + ID + "-10.txt", 'r') as file1:
#     peaks = [float(i) for line in file1 for i in line.split('\n') if i.strip()]

# == healthy subjects
NN50_ep, pNN50_ep, SDNN_ep, SDNN_test, nn50_test_sei, fft_ep, welch_ep, RMSSD_ep = ([] for i in range(8))

# == healthy subjects

#nn50_test_hea, SDNN, pNN50, NN50, welch, fft, RMSSD = ([] for i in range(7))

pre_ictal = []
STD = []
STD_healthy = []

def std_compute(xx):
    i = 0
    j = 6
    STD = []

    while (True):
        go_in = []

        go_in = xx[i:j]
        std = np.std(go_in)
        STD.append(std)

        j = j + 6
        i = i + 6

        if j > len(app):
            break
    return STD

STD_app = std_compute(app)
# STD_sample = std_compute(sample)
# STD_SDNN = std_compute(SDNN)
STD_NN50 = std_compute(NN50)
# STD_rmssd = std_compute(RMSSD)
# STD_spectral = std_compute(spectral)

first = 0
tt = [first]
i = 1
while i <= len(app) - 1:
    first = first + 10
    tt.append(first)
    i = i + 1

first = 0
tt_healthy = [first]
i = 1
while i <= len(STD_app) - 1:
    first = first + 60
    tt_healthy.append(first)
    i = i + 1

first = 0
tt_healthy = [first]
i = 1
while i <= len(STD_app) - 1:
    first = first + 1
    tt_healthy.append(first)
    i = i + 1

# ____ woerking on the approximate thresholding
x = numpy.zeros(len(STD_app), dtype=float, order='C')
xy = numpy.zeros(len(app), dtype=float, order='C')

arr=[]
arr1=[]

for i in range (len(STD_app)):
    arr.append(0.07)
    arr1.append(0)

first_line = LineString(np.column_stack((tt_healthy,STD_app)))
second_line = LineString(np.column_stack((tt_healthy,arr)))
intersection = first_line.intersection(second_line)

x, y = LineString(intersection).xy

result = np.where(STD_app == STD_app[len(STD_app) - 10])

go = bisect.bisect_right(x, result[0])

index_threshold = x[go - 1]

print('index threshold\t', index_threshold )

# ____ working on the NN50 thresholding

arr_n=[]
arr1_n=[]

for i in range (len(STD_NN50)):
    arr_n.append(5)
    arr1_n.append(0)

first_line_n = LineString(np.column_stack((tt_healthy, STD_NN50)))
second_line_n = LineString(np.column_stack((tt_healthy, arr_n)))
intersection_n = first_line_n.intersection(second_line_n)

x_n, y_n = LineString(intersection_n).xy

# result = np.where(STD_NN50 == STD_NN50[len(STD_NN50) - 10])
#
# go = bisect.bisect_right(x, result[0])
#
# index_threshold_n = x[go - 1]

# print('index threshold\t', index_threshold_n )

#go = bisect.bisect_left(x, result)

# 0.15386027673006075

# array('d', [20.674026070985576, 21.375799742626604, 24.835173349117987, 25.144864930160093, 31.251426864399274, 32.77824431486669, 33.31204072571591, 35.367657501791655, 36.25015602208525, 37.97279724942647, 44.437310033274606, 45.352586139261014, 47.18662398202637, 48.85492623558239, 53.22404377724342, 54.74594183729389, 57.02551364687237, 58.803944407332665, 59.34866467674018, 60.783847142563296, 61.24868358025391, 63.31407851420438, 66.41567957908599])
# == plotting STD of approximate entropy
fig, axs = plt.subplots(2, 1)
axs[0].plot(tt, app, label="approximate entropy of healthy signal", marker='o')
axs[1].plot(tt_healthy,STD_app, label="STD of approximate entropy", marker='o')
# axs[1].plot(tt_healthy,arr, label="STD of approximate entropy", marker='o')
# axs[0].set_title('Patient ' + ID, fontsize=24, y=1)
# axs[1].set_title("Patient " + ID_healthy, fontsize=24, y=1)
axs[0].axvline(x=tt[-1] - 600, color='red', linestyle='--')
axs[1].axvline(x=len(STD_app) - 10, color='red', linestyle='--')

axs[0].set_title('Subject ' + ID,fontsize=24, y=1)

axs[1].axhline(y=0.07, color='blue', linestyle='--')

axs[0].set_xlabel('sample en seconde')
axs[0].set_ylabel('valeur de entropie')
axs[1].set_xlabel('sample en seconde')
axs[1].set_ylabel('valeur de entropie')
axs[0].grid(True)
axs[1].grid(True)
axs[0].legend()
axs[1].legend()

ymin = 0.1
ymax = 1.3
axs[0].set_ylim([ymin,ymax])

ymin_1 = 0
ymax_1 = 0.25
axs[1].set_ylim([ymin_1,ymax_1])

if intersection.geom_type == 'MultiPoint':
    axs[1].plot(*LineString(intersection).xy, 'o')
elif intersection.geom_type == 'Point':
    axs[1].plot(*intersection.xy, 'o')

# # == STD of sample entropy
# fig, axs = plt.subplots(2, 1)
# axs[0].plot(sample, label=" sample entropy of healthy signal", marker='o')
# axs[1].plot(STD_sample, label="STD of sample entropy", marker='o')
# axs[0].set_title('Subject ' + ID,fontsize=24, y=1)
# # axs[0].axvline(x=len(sample) - 60, color='red', linestyle='--')
# # axs[1].axvline(x=len(STD_sample) - 10, color='red', linestyle='--')
# axs[0].set_xlabel('sample en seconde')
# axs[0].set_ylabel('valeur de entropie')
# axs[1].set_xlabel('sample en seconde')
# axs[1].set_ylabel('valeur de entropie')
# axs[0].grid(True)
# axs[1].grid(True)
# axs[0].legend()
# axs[1].legend()
#
# ymin = 0; ymax = 2.5
# axs[0].set_ylim([ymin,ymax])
#
# ymin_1 = 0; ymax_1 = 0.5
# axs[1].set_ylim([ymin_1,ymax_1])

# == plotting SDNN
# fig, axs = plt.subplots(2, 1)
# axs[0].plot(SDNN, label=" SDNNN entropy of healthy signal", marker='o')
# axs[1].plot(STD_SDNN, label="STD of SDNN", marker='o')
# axs[0].set_title('Subject ' + ID,fontsize=24, y=1)
# # axs[0].axvline(x=len(sample) - 60, color='red', linestyle='--')
# # axs[1].axvline(x=len(STD_sample) - 10, color='red', linestyle='--')
# axs[0].set_xlabel('sample en seconde')
# axs[0].set_ylabel('valeur de entropie')
# axs[1].set_xlabel('sample en seconde')
# axs[1].set_ylabel('valeur de entropie')
# axs[0].grid(True)
# axs[1].grid(True)
# axs[0].legend()
# axs[1].legend()
#
# ymin = 0; ymax = 0.2
# axs[0].set_ylim([ymin,ymax])
#
# ymin_1 = 0; ymax_1 = 0.026
# axs[1].set_ylim([ymin_1,ymax_1])

# == plotting NN50
fig, axs = plt.subplots(2, 1)
axs[0].plot(tt_healthy,STD_app, label="STD of approximate entropy", marker='o')
axs[1].plot(tt_healthy, STD_NN50, label="STD of NN50", marker='o')

axs[0].set_title('Subject ' + ID,fontsize=24, y=1)

axs[0].axvline(x= len(STD_app) - 10, color='red', linestyle='--')
axs[1].axvline(x= len(STD_NN50) - 10, color='red', linestyle='--')

axs[0].set_xlabel('sample en seconde')
axs[0].set_ylabel('valeur de entropie')
axs[1].set_xlabel('sample en seconde')
axs[1].set_ylabel('valeur de entropie')
axs[0].grid(True)
axs[1].grid(True)
axs[0].legend()
axs[1].legend()

axs[1].axhline(y=5, color='blue', linestyle='--')
axs[0].axhline(y=0.07, color='blue', linestyle='--')

ymin_1 = 0; ymax_1 = 0.25
axs[0].set_ylim([ymin_1,ymax_1])

ymin_1 = 0; ymax_1 = 14
axs[1].set_ylim([ymin_1,ymax_1])

if intersection.geom_type == 'MultiPoint':
    axs[0].plot(*LineString(intersection).xy, 'o')
    # for i in range (len(y)):
    #     axs[0].axvline(x=x[i], color='green', linestyle='--')
elif intersection.geom_type == 'Point':
    axs[0].plot(*intersection.xy, 'o')
    # for i in range(len(y)):
    #     axs[0].axvline(x=x[i], color='green', linestyle='--')

if intersection_n.geom_type == 'MultiPoint':
    axs[1].plot(*LineString(intersection_n).xy, 'o')
    # for i in range(len(x_n)):
    #     axs[1].axvline(x=x_n[i], color='green', linestyle='--')
elif intersection_n.geom_type == 'Point':
    axs[1].plot(*intersection_n.xy, 'o')
    # for i in range(len(x_n)):
    #     axs[1].axvline(x=x_n[i], color='green', linestyle='--')

# == plotting specteal entropy
# fig, axs = plt.subplots(2, 1)
# axs[0].plot(spectral, label=" spectral entropy of healthy signal", marker='o')
# axs[1].plot(STD_spectral, label="STD of spectral entropy", marker='o')
# axs[0].set_title('Subject ' + ID, fontsize=24, y=1)
# # axs[0].axvline(x=len(spectral) - 60, color='red', linestyle='--')
# # axs[1].axvline(x=len(STD_spectral) - 10, color='red', linestyle='--')
# axs[0].set_xlabel('sample en seconde')
# axs[0].set_ylabel('valeur de entropie')
# axs[1].set_xlabel('sample en seconde')
# axs[1].set_ylabel('valeur de entropie')
# axs[0].grid(True)
# axs[1].grid(True)
# axs[0].legend()
# axs[1].legend()
#
# ymin = 0 ; ymax = 10
# axs[0].set_ylim([ymin,ymax])
#
# ymin_1 = 0; ymax_1 = 14
#axs[1].set_ylim([ymin_1,ymax_1])

# == plotting NN50
fig, axs = plt.subplots(2, 1)
axs[0].plot(tt, NN50, label=" NN50 of healthy signal", marker='o')
axs[1].plot(tt_healthy, STD_NN50, label="STD of NN50", marker='o')
axs[0].set_title('Subject ' + ID,fontsize=24, y=1)

axs[0].axvline(x=tt[-1] - 600, color='red', linestyle='--')
axs[1].axvline(x= len(STD_NN50) - 10, color='red', linestyle='--')

axs[0].set_xlabel('sample en seconde')
axs[0].set_ylabel('valeur de entropie')
axs[1].set_xlabel('sample en seconde')
axs[1].set_ylabel('valeur de entropie')
axs[0].grid(True)
axs[1].grid(True)
axs[0].legend()
axs[1].legend()

axs[1].axhline(y=5, color='blue', linestyle='--')

ymin = 70 ; ymax = 275
axs[0].set_ylim([ymin,ymax])

ymin_1 = 0; ymax_1 = 14
axs[1].set_ylim([ymin_1,ymax_1])

if intersection_n.geom_type == 'MultiPoint':
    axs[1].plot(*LineString(intersection_n).xy, 'o')
elif intersection_n.geom_type == 'Point':
    axs[1].plot(*intersection_n.xy, 'o')


plt.show()

print('')
