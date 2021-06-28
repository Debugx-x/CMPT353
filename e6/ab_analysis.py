# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 03:06:59 2021

@author: Vaibhav 301386847
"""

import sys
import pandas as pd
from scipy.stats import mannwhitneyu, chi2_contingency



OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value:  {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value:  {more_searches_p:.3g} \n'
    '"Did more/less instructors use the search feature?" p-value:  {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value:  {more_instr_searches_p:.3g}'
)


def main():
    searchdata_file = sys.argv[1]
    searchdata = pd.read_json(searchdata_file, orient='records', lines=True)
    #filter to seprate odd and even uid 
    #src: https://www.geeksforgeeks.org/split-pandas-dataframe-by-column-value/
    filter = searchdata['uid'] % 2 == 0
    searchdata_even = searchdata[filter].reset_index().drop(['index'], axis=1)
    searchdata_odd = searchdata[~filter].reset_index().drop(['index'], axis=1)
    
    #seprate 0 and non-zero searches for even and odd cases 
    evensearch_zero = searchdata_even[searchdata_even['search_count']==0]
    evensearch_notzero = searchdata_even[searchdata_even['search_count']!=0] 
    oddsearch_zero = searchdata_odd[searchdata_odd['search_count']==0]
    oddsearch_notzero = searchdata_odd[searchdata_odd['search_count']!=0] 
    
    contigency = [[len(evensearch_notzero),len(evensearch_zero)],[len(oddsearch_notzero),len(oddsearch_zero)]]
    chi2, p, dof, ex = chi2_contingency(contigency)
    searches_p = mannwhitneyu(searchdata_even['search_count'],searchdata_odd['search_count']).pvalue
    
    #filter instructors
    instructor_even = searchdata_even[searchdata_even['is_instructor']==True]
    instructor_odd = searchdata_odd[searchdata_odd['is_instructor']==True]
    
    #seprate 0 and non-zero searches for even and odd uid instructors
    eveninstructor_zero = instructor_even[instructor_even['search_count']==0]
    eveninstructor_notzero = instructor_even[instructor_even['search_count']!=0] 
    oddinstructor_zero = instructor_odd[instructor_odd['search_count']==0]
    oddinstructor_notzero = instructor_odd[instructor_odd['search_count']!=0]
    
    contigency = [[len(eveninstructor_notzero),len(eveninstructor_zero)],[len(oddinstructor_notzero),len(oddinstructor_zero)]]
    chi2, instruct_p, dof, ex = chi2_contingency(contigency)
    instruct_searches_p = mannwhitneyu(instructor_even['search_count'],instructor_odd['search_count']).pvalue

    print(OUTPUT_TEMPLATE.format(
        more_users_p=p,
        more_searches_p=searches_p,
        more_instr_p=instruct_p,
        more_instr_searches_p=instruct_searches_p,
    ))


if __name__ == '__main__':
    main()
