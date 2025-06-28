#importing essential Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Setting the pd configuration
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 100)
#importing Libyana LTE KPI Data
LTEKPIS_raw = pd.read_excel('Datasets/Libyana Dataset JUN25/History Query-LTE KPI one year daily.xlsx',
                        sheet_name='Sheet0')
#Exploratory DATA Analysis
LTEKPIS_raw.head(10)
LTEKPIS_raw.shape #(61647 x 95)
LTEKPIS_raw.columns # some columns require to be renamed for clarity

##### == Select KEY Radio Features required for forecasting (technical discussion as to why will be convered)
LTEKPIS_clean = LTEKPIS_raw[[
    #Time Stamp
    'Begin Time',
    'Granularity',
    #BTS and Cells identifiers
    'eNodeB ID',
    'eNodeB Name',
    'E-UTRAN FDD Cell ID',
    'E-UTRAN FDD Cell Name',
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
    'Number of Ping-Pong Handover']].rename(columns={
    # Time Stamp
    'Begin Time': 'timestamp',
    'Granularity': 'granularity',
    # BTS and Cell Identifiers
    'eNodeB ID': 'enodeb_id',
    'eNodeB Name': 'enodeb_name',
    'E-UTRAN FDD Cell ID': 'cell_id',
    'E-UTRAN FDD Cell Name': 'cell_name',
    # Target Variables
    'PS Traffic Volume(GB)_ITBBU&SDR': 'ps_traffic_volume_gb',
    'DL E-UTRAN IP Throughput(Mbps)_ITBBU&SDR': 'dl_throughput_mbps',
    'Cell DL Average Aggregated Throughput(Mbps)': 'cell_dl_avg_agg_throughput',
    'DL PRB Utilization Rate(%)': 'dl_prb_util_%',
    # Load & Resource KPIs
    'UL PRB Utilization Rate(%)': 'ul_prb_util_%',
    'DL PRB Available (Bandwidth)': 'dl_prb_available_bandwidth',
    'Mean Number of RRC Connection User': 'mean_no_rrc_users',
    'Maximum Active User Number on User Plane': 'max_active_no_users_uplane',
    'Maximum Number of RRC Connection User': 'max_no_rrc_users',
    # Quality KPIs
    'RRC Establishment Success Rate(%)': 'rrc_success_rate_%',
    'E-RAB Setup Success Rate(%)': 'erab_setup_success_rate_%',
    'E-RAB Drop Rate(%)': 'erab_drop_rate_%',
    'RRC Drop Rate(%)': 'rrc_drop_rate_%',
    'Cell Uplink BLER(%)': 'cell_ul_bler_rate_%',
    'Cell Downlink BLER(%)': 'cell_dl_bler_rate_%',
    # RF/PHY Layer
    'DL Average MCS': 'dl_avg_mcs',
    'UL Average MCS': 'ul_avg_mcs',
    'Average CQI(N/A)': 'avg_cqi',
    'Ratio of CQI>7 Percentage': 'ratio_cqi_gt7',
    'Ratio of CQI >= 10 (64QAM)': 'ratio_cqi_gte10',
    # Coverage and Interference
    'LTE Average TA(km)': 'avg_ta_km',
    'Average Cell RSSI(dBm)': 'avg_rssi_dbm',
    'Ratio of SINR<-3dB': 'ratio_sinr_lt_neg3',
    'Ratio of RSRP in Range of  [-110,-106]dBm': 'rsrp_range_110_106_Ratio_%',
    'Ratio of RSRP in Range of  [-115,-111]dBm': 'rsrp_range_115_111_Ratio_%',
    'Ratio of RSRP in Range of  [-120,-116]dBm': 'rsrp_range_120_116_Ratio_%',
    'Ratio of RSRP in Range of  [-140,-121]dBm': 'rsrp_range_140_121_Ratio_%',
    # Mobility
    'Success Rate of Outgoing Handover(Cell)(%)': 'outgoing_ho_success_rate_%',
    'Success Rate of Intra-RAT Inter-frequency Cell Outgoing Handover(%)': 'intra_rat_ho_success_rate_%',
    'Number of Ping-Pong Handover': 'no_ping_pong_ho_count'
})
## = Exporting Data to local disk
LTEKPIS_clean.to_csv('exports/Libyana LTE KPIs/LTEKPIS_clean.csv')
## == Exploratory Data analysis of the cleaned data
LTEKPIS_clean.columns
LTEKPIS_clean['enodeb_name'].nunique() # A total of 16 eNodeBs are in the dataset
LTEKPIS_clean['cell_name'].nunique()   # A total of 168 cells are in the dataset
LTEKPIS_clean.shape #Data contains (61647 x 36)

