#Importing and mainpulation, EDA script

import pandas as pd
# -- to be able to view the entire dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# --------------------------- Libyana Ookla Dataset --------------------------
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



# --------------------------- Libyana LTE KPIs Dataset --------------------------
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
#---- LTE Data 1 year
LTE_DATA = pd.read_excel('Datasets/Libyana Dataset JUN25/History Query-LTE KPI one year daily.xlsx', sheet_name='Sheet0')
# Exploring
LTE_DATA['eNodeB Name'].nunique() #16 BTS sites
LTE_DATA['E-UTRAN FDD Cell Name'].unique() #168 Radio Cells

# == Select KEY Radio Features required for forecasting
LTE_DATA.columns

LTE_DATA1 = LTE_DATA[[
    #Time Stamp
    'Begin Time',
    'Granularity',
    # Target variables (choose one for Y)
    'PS Traffic Volume(GB)_ITBBU&SDR',
    'DL E-UTRAN IP Throughput(Mbps)_ITBBU&SDR',
    'Cell DL Average Aggregated Throughput(Mbps)',
    'DL PRB Utilization Rate(%)',
    # Load & Resource KPIs
    'UL PRB Utilization Rate(%)',
    'DL PRB Available (Bandwidth)',
    'Mean Number of RRC Connection User',
    'Maximum Active User Number on User Plane',
    'Maximum Number of RRC Connection User',
    # Quality KPIs
    'RRC Establishment Success Rate(%)',
    'E-RAB Setup Success Rate(%)',
    'E-RAB Drop Rate(%)',
    'RRC Drop Rate(%)',
    'Cell Uplink BLER(%)',
    'Cell Downlink BLER(%)',
    # RF/PHY Layer
    'DL Average MCS',
    'UL Average MCS',
    'Average CQI(N/A)',
    'Ratio of CQI>7 Percentage',
    'Ratio of CQI >= 10 (64QAM)',
    # Coverage and Interference
    'LTE Average TA(km)',
    'Average Cell RSSI(dBm)',
    'Ratio of SINR<-3dB',
    'Ratio of RSRP in Range of  [-110,-106]dBm',
    'Ratio of RSRP in Range of  [-115,-111]dBm',
    'Ratio of RSRP in Range of  [-120,-116]dBm',
    'Ratio of RSRP in Range of  [-140,-121]dBm',
    # Mobility
    'Success Rate of Outgoing Handover(Cell)(%)',
    'Success Rate of Intra-RAT Inter-frequency Cell Outgoing Handover(%)',
    'Number of Ping-Pong Handover']]

# === Data Exploration
LTE_DATA1
LTE_DATA1.columns
LTE_DATA1.head()
LTE_DATA1.dtypes
LTE_DATA1.shape
# === Convert 'Begin Time' to datetime ===
LTE_DATA1.loc[:, 'Begin Time'] = pd.to_datetime(LTE_DATA1['Begin Time'])
#or LTE_DATA1['Begin Time'] = pd.to_datetime(LTE_DATA1['Begin Time'])

# === Explorting LTE_DATA1
LTE_DATA1.head()
LTE_DATA1.dtypes
LTE_DATA1[LTE_DATA1['Begin Time'].between('2024-12-24', '2024-12-25')] # Coversion to date is successful

# === Writting LTE data 1 to local disk
LTE_DATA1.to_csv('exports/LTE DATA 1.csv')

# === Set Begin Time as Index (for time series modeling) ===
LTE_DATA2 = LTE_DATA1.copy()
LTE_DATA2 = LTE_DATA2.set_index('Begin Time')
# === Explorting LTE_DATA2
LTE_DATA2
LTE_DATA2.shape
# == Writing Data to local Disk
LTE_DATA2.to_csv('exports/LTE DATA2.csv')
