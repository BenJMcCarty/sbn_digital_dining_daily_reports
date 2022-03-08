def cleaning_two(file_path):



    df = pd.read_excel(file_path, skiprows = 2)

    df.columns = ['Label', *df.columns[:-1]]

    col_labels = ['Label', 'Bar', 'Dining Room', 'Room Service', 'Starbucks']
    drop_cols = []

    for col in df.columns:
        if col not in col_labels:
            drop_cols.append(col)

    df = df.drop(columns = drop_cols)

    df_cleaned = df[df.isna().sum(axis=1) == 0]
    df_cleaned = df_cleaned[~df_cleaned.loc[:, "Label"].isin([' '])]
    df_cleaned = df_cleaned.reset_index(drop=True)

    df_all_cols = df_cleaned.copy().T

    df_all_cols.columns = df_all_cols.iloc[0]
    df_all_cols = df_all_cols.drop(index = 'Label')

    daily_rows = ['Food', 'Beverage', 'Other', 'Discount', 'MD Food 6%',
              'MD Liq 9%', 'Tip collected', "ALL A&G CHRG", 'Room Charge',
              'American Express', 'Cash', 'Discover Card', 'MasterCard', 'Visa']

    df_daily = df_all_cols[daily_rows]

    for col in df_daily.columns:
        df_daily.loc[:,col] = pd.to_numeric(df_daily.loc[:,col], downcast = 'float')

    daily_food = df_daily['Food'] + df_daily['Other'] - df_daily['Discount']

    daily_tax = df_daily['MD Food 6%']+df_daily['MD Liq 9%']

    summary = pd.concat([daily_food, df_daily['Beverage'], daily_tax, 
           df_daily['Tip collected']], axis=1)
    
    col_labels = {0: "Food", 1: "Tax", 'Tip collected': 'Gratuity'}

    row_labels = {'Bar': "Lobby Bar", "Dining Room": 'Rain 903', 
              'Room Service': 'In-Room Dining', 'Starbucks': 'Coffee Corner'}

    summary = summary.rename(columns = col_labels, index = row_labels)

    summary = summary.applymap(lambda x: round(x, 2))

    summary.to_excel('Test_Summary_Workbook.xlsx')