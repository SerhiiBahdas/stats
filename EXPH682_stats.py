a#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 09:43:24 2020

@author: Serhii Bahdasariants. NEL. WVU
"""

#  Files that start with corr: formulate null hypotheses (H0) and apply correlation
#  analysis to test them. Please, do not forget to use the correction for multiple
#  comparisons. For bonus points, apply ANOVA using sSex column data for defining
#  a single factor. The outcome of the assignment comprises the description of H0,
#  three Pearson correlation coefficient values (or F-statistics for ANOVA) with
#  associated p-values, and the statement of whether H0 is/are rejected or not.

# Data import
import pandas as pd
data = pd.read_csv('/Users/labmate/Python_projects/EXP682_stats/corr_homework11.csv')

#Correlation--

# Pearson's coefficients calculation
from scipy.stats import pearsonr, spearmanr
[R_xy, p_xy] = pearsonr(data.Xvar,data.Yvar)
[R_zy, p_zy] = pearsonr(data.Zvar,data.Yvar)
[R_zx, p_zx] = pearsonr(data.Zvar,data.Xvar)

#Spearman's coefficients calculation
[Rho, p_xyz] = spearmanr(data[['Xvar', 'Yvar', 'Zvar']])

# Bonfferoni correction for Pearson
from statsmodels.stats.multitest import multipletests
[reject, p_corrected, alphacSidak, alphacBonf] = multipletests([p_xy,p_zy,p_zx], alpha=0.05, method='bonferroni')
# Bonfferoni correction for Spearman
[rejectS, p_correctedS, alphacSidakS, alphacBonfS] = multipletests([p_xyz[0,1],p_xyz[1,2],p_xyz[0,2]], alpha=0.05, method='bonferroni')

#Results visualization
import matplotlib.pyplot as plt
import seaborn

def build_heatmap(x):
    plt.figure()
    seaborn.heatmap(x, center = 2, annot=True,
                    xticklabels = ['Xvar', 'Yvar', 'Zvar'],
                    yticklabels = ['Xvar', 'Yvar', 'Zvar'])

build_heatmap(Rho)
build_heatmap(p_xyz)

def scatter_plot (x,y,c,p,R):
    plt.figure()
    plt.scatter(x, y, c = c, alpha=0.5, s = 60)
    plt.title('R = {}, p = {}'.format(round(R,4), round(p,5)))
    plt.xlabel(str(x.name)), plt.ylabel(str(y.name))
    plt.legend(), plt.grid(True)
    
    
scatter_plot(data.Xvar, data.Yvar, 'b', p_corrected[0], R_xy)
scatter_plot(data.Zvar, data.Yvar, 'r', p_corrected[1], R_zy)
scatter_plot(data.Zvar, data.Xvar, 'm', p_corrected[2], R_zx)

#ANOVA--

#Data visualization - density plots
def density_plot(x,y):
    plt.figure()
    seaborn.kdeplot(x, shade=True, color="r", label = 'Male')
    seaborn.kdeplot(y, shade=True, color="b", label = 'Female')
    plt.grid(True), plt.xlabel(str(x.name)), plt.ylabel('Density function (gaussian kernel)')
    plt.legend()
    
density_plot(data.Xvar[data.sSex == 'M'], data.Xvar[data.sSex == 'F'])
density_plot(data.Yvar[data.sSex == 'M'], data.Yvar[data.sSex == 'F'])
density_plot(data.Zvar[data.sSex == 'M'], data.Zvar[data.sSex == 'F'])

#test data on normality 
from scipy.stats import normaltest
alpha = 0.05

#null hypothesis: x comes from a normal distribution
#overall population
kx, xp = normaltest(data.Xvar); 
ky, yp = normaltest(data.Yvar); 
kz, zp = normaltest(data.Zvar); 

[reject_all, p_corrected_all, alphacSidak_all, alphacBonf_all] = multipletests([xp, yp, zp], alpha=0.05, method='bonferroni')

print("\nXvar comes from n distr.: {}".format(reject_all[0] == 0))
print("Yvar comes from n distr.: {}".format(reject_all[1] == 0))
print("Zvar comes from n distr.: {}".format(reject_all[2] == 0))


#male population
kx_m, xp_m = normaltest(data.Xvar[data.sSex == 'M']); 
ky_m, yp_m = normaltest(data.Yvar[data.sSex == 'M']); 
kz_m, zp_m = normaltest(data.Zvar[data.sSex == 'M']); 

[reject1, p_corrected1, alphacSidak1, alphacBonf1] = multipletests([xp_m, yp_m, zp_m], alpha=0.05, method='bonferroni')

print("\nXvar_male comes from n distr.: {}".format(reject1[0] == 0))
print("Yvar_male comes from n distr.: {}".format(reject1[1] == 0))
print("Zvar_male comes from n distr.: {}".format(reject1[2] == 0))

#female population
kx_f, xp_f = normaltest(data.Xvar[data.sSex == 'F']); 
ky_f, yp_f = normaltest(data.Yvar[data.sSex == 'F']); 
kz_f, zp_f = normaltest(data.Zvar[data.sSex == 'F']); 

[reject2, p_corrected2, alphacSidak2, alphacBonf2] = multipletests([xp_f, yp_f, zp_f], alpha=0.05, method='bonferroni')

print("\nXvar_female comes from n distr.: {}".format(reject2[0] == 0))
print("Yvar_female comes from n distr.: {}".format(reject2[1] == 0))
print("Zvar_female comes from n distr.: {}".format(reject2[2] == 0))

#Standard deviations
import numpy as np
malex_std = np.std(data.Xvar[data.sSex == 'M'])
maley_std = np.std(data.Yvar[data.sSex == 'M'])
malez_std = np.std(data.Zvar[data.sSex == 'M'])

femalex_std = np.std(data.Xvar[data.sSex == 'F'])
femaley_std = np.std(data.Yvar[data.sSex == 'F'])
femalez_std = np.std(data.Zvar[data.sSex == 'F'])

print('\nSTD MaleX = {}, STD FemaleX = {}'.format(round(malex_std,3), round(femalex_std,3)))
print('STD MaleY = {}, STD FemaleY = {}'.format(round(maley_std,3), round(femaley_std,3)))
print('STD MaleZ = {}, STD FemaleZ = {}'.format(round(malez_std,3), round(femalez_std,3)))

#One-way ANOVA
from scipy.stats import f_oneway

#null hypothesis: two groups have the same population mean
fx, px =  f_oneway(data.Xvar[data.sSex == 'M'],data.Xvar[data.sSex == 'F'])
fy, py =  f_oneway(data.Yvar[data.sSex == 'M'],data.Yvar[data.sSex == 'F'])
fz, pz =  f_oneway(data.Zvar[data.sSex == 'M'],data.Zvar[data.sSex == 'F'])

[reject_anova, p_corrected_anova, alphacSidak_anova, alphacBonf_anova] = multipletests([px, py, pz],alpha=0.05, method='bonferroni')

print("\nX_F = {}, X_p = {}".format(round(fx,3), round(p_corrected_anova[0],5)))
print("Y_F = {}, Y_p = {}".format(round(fy,3), round(p_corrected_anova[1],5)))
print("Z_F = {}, Z_p = {}".format(round(fz,3), round(p_corrected_anova[2],5)))