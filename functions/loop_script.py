## Looping through workflow

import pandas as pd
from functions.script import workflow

def loop_workflow(summary_file_name, receipts_filepath, log_filepath):

    
    list_mops = ['ag', 'rc', 'ax', 'ca', 'di', 'vimc']
    new_results = []
    for mop in list_mops:
        file_path = f'./data/02_25_2022_mop_det_{mop}.xls'
        summary_file_name = f'results_for_{mop}.xlsx'
        new_results.append(workflow(data_filepath = file_path, summary_file_name = summary_file_name,
                                    receipts_filepath = receipts_filepath, log_filepath = log_filepath))
        
    new_results_df = pd.concat(new_results)

    return new_results_df