

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 15th May 2018

@authors: Zheng Zhang with Louis Felix Nothias, University of California San Diego
@purpose: convert MS2LDA CSV table (http://ms2lda.org) All Fragmentation Spectra and Mass2Motifs matching details) to a format that can be mapped in GNPS molecular networks (http://gnps.ucsd.edu) viewed in Cytoscape
"""

import sys
import os
import argparse
import csv
import pandas as pd
import math


def main():

    #parse in all the parameters
    parser = argparse.ArgumentParser(description='Running converter')
    parser.add_argument('input', help='input.csv')
    args = parser.parse_args()
    inputf = args.input

    #creating a dictionary and sort by ids
    df1 = pd.read_csv(inputf)
    df1 = df1.sort_values('Document',ascending=True)

    # count id numbers
    oldid=0
    idList = []
    for i in range(len(df1)):
        if df1['Document'][i] != oldid:
            oldid = df1['Document'][i]
            idList.append(oldid)


    #iterate through dataframe and combine rows
    df2 = pd.DataFrame(columns=['Document','Motif','Probability',\
          'Overlap Score','Precursor Mass','Retention Time',\
          'Document Annotation','Motif_consensus','Motif_2','Proba_2',\
          'Overl_2','Motif_3','Proba_3','Overl_3','Motif_4','Proba_4',\
          'Overl_4','Motif_5','Proba_5','Overl_5','Motif_6','Proba_6',\
          'Overl_6','Motif_7','Proba_7','Overl_7','Motif_8','Proba_8',\
          'Overl_8','Motif_9','Proba_9','Overl_9'])
    #df2['id'] = idList
    df2['Document'] = idList
    oldid=0
    id_counter = -1
    counter =0
    for i in range(len(df1)):
        if df1['Document'][i] == oldid and counter <9:
            counter = counter+1
            df2.iloc[id_counter,2+counter*3] =  df1['Motif'][i]
            df2.iloc[id_counter,3+counter*3] =  df1['Probability'][i]
            df2.iloc[id_counter,4+counter*3] =  df1['Overlap Score'][i]
        if df1['Document'][i] != oldid:
            counter=1
            if id_counter !=-1:
                mflist =[df2['Motif'][id_counter],df2['Motif_2'][id_counter],\
                        df2['Motif_3'][id_counter],df2['Motif_4'][id_counter],\
                        df2['Motif_5'][id_counter],df2['Motif_6'][id_counter],\
                        df2['Motif_7'][id_counter],df2['Motif_8'][id_counter],\
                        df2['Motif_9'][id_counter]]
                mflist  = list(filter(lambda a: a == a, mflist))
                if len(mflist) > 1:
                    df2['Motif_consensus'][id_counter]=','.join(mflist)
                else:
                    df2['Motif_consensus'][id_counter] = mflist[0]
            id_counter = id_counter+1
            oldid = df1['Document'][i]
            df2['Document'][id_counter] =  df1['Document'][i]
            df2['Motif'][id_counter] =  df1['Motif'][i]
            df2['Overlap Score'][id_counter] =  df1['Overlap Score'][i]
            df2['Probability'][id_counter] =  df1['Probability'][i]
            df2['Precursor Mass'][id_counter] =  df1['Precursor Mass'][i]
            df2['Retention Time'][id_counter] =  df1['Retention Time'][i]
            df2['Document Annotation'][id_counter] =  df1['Document Annotation'][i]
        if i == len(df1)-1:
            mflist = [df2['Motif'][id_counter],df2['Motif_2'][id_counter],df2['Motif_3'][id_counter],df2['Motif_4'][id_counter]]
            mflist  = list(filter(lambda a: a == a, mflist))
            if len(mflist) > 1:
                df2['Motif_consensus'][id_counter]=','.join(mflist)
            else:
                df2['Motif_consensus'][id_counter] = mflist[0]
    # Quick fix LF
    df2['Document']= df2['Document'].str.split('_').str[-1]
    df3 = df2.set_index(["Document"])
    df3['Motif'] = df3['Motif'].str.replace('motif_','M')
    df3['Motif_consensus'] = df3['Motif_consensus'].str.replace('motif_','M')
    df3['Motif_2'] = df3['Motif_2'].str.replace('motif_','M')
    df3['Motif_3'] = df3['Motif_3'].str.replace('motif_','M')
    df3['Motif_4'] = df3['Motif_4'].str.replace('motif_','M')
    df3['Motif_5'] = df3['Motif_5'].str.replace('motif_','M')
    df3['Motif_6'] = df3['Motif_6'].str.replace('motif_','M')
    df3['Motif_7'] = df3['Motif_7'].str.replace('motif_','M')
    df3['Motif_8'] = df3['Motif_8'].str.replace('motif_','M')
    df3['Motif_9'] = df3['Motif_9'].str.replace('motif_','M')

    print (df3)
    df3.to_csv(str(inputf)+'_output.csv', sep='\t')
if __name__=="__main__":
    main()
