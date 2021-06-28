# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 21:37:16 2021

@author: Vaibhav 301386847
"""

import sys
import pandas as pd
import numpy as np
import datetime as dt
from scipy import stats
import matplotlib.pyplot as plt


OUTPUT_TEMPLATE = (
    "Initial T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann-Whitney U-test p-value: {utest_p:.3g}"
)


def main():
    reddit_counts = sys.argv[1]
    counts = pd.read_json(reddit_counts, lines=True)
    
    #filter data for year 2012-2013 and subreddit = canada
    counts = counts[((counts['date'].dt.year == 2012) | (counts['date'].dt.year == 2013)) & (counts['subreddit'] == 'canada')]
    
    #separate  weekends from weekdays
    weekends = counts[((counts['date'].dt.weekday == 5) | (counts['date'].dt.weekday == 6))]
    weekdays = counts[~((counts['date'].dt.weekday == 5) | (counts['date'].dt.weekday == 6))]
    
    #Student's T-test
    initial_ttest_p = stats.ttest_ind(weekends['comment_count'],weekdays['comment_count']).pvalue
    initial_weekday_normality_p = stats.normaltest(weekdays['comment_count']).pvalue
    initial_weekend_normality_p = stats.normaltest(weekends['comment_count']).pvalue
    initial_levene_p = stats.levene(weekends['comment_count'], weekdays['comment_count']).pvalue
    
    #Fix 1 : Transforming data
    #plt.hist(weekdays['comment_count'])
    #plt.hist(weekends['comment_count'])
    
    #We use sqrt() to transform the data since thats when the data comes closes to normal distribution
    transformed_weekend = np.sqrt(weekends['comment_count'])
    transformed_weekend_normality_p = stats.normaltest(transformed_weekend).pvalue
    transformed_weekday = np.sqrt(weekdays['comment_count'])
    transformed_weekday_normality_p = stats.normaltest(transformed_weekday).pvalue
    transformed_levene_p = stats.levene(transformed_weekend,transformed_weekday).pvalue
    
    #Fix 2 : Central Limit Theorem
    weekends_iso = weekends['date'].dt.isocalendar()
    weekends_iso = weekends_iso[['year','week']]
    weekends = pd.concat([weekends,weekends_iso], axis=1)
    
    weekdays_iso = weekdays['date'].dt.isocalendar()
    weekdays_iso = weekdays_iso[['year','week']]
    weekdays = pd.concat([weekdays,weekdays_iso], axis=1)
    
    weekends_grouped = weekends.groupby(by=['year','week']).aggregate('mean').reset_index()
    weekdays_grouped = weekdays.groupby(by=['year','week']).aggregate('mean').reset_index()
    
    weekly_weekday_normality_p = stats.normaltest(weekdays_grouped['comment_count']).pvalue
    weekly_weekend_normality_p = stats.normaltest(weekends_grouped['comment_count']).pvalue
    weekly_levene_p = stats.levene(weekends_grouped['comment_count'],weekdays_grouped['comment_count']).pvalue  
    weekly_ttest_p = stats.ttest_ind(weekends_grouped['comment_count'],weekdays_grouped['comment_count']).pvalue
    
    #Fix 3 : Non-parametric test
    utest_p = stats.mannwhitneyu(weekends['comment_count'],weekdays['comment_count'], alternative='two-sided').pvalue
    
    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p = initial_ttest_p,
        initial_weekday_normality_p = initial_weekday_normality_p,
        initial_weekend_normality_p = initial_weekend_normality_p,
        initial_levene_p = initial_levene_p,
        transformed_weekday_normality_p = transformed_weekday_normality_p,
        transformed_weekend_normality_p = transformed_weekend_normality_p,
        transformed_levene_p = transformed_levene_p,
        weekly_weekday_normality_p = weekly_weekday_normality_p,
        weekly_weekend_normality_p = weekly_weekend_normality_p,
        weekly_levene_p = weekly_levene_p,
        weekly_ttest_p = weekly_ttest_p,
        utest_p = utest_p,
    ))


if __name__ == '__main__':
    main()
