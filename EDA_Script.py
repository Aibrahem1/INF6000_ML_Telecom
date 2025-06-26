#Importing and mainpulation, EDA script

import pandas as pd
# -- to be able to view the entire dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# --------------------------- Ookla Dataset --------------------------
#---Reading the CSV data into pandas dataframe
OOKLA_DATA = pd.read_csv('Datasets/Ookla Rawdata.csv')
#---Data Exploration
OOKLA_DATA.head(10)
OOKLA_DATA.columns
OOKLA_DATA.dtypes
OOKLA_DATA.tail(10)
# ------ Subsetting the dataset to focus on Country: libya and ISPname : Libyana
# -- to use logical_and in numpy package
import numpy as np
# -- Libyana Only
OOKLA_DATA_LIBYANA = OOKLA_DATA[np.logical_and(OOKLA_DATA['country']=='Libya',
                                               OOKLA_DATA['ispName']=='Libyana')]
# - Exploration Libyana Subset
OOKLA_DATA_LIBYANA['testId'].count() # 74929 observations
OOKLA_DATA.head(10)
OOKLA_DATA_LIBYANA.columns
OOKLA_DATA_LIBYANA.dtypes
OOKLA_DATA_LIBYANA.sample
OOKLA_DATA_LIBYANA.index
# - Libyana Subset categorical Variables
OOKLA_DATA_LIBYANA
OOKLA_DATA_LIBYANA['connectionType'].unique()
OOKLA_DATA_LIBYANA['connectionType'].nunique()
#---
for col in OOKLA_DATA_LIBYANA.select_dtypes(include='object').columns:
    print(f"\n--- {col} ---")
    print(OOKLA_DATA[col].value_counts(dropna=False))

# -- Libyana, LTT and Almadar
OOKLA_DATA_LIBYA_MNO = OOKLA_DATA[np.logical_and(OOKLA_DATA['country']=='Libya',
                                               OOKLA_DATA['ispName'].isin(['Libyana',
                                                                           'LTT',
                                                                           'Almadar Aljadid']))]
# - Exploring Libya MNO Subset
OOKLA_DATA_LIBYA_MNO
OOKLA_DATA_LIBYA_MNO['testId'].count() #206286 observations
# WRITING DATA TO DISK
OOKLA_DATA_LIBYANA.to_csv('exports/OOKLA DATA LIBYANA.csv')
OOKLA_DATA_LIBYA_MNO.to_csv('exports/ookla data libya mno.csv')

# -- Subsetting using alternative approach # Example
OOKLA_DATA_TEST = OOKLA_DATA.loc[(OOKLA_DATA['country']=='Libya') &
                                    (OOKLA_DATA['ispName'].isin(['Libyana', 'LTT','Almadar Aljadid']))]

# -- Alternative subsetting
OOKLA_DATA_LY=OOKLA_DATA[OOKLA_DATA.loc[:,'country']=='Libya'] # subsetting the country
OOKLA_DATA_LYN=OOKLA_DATA_LY[OOKLA_DATA_LY.loc[:,'ispName']=='Libyana'] # Subsetting the isp into the subsetted country
## Correlation for Ookla data analysis

