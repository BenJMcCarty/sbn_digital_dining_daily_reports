## --- Functionizing Cleaning Function for DD-DRR --- ##

## --- Importing Packages --- ##

## --- Importing Packages --- ##

import numpy as np
import pandas as pd


def clean_data_old(file_path):
    """Work flow to import, clean, and eventually save the results as a new report.

    Args:
        file_path (string): file path for the original profit center report
    """    

    ## --- Read specific columns from Excel file --- ##

    df = pd.read_excel(file_path, header = None, skiprows = 3,
                    usecols = 'A, B, D, F, H', 
                    names = ['Label', 'Lounge', 'Rain 903', 'In-Room Dining',
                                'Coffee Corner'])
    # df

    ## --- How many rows have missing values, and how many? --- ##

    # df.isna().sum(axis=1).value_counts()

    ## --- Filter out those rows with missing values --- ##

    df_cleaned = df[df.isna().sum(axis=1) ==0]
    df_cleaned = df_cleaned.reset_index(drop=True)
    # df_cleaned

    ## --- Create new DF to allow for later reuse --- ##

    df_no_drp = df_cleaned.copy()
    # df_no_drp

    ## --- Dropping blank rows --- ##

    df_no_drp = df_no_drp[~df_no_drp.loc[:, "Label"].isin([' '])]
    # df_no_drp

    ## --- Relabel and reset index with correct labels --- ##

    df_no_drp = df_no_drp.rename(df_no_drp["Label"])
    df_no_drp = df_no_drp.drop(columns = "Label")
    # df_no_drp

    ## --- Review datatypes --- ##

    df_no_drp.dtypes

    ## --- Recast columns to "float" datatype & review --- ##

    for col in df_no_drp.columns:
        df_no_drp[col] = pd.to_numeric(df_no_drp[col], downcast = 'float')

    # print(df_no_drp.dtypes)

    # display(df_no_drp)

    # ## --- Inspect results --- ##

    # df_no_drp.T.describe().T

    # ## --- Create new total column --- ##

    # df_no_drp['Total'] = df_no_drp.sum(axis=1)
    # df_no_drp

    # ## --- Filter rows without any activity --- ##

    # df_no_zero = df_no_drp[df_no_drp['Total'] > 0]
    # df_no_zero

    return df_no_drp


def clean_data_test(file_path):
    """Work flow to import, clean, and eventually save the results as a new report.

    Args:
        file_path (string): file path for the original profit center report
    """    

    ## --- Read specific columns from Excel file --- ##

    df = pd.read_excel(file_path, skiprows = 2)

    ## --- Reassign label names: shifting to the right and dropping extra --- ##

    df.columns = ['Label', *df.columns[:-1]]
    ## --- Creating list of columns to keep/drop --- ##

    col_labels = ['Label', 'Bar', 'Dining Room', 'Room Service', 'Starbucks',
                'Page Total']

    drop_cols = []

    for col in df.columns:
        if col not in col_labels:
            drop_cols.append(col)
            
    ## --- Dropping columns not representing an outlet --- ##

    df = df.drop(columns = drop_cols)

    ## --- Filter out those rows with missing/blank values --- ##

    df_cleaned = df[df.isna().sum(axis=1) == 0]
    df_cleaned = df_cleaned[~df_cleaned.loc[:, "Label"].isin([' '])]
    df_cleaned = df_cleaned.reset_index(drop=True)

    ## --- Create new DF to allow for later reuse --- ##

    df_no_drp = df_cleaned.copy()

    ## --- Relabel and reset index with correct labels --- ##

    df_no_drp = df_no_drp.rename(df_no_drp["Label"])
    df_no_drp = df_no_drp.drop(columns = "Label")
    df_no_drp

    ## --- Recast columns to "float" datatype & review --- ##

    for col in df_no_drp.columns:
        df_no_drp[col] = pd.to_numeric(df_no_drp[col], downcast = 'float')
    
    ## --- Create list of frequently-used labels --- ##

    freq_cats = ['Food', 'Beverage', 'Other','Discount', 'Charge','MD Food 6%',
             'MD Liq 9%','Tip collected','ALL A&G CHRG', 'Room Charge',
             'American Express', 'Cash', 'Discover Card', 'MasterCard',
             'Visa']

    return df_no_drp