## Script to generate summary stats for Digital Dining daily sales reports
## Author: Ben McCarty (bmccarty505@gmail.com)
## Date: 4.19.22

import pandas as pd
import logging


def workflow(data_filepath, summary_file_name, receipts_filepath, log_filepath, mop_name = None):
    """Processes entire workflow to generate summary data for Digital Dining reports.

    Reads files; cleans; summarizes by MOP; generates log files to confirm any issues.

    Args:
        data_filepath (str): Path to data file (.xls/.xlsx files only)
        summary_file_name (str): Name for results file
        receipts_filepath (str): Receipts Audit report file
        log_filepath (str): Name for log file.
    """

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', 
                        datefmt='%d-%b-%y %H:%M:%S',filename=log_filepath,
                        encoding='utf-8',  filemode='a')

    # Create logger and set level
    logger = logging.getLogger('Report_Log')
    logger.setLevel(logging.INFO)

    # Create log file handler
    fh = logging.FileHandler(log_filepath)
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)



    ## Read all columns from file (incl. empty columns)
    df = pd.read_excel(data_filepath, engine = 'xlrd',  skiprows = 2)

    ## Shifting label names one to the right and drop extra column
    df.columns = ['Label', *df.columns[:-1]]

    ## Creating list of columns to keep/drop
    col_labels = ['Label', 'Bar', 'Dining Room', 'Room Service', 'Starbucks']
    drop_cols = []

    for col in df.columns:
        if col not in col_labels:
            drop_cols.append(col)

    ## Dropping columns not representing an outlet
    df = df.drop(columns = drop_cols)

    df_cleaned = df[df.isna().sum(axis=1) == 0]
    df_cleaned = df_cleaned[~df_cleaned.loc[:, "Label"].isin([' '])]
    df_cleaned = df_cleaned.reset_index(drop=True)

    df_all_cols = df_cleaned.copy().T
    df_all_cols

    ## Re-labeling columns based on "Label" row
    df_all_cols.columns = df_all_cols.iloc[0]
    df_all_cols = df_all_cols.drop(index = 'Label')

    daily_rows = ['Food', 'Beverage', 'Other', 'Discount', 'MD Food 6%',
                'MD Liq 9%', 'Tip collected', "ALL A&G CHRG", 'Room Charge',
                'American Express', 'Cash', 'Discover Card', 'MasterCard', 'Visa']

    df_daily = df_all_cols[daily_rows]

    ## Converting data to "float"
    # for col in df_daily.columns:
    #     df_daily.loc[:,col] = pd.to_numeric(df_daily.loc[:,col], downcast = 'float')
    df_daily = df_daily.applymap(lambda x: float(x))

    ## Summarize food charges by outlet
    daily_food = df_daily['Food'] + df_daily['Other'] - df_daily['Discount']

    ## Summarize tax charges by outlet
    daily_tax = df_daily['MD Food 6%']+df_daily['MD Liq 9%']

    ## Summarize all charges by outlet
    summary = pd.concat([daily_food, df_daily['Beverage'], daily_tax, 
            df_daily['Tip collected']], axis=1)

    ## Creating new labels
    col_labels = {0: "Food", 1: "Tax", 'Tip collected': 'Gratuity'}
    row_labels = {'Bar': "Lobby Bar", "Dining Room": 'Rain 903', 
                'Room Service': 'In-Room Dining', 'Starbucks': 'Coffee Corner'}

    ## Renaming columns
    summary = summary.rename(columns = col_labels, index = row_labels)

    ## Rounding values - preventing long numbers
    summary = summary.applymap(lambda x: round(x, 2))

    ## Generate new index to group MOPs
    if mop_name != None:
        summary.loc[:,'Payment'] = mop_name.upper()
        summary = summary.reset_index()
        summary = summary.rename(columns = {'index':'Outlet'})
        summary = summary.set_index(['Payment', 'Outlet'])

    summary.to_excel(summary_file_name)

    ra_rc_df = pd.read_excel(io = receipts_filepath, header = None, skiprows = 1,
                        names = ['Table #', 'Check #', 'Server #', 'Server Name', 'Cashier #',
                                'Cashier Name','MoP', 'Profit Center', 'Blank1', 'Blank2',
                                'Tip', 'Total Receipt', 'Guest Name/Room', 'Date', 'Time'])
    
    ## Dropping total rows at end of report
    ra_rc_df = ra_rc_df[:-3]

    bool_idx = ra_rc_df.loc[:,'Guest Name/Room'].str.startswith(('A&G', 'Dup'))

    chk_num = list(ra_rc_df[bool_idx]['Check #'].values)

    if len(chk_num) >0:
        logger.warning(f'Review checks for possible errors: {chk_num}')
    else:
        logger.info(f'There are no checks to review.')

    return summary


## Function not working - not creating/concatenating multi-index
# def loop_workflow(summary_file_name, receipts_filepath, log_filepath):
    
#     list_mops = ['ag', 'rc', 'ax', 'ca', 'di', 'vimc']

#     new_results = []
#     for mop in list_mops:
#         file_path = f'./data/02_25_2022_mop_det_{mop}.xls'
#         summary_file_name = f'results_for_{mop}.xlsx'
#         new_results.append(workflow(data_filepath = file_path, mop_name = mop,
#                                     summary_file_name = summary_file_name,
#                                     receipts_filepath = receipts_filepath,
#                                     log_filepath = log_filepath))

#     new_results_df = pd.concat(new_results, axis = 0)

#     return new_results_df