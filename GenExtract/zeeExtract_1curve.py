#! /usr/bin/env python
#-*-coding: utf-8 -*-

# MUST be launched with the cmsenv cmd after a cmsrel cmd !!

import os,sys,subprocess
import urllib2
import re

import pandas as pd
import numpy as np
import matplotlib

import matplotlib.dates as md
matplotlib.use('agg')
from matplotlib import pyplot as plt

#import seaborn # only with cmsenv on cca.in2p3.fr

# lines below are only for func_Extract
from sys import argv
from os import listdir
from os.path import isfile, join

argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
argv.remove( '-b-' )

from ROOT import *

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.gSystem.Load("libDataFormatsFWLite.so")
ROOT.FWLiteEnabler.enable()

sys.path.append('../ChiLib_CMS_Validation')
from graphicFunctions import getHisto
from default import *

# these line for daltonians !
#seaborn.set_palette('colorblind')

from DataFormats.FWLite import Handle, Events

def getHisto(file, tp):
    path = 'DQMData/Run 1/EgammaV/Run summary/' + tp
    t_path = file.Get(path)
    return t_path # t5

def getListFiles(path):
    #print('path : %s' % path)
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    onlyfiles = [f for f in onlyfiles if f.endswith(".root")] # keep only root files
    #print(onlyfiles)
    return onlyfiles

def getBranches(t_p):
    b = []
    source = open("../ChiLib_CMS_Validation/HistosConfigFiles/ElectronMcSignalHistos.txt", "r")
    for ligne in source:
        if t_p in ligne:
            #print(ligne)
            tmp = ligne.split(" ", 1)
            #print(tmp[0].replace(t_p + "/", ""))
            b.append(tmp[0].replace(t_p + "/", ""))
    source.close()
    return b

def diffMAXKS(s0,s1, sum0, sum1):
    s0 = np.asarray(s0) # if not this, ind is returned as b_00x instead of int value
    s1 = np.asarray(s1)
    N = len(s0)
    #print('diffMAXKS : %d' % N)
    v0 = 0.
    v1 = 0.
    sDKS = []
    for i in range(0, N):
        t0 = s0[i]/sum0 
        t1 = s1[i]/sum1 
        v0 += t0
        v1 += t1
        sDKS.append(np.abs(v1 - v0))
    v = max(sDKS)
    ind = sDKS.index(v)
    return v, ind, sDKS

def integralpValue(abscisses, ordonnees, x):
    #print(abscisses)
    #print(ordonnees)
    v = 0.0
    N = len(abscisses)
    #print('== ', x)
    if (x <= abscisses[0]) :
        x = 0. #ttl integral
        for i in range(0, N-1):
            v += (abscisses[i+1] - abscisses[i]) * ordonnees[i]
            #print(v)
    elif (x >= abscisses[N-1]):
        v = 0. # null integral
    else: # general case
        ind = 0
        for i in range(0, N):
            if (np.floor(x/abscisses[i]) == 0):
                ind = i                
                break
        #print('ind : %d' % ind)    
        v = (abscisses[ind] - x) * ordonnees[ind-1]
        for i in range(ind, N-1):
            v += (abscisses[i+1] - abscisses[i]) * ordonnees[i]
    return v

# create a Kolmogorov-Smirnov curve (integrated curve) with s0
def funcKS(s0):
    s0 = np.asarray(s0) # if not this, ind is returned as b_00x instead of int value
    #print(s0)
    N = len(s0)
    SumSeries0 = np.floor(s0.sum())
    #SumSeries0 = s0.sum()
    v0 = 0.
    sDKS = []
    for i in range(0, N):
        t0 = s0[i]/SumSeries0
        v0 += t0
        sDKS.append(np.abs(v0))
    return sDKS

def func_Extract(br, nbFiles): # read files
    print("func_Extract")
    
    branches = []
    wr = []
    histos = {}
        

    # get the branches for ElectronMcSignalHistos.txt
    #branches += ["h_recEleNum", "h_scl_ESFrac_endcaps", "h_scl_sigietaieta", "h_ele_PoPtrue_endcaps", "h_ele_PoPtrue", "h_scl_bcl_EtotoEtrue_endcaps", "h_scl_bcl_EtotoEtrue_barrel", "h_ele_Et"]
    #branches += ["h_recEleNum"]
    branches = br
    for leaf in branches:
        histos[leaf] = []
    
    fileList = getListFiles(folderName) # get the list of the root files in the folderName folder
    fileList.sort()
    #nbFiles = 10 # nb of files to be used
    fileList = fileList[0:nbFiles]
    print(fileList)

    for elem in fileList:
        input_file = folderName + str(elem.split()[0])
        print('\n' + input_file)
        name_1 = input_file.replace(folderName, '').replace('DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO_', '').replace('.root', '')
        print ("name_1 : %s" % name_1)
        
        f_root = ROOT.TFile(input_file) # 'DATA/' + 
        h1 = getHisto(f_root, tp_1)
        #h1.ls()
        for leaf in branches:
            print("== %s ==" % leaf)
            temp_leaf = []
            histo = h1.Get(leaf)
            #histo_nb_x = histo.GetXaxis().GetNbins()+1 # not used

            temp_leaf.append(histo.GetMean()) # 0
            temp_leaf.append(histo.GetMeanError()) # 2
            temp_leaf.append(histo.GetStdDev()) # 6
            temp_leaf.append(histo.GetEntries()) # 6b

            temp_leaf.append(name_1) # 7
            
            texttoWrite = ''
            i=0
            for entry in histo:
                #print("%d/%d : %s - %s - %s") % (i, histo_nb_x, histo.GetXaxis().GetBinCenter(i), entry, histo.GetBinError(i))
                texttoWrite += 'b_' + '{:03d}'.format(i) + ',c_' + '{:03d},'.format(i)
                temp_leaf.append(entry) # b_
                temp_leaf.append(histo.GetBinError(i)) # c_
                i+=1
            texttoWrite = texttoWrite[:-1] # remove last char
            temp_leaf.append(texttoWrite) # end
            histos[leaf].append(temp_leaf)

    #print histos into histo named files
    i_leaf = 0
    for leaf in branches:
        wr.append(open(folderName + 'histo_' + str(leaf) + '_' + '{:03d}'.format(nbFiles) + '_0_lite.txt', 'w'))
        nb_max = len(histos[leaf][0]) - 1
        print("nb_max : %d" % nb_max)
        wr[i_leaf].write('evol,Mean,MeanError,StdDev,nbBins,name,')
        wr[i_leaf].write(str(histos[leaf][0][nb_max]))
        wr[i_leaf].write('\n')
        #'''
        for i_file in range(0, len(fileList)):
            texttoWrite = str(i_file) + ','
            wr[i_leaf].write(texttoWrite) 
            for i in range(0, nb_max-1):
                #print('i : %d' % i)
                wr[i_leaf].write(str(histos[leaf][i_file][i]))
                wr[i_leaf].write(',')
            wr[i_leaf].write(str(histos[leaf][i_file][nb_max-1]))
            texttoWrite = '\n'
            wr[i_leaf].write(texttoWrite) 
        wr[i_leaf].close()
        i_leaf +=1
        #'''
    return

def func_CreateKS(br, nbFiles):
    print("func_Extract")
    
    branches = br
    N_histos = len(branches)
    print('N_histos : %d' % N_histos)
    
    # nb of bins for sampling
    nbins = 100 
    
    # create folder 
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
        except OSError as e:
            if e.errno != errno.EEXIST: # the folder did not exist
                raise  # raises the error again
        print('Creation of %s release folder\n' % folder)
    else:
        print('Folder %s already created\n' % folder)

    # get the "new" root file datas
    #input_rel_file = 'DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO_9000_new.root'
    #input_rel_file = 'DATA/DQM_V0001_R000000001__RelValZEE_14__CMSSW_11_2_0-112X_mcRun3_2021_realistic_v13-v1__DQMIO.root'
    #input_rel_file = 'DATA/DQM_V0001_R000000001__RelValZEE_14__CMSSW_11_3_0_pre2-113X_mcRun3_2021_realistic_v2_rsb-v1__DQMIO.root'
    #input_rel_file = 'DATA/DQM_V0001_R000000001__RelValZEE_14__CMSSW_11_3_0_pre3-113X_mcRun3_2021_realistic_v4-v1__DQMIO.root'
    input_rel_file = 'DATA/DQM_V0001_R000000001__RelValZEE_14__CMSSW_11_3_0_pre6-113X_mcRun3_2021_realistic_v9-v1__DQMIO.root'
    #input_rel_file = 'DATA/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO_9000_056.root'
    f_rel = ROOT.TFile(input_rel_file)

    #input_ref_file = 'DATA/DQM_V0001_R000000001__RelValZEE_14__CMSSW_11_2_0_pre11-112X_mcRun3_2021_realistic_v13-v1__DQMIO.root'
    #input_ref_file = 'DATA/DQM_V0001_R000000001__RelValZEE_14__CMSSW_11_3_0_pre1-113X_mcRun3_2021_realistic_v1-v1__DQMIO.root'
    #input_ref_file = 'DATA/DQM_V0001_R000000001__RelValZEE_14__CMSSW_11_3_0_pre2-113X_mcRun3_2021_realistic_v2_rsb-v1__DQMIO.root'
    #input_ref_file = 'DATA/DQM_V0001_R000000001__RelValZEE_14__CMSSW_11_3_0_pre4-113X_mcRun3_2021_realistic_v4-v1__DQMIO.root'
    input_ref_file = 'DATA/DQM_V0001_R000000001__RelValZEE_14__CMSSW_11_3_0_pre5-113X_mcRun3_2021_realistic_v7-v1__DQMIO.root'
    #input_ref_file = 'DATA/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO_9000_017.root'
    f_ref = ROOT.TFile(input_ref_file)

    nb_red1 = 0
    nb_green1 = 0
    nb_red2 = 0
    nb_green2 = 0
    nb_red3 = 0
    nb_green3 = 0

    for i in range(0, N_histos): # 1 histo for debug
        if (branches[i] == 'h_ele_seedMask_Tec'): # temp (pbm with nan)
            i += 1
        name = folderName + "histo_" + branches[i] + '_{:03d}'.format(nbFiles) + "_0_lite.txt"
        print('\n%d - %s' %(i, name))
        df = pd.read_csv(name)
        
        h1 = getHisto(f_rel, tp_1)
        #print("h1")
        #print(h1)
        print(branches[i]) # print histo name
        histo_1 = h1.Get(branches[i])
        ii=0
        s_new = []
        e_new = []
        for entry in histo_1:
            #print("%d/%d : %s - %s") % (ii, histo_1.GetXaxis().GetNbins(), entry, histo_1.GetBinError(i))
            s_new.append(entry)
            e_new.append(histo_1.GetBinError(ii))
            ii += 1
        s_new = np.asarray(s_new)
        s_new = s_new[1:-1]
        e_new = e_new[1:-1]
        #print(s_new)
        #print(e_new)
        Ntot_h1 = histo_1.GetEntries()

        h2 = getHisto(f_ref, tp_1)
        #print("h2")
        #print(h2)
        print(branches[i]) # print histo name
        histo_2 = h2.Get(branches[i])
        ii=0
        s_old = []
        e_old = []
        for entry in histo_2:
            #print("%d/%d : %s - %s") % (ii, histo_2.GetXaxis().GetNbins(), entry, histo_2.GetBinError(i))
            s_old.append(entry)
            e_old.append(histo_2.GetBinError(ii))
            ii += 1
        s_old = np.asarray(s_old)
        s_old = s_old[1:-1]
        e_old = e_old[1:-1]
        #print(s_old)
        #print(e_old)
        Ntot_h2 = histo_2.GetEntries()
        print('Ntot_h1 : %d - Ntot_h2 : %d' % (Ntot_h1, Ntot_h2))

        # print min/max for the new curve
        print('\n##########')
        print('min : %f' % s_new.min())
        print('max : %f' % s_new.max())
        print('###########\n')
        if (s_new.min() < 0.):
            print('pbm whith histo %s, min < 0' % branches[i])
            continue
        if (np.floor(s_new.sum()) == 0.):
            print('pbm whith histo %s, sum = 0' % branches[i])
            continue

        # create file for KS curve
        #KSname1 = folder + "histo_" + branches[i] + '_{:03d}'.format(nbFiles) + "_KScurve1.txt"
        KSname1 = folder + "histo_" + branches[i] + "_KScurve1.txt"
        print("KSname 1 : %s" % KSname1)
        wKS1 = open(KSname1, 'w')
        #KSname2 = folder + "histo_" + branches[i] + '_{:03d}'.format(nbFiles) + "_KScurve2.txt"
        KSname2 = folder + "histo_" + branches[i] + "_KScurve2.txt"
        print("KSname 2 : %s" % KSname2)
        wKS2 = open(KSname2, 'w')
        #KSname3 = folder + "histo_" + branches[i] + '_{:03d}'.format(nbFiles) + "_KScurve3.txt"
        KSname3 = folder + "histo_" + branches[i] + "_KScurve3.txt"
        print("KSname 3 : %s" % KSname3)
        wKS3 = open(KSname3, 'w')

        # check the values & errors data
        #print(df.head(5))
        cols = df.columns.values
        n_cols = len(cols)
        print('nb of columns for histos : %d' % n_cols)
        cols_entries = cols[6::2]
        df_entries = df[cols_entries]
        #print(df_entries.head(15))#

        # nbBins (GetEntries())
        df_GetEntries = df['nbBins']
        #print(df_GetEntries.head(15))

       # get nb of columns & rows for histos
        (Nrows, Ncols) = df_entries.shape
        print('[Nrows, Ncols] : [%d, %d]' % (Nrows, Ncols))
        df_entries = df_entries.iloc[:, 1:Ncols-1]
        (Nrows, Ncols) = df_entries.shape
        print('[Nrows, Ncols] : [%d, %d]' % (Nrows, Ncols))

        # create the datas for the p-Value graph
        # by comparing all curves between them. (KS 1)
        nb1 = 0
        totalDiff = []
        for k in range(0,Nrows-1):
            for l in range(k+1, Nrows):
                nb1 += 1
                series0 = df_entries.iloc[k,:]
                series1 = df_entries.iloc[l,:]     
                sum0 = df_GetEntries[k]
                sum1 = df_GetEntries[l]
                totalDiff.append(diffMAXKS(series0, series1, sum0, sum1)[0]) # 9000, 9000

        print('ttl nb1 of couples : %d' % nb1)

        # create the datas for the p-Value graph
        # by comparing 1 curve with the others.
        # Get a random histo as reference (KS 2)
        ind_reference = np.random.randint(0, Nrows)
        print('reference ind. : %d' % ind_reference)
        series_reference = df_entries.iloc[ind_reference,:]
        nbBins_reference = df_GetEntries[ind_reference]
        print('nb bins reference : %d' % nbBins_reference)
        #print(series_reference)
        nb2 = 0
        totalDiff2 = []
        for k in range(0,Nrows-0):
            if (k != ind_reference):
                nb2 += 1
                series0 = df_entries.iloc[k,:]
                sum0 = df_GetEntries[k]
                totalDiff2.append(diffMAXKS(series0, series_reference, sum0, nbBins_reference)[0]) # 9000, 9000

        print('ttl nb of couples : %d' % nb2)
        #stop
    
        # create the datas for the p-Value graph
        # by comparing the new curve with the others.
        # Get the new as reference (KS 3)
        #print("s_new : ")
        #print(s_new)
        nb3 = 0
        totalDiff3 = []
        for k in range(0,Nrows-0):
            nb3 += 1
            series0 = df_entries.iloc[k,:]
            sum0 = df_GetEntries[k]
            totalDiff3.append(diffMAXKS(series0, s_new, sum0, Ntot_h1)[0])

        print('ttl nb of couples : %d' % nb3)
    
        # plot some datas (in fact doing nothing but creating fig)
        plt_entries = df_entries.plot(kind='line')
        fig = plt_entries.get_figure()
        fig.clf()
        # create the integrated curve
        curves = []
        for k in range(0,Nrows):
            series0 = df_entries.iloc[k,:]
            curves = funcKS(series0)
            plt.plot(curves)
        #fig.savefig(folder + '/cumulative_curve_' + branches[i] + '_{:03d}'.format(nbFiles) + '.png')
        fig.savefig(folder + '/cumulative_curve_' + branches[i] + '.png')
        fig.clf()
    
        # ================================ #
        # create the mean curve of entries #
        # ================================ #
        mean_df_entries = df_entries.mean()
        mean_sum = mean_df_entries.sum()
        #mean_df_errors = df_errors.mean()
        diffMax1, posMax1, sDKS = diffMAXKS(mean_df_entries, s_new, mean_sum, Ntot_h1)
        diffMax2, posMax2, sDKS = diffMAXKS(series_reference, s_new, nbBins_reference, Ntot_h1)
        diffMax3, posMax3, sDKS = diffMAXKS(s_new, s_old, Ntot_h1, Ntot_h2)
        print("diffMax1 : %f - posMax1 : %f" % (diffMax1, posMax1))
        print("diffMax2 : %f - posMax2 : %f" % (diffMax2, posMax2))
        print("diffMax3 : %f - posMax3 : %f" % (diffMax3, posMax3))
        print('Ntot_h1 : %d - Ntot_h2 : %d' % (Ntot_h1, Ntot_h2))

        # diff max between new & old
        diffMax0, posMax0, sDKS = diffMAXKS(s_old, s_new, Ntot_h2, Ntot_h1)
        print("diffMax0 : %f - posMax0 : %f" % (diffMax0, posMax0))
        print(s_new[0:8])
        print(s_old[0:8])
        print(sDKS[0:8]) # diff

        yellowCurve1 = mean_df_entries
        yellowCurve2 = series_reference
        yellowCurve3 = s_new
        yellowCurveCum1 = funcKS(mean_df_entries) #  cumulative yellow curve
        yellowCurveCum2 = funcKS(series_reference)
        yellowCurveCum3 = funcKS(s_new)

        # Kolmogoroff-Smirnov curve
        seriesTotalDiff = pd.DataFrame(totalDiff, columns=['KSDiff'])
        plt_diff_KS1 = seriesTotalDiff.plot.hist(bins=nbins, title='KS diff.')
        if (diffMax0 >= seriesTotalDiff.values.max()):
            color1 = 'r'
            nb_red1 += 1
            x1 = seriesTotalDiff.values.max()
        elif (diffMax0 <= seriesTotalDiff.values.min()):
            color1 = 'r'
            nb_red1 += 1
            x1 = seriesTotalDiff.values.min()
        else:
            color1 = 'g'
            nb_green1 += 1
            x1 = diffMax0
        ymi, yMa = plt_diff_KS1.get_ylim()
        plt_diff_KS1.vlines(x1, ymi, 0.9*yMa, color=color1, linewidth=4)
        fig = plt_diff_KS1.get_figure()
        #fig.savefig(folder + '/KS-ttlDiff_1_' + branches[i] + '_{:03d}'.format(nbFiles) + '.png')
        fig.savefig(folder + '/KS-ttlDiff_1_' + branches[i] + '.png')
        fig.clf()
        #count, division = np.histogram(seriesTotalDiff, bins=nbins)
        count, division = np.histogram(seriesTotalDiff[~np.isnan(seriesTotalDiff)], bins=nbins)
        div_min = np.amin(division)
        div_max = np.amax(division)

        # Get the max of the integral
        I_max = integralpValue(division, count, 0.)
        print('\nMax. integral : %0.4e for nbins=%d' % (I_max, nbins))
        # print the min/max values of differences
        print('Kolmogoroff-Smirnov min value : %0.4e - max value : %0.4e | diff value : %e \n' % (div_min, div_max, x1))
        #stop
        # save the KS curves
        wKS1.write('%e, %d\n' % (I_max, nbins))
        wKS1.write('%e, %e\n' % (div_min, div_max))
        wKS1.write(' '.join("{:10.04e}".format(x) for x in count))
        wKS1.write('\n')
        wKS1.write(' '.join("{:10.04e}".format(x) for x in division))
        wKS1.write('\n')
        wKS1.write(' '.join("{:10.04e}".format(x) for x in yellowCurve1 )) # average (mean) curve
        wKS1.write('\n')
        wKS1.write(' '.join("{:10.04e}".format(x) for x in yellowCurveCum1 ))
        wKS1.write('\n')
        wKS1.close()

        # Kolmogoroff-Smirnov curve 2
        seriesTotalDiff2 = pd.DataFrame(totalDiff2, columns=['KSDiff'])
        plt_diff_KS2 = seriesTotalDiff2.plot.hist(bins=nbins, title='KS diff. 2')
        if (diffMax0 >= seriesTotalDiff2.values.max()):
            color2 = 'r'
            nb_red2 += 1
            x2 = seriesTotalDiff2.values.max()
        elif (diffMax0 <= seriesTotalDiff2.values.min()):
            color2 = 'r'
            nb_red2 += 1
            x2 = seriesTotalDiff2.values.min()
        else:
            color2 = 'g'
            nb_green2 += 1
            x2 = diffMax0
        ymi, yMa = plt_diff_KS2.get_ylim()
        plt_diff_KS2.vlines(x2, ymi, 0.9*yMa, color=color2, linewidth=4)
        fig = plt_diff_KS2.get_figure()
        #fig.savefig(folder + '/KS-ttlDiff_2_' + branches[i] + '_{:03d}'.format(nbFiles) + '.png')
        fig.savefig(folder + '/KS-ttlDiff_2_' + branches[i] + '.png')
        fig.clf()
        count, division = np.histogram(seriesTotalDiff2, bins=nbins)
        div_min = np.amin(division)
        div_max = np.amax(division)
    
        # Get the max of the integral
        I_max = integralpValue(division, count, 0.)
        print('\nMax. integral : %0.4e for nbins=%d' % (I_max, nbins))
        # print the min/max values of differences
        print('Kolmogoroff-Smirnov min value : %0.4e - max value : %0.4e | diff value : %e \n' % (div_min, div_max, x2))
        #stop
        # save the KS curves
        wKS2.write('%e, %d\n' % (I_max, nbins))
        wKS2.write('%e, %e\n' % (div_min, div_max))
        wKS2.write(' '.join("{:10.04e}".format(x) for x in count))
        wKS2.write('\n')
        wKS2.write(' '.join("{:10.04e}".format(x) for x in division))
        wKS2.write('\n')
        wKS2.write(' '.join("{:10.04e}".format(x) for x in yellowCurve2 )) # random curve
        wKS2.write('\n')
        wKS2.write(' '.join("{:10.04e}".format(x) for x in yellowCurveCum2 ))
        wKS2.write('\n')
        wKS2.close()

        # Kolmogoroff-Smirnov curve 3
        seriesTotalDiff3 = pd.DataFrame(totalDiff3, columns=['new'])
        plt_diff_KS3 = seriesTotalDiff3.plot.hist(bins=nbins, title='KS diff. 3')
        if (diffMax0 >= seriesTotalDiff3.values.max()):
            color3 = 'r'
            nb_red3 += 1
            x3 = 0.95 * seriesTotalDiff3.values.max()
        elif (diffMax0 <= seriesTotalDiff3.values.min()):
            color3 = 'r'
            nb_red3 += 1
            x3 = seriesTotalDiff3.values.min()
        else:
            color3 = 'g'
            nb_green3 += 1
            x3 = diffMax0
        ymi, yMa = plt_diff_KS3.get_ylim()
        plt_diff_KS3.vlines(x3, ymi, 0.9*yMa, color=color3, linewidth=4)
        fig = plt_diff_KS3.get_figure()
        #fig.savefig(folder + '/KS-ttlDiff_3_' + branches[i] + '_{:03d}'.format(nbFiles) + '.png')
        fig.savefig(folder + '/KS-ttlDiff_3_' + branches[i] + '.png')
        fig.clf()
        count, division = np.histogram(seriesTotalDiff3, bins=nbins)
        div_min = np.amin(division)
        div_max = np.amax(division)
    
        # Get the max of the integral
        I_max = integralpValue(division, count, 0.)
        print('\nMax. integral : %0.4e for nbins=%d' % (I_max, nbins))
        # print the min/max values of differences
        print('Kolmogoroff-Smirnov min value : %0.4e - max value : %0.4e | diff value : %e \n' % (div_min, div_max, x3))
        #stop

        plt.close('all')
        # save the KS curves
        wKS3.write('%e, %d\n' % (I_max, nbins))
        wKS3.write('%e, %e\n' % (div_min, div_max))
        wKS3.write(' '.join("{:10.04e}".format(x) for x in count))
        wKS3.write('\n')
        wKS3.write(' '.join("{:10.04e}".format(x) for x in division))
        wKS3.write('\n')
        wKS3.write(' '.join("{:10.04e}".format(x) for x in yellowCurve3 )) # new curve
        wKS3.write('\n')
        wKS3.write(' '.join("{:10.04e}".format(x) for x in yellowCurveCum3 ))
        wKS3.write('\n')
        wKS3.close()

    # print nb of red/green lines
    print('KS 1 : %d red - %d green' % (nb_red1, nb_green1))
    print('KS 2 : %d red - %d green' % (nb_red2, nb_green2))
    print('KS 3 : %d red - %d green' % (nb_red3, nb_green3))
    nb_red = nb_red1 + nb_red2 + nb_red3
    nb_green = nb_green1 + nb_green2 + nb_green3
    print('KS ttl : %d red - %d green' % (nb_red, nb_green))

    return

if __name__=="__main__":

    # get the branches for ElectronMcSignalHistos.txt
    branches = []
    branches = getBranches(tp_1)
    print(branches[0:10])
    print(branches[5])
    #branches = branches[0:60]

    # nb of files to be used
    nbFiles = 200 # 

    #func_Extract(branches, nbFiles) # create file with histo datas.

    func_CreateKS(branches[0:9], nbFiles) # create the KS files from histos datas for 5 datasets
    #func_CreateKS(branches, nbFiles)  # create the KS files from histos datas

    print("Fin !")

