""" Run associator 
    picks --> events
"""
import os, glob
import argparse
import numpy as np
from obspy import UTCDateTime
import associators
import config
import warnings
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ppk_dir', type=str,
                        default='output/picks')
    parser.add_argument('--time_range', type=str,
                        default='20171003-20171004')
    parser.add_argument('--sta_file', type=str,
                        default='input/station.dat')
    parser.add_argument('--out_ctlg', type=str,
                        default='output/catalog.tmp')
    parser.add_argument('--out_pha', type=str,
                        default='output/phase.tmp')
    args = parser.parse_args()


# define func
cfg = config.Config()
get_picks = cfg.get_picks
sta_dict = cfg.get_sta_dict(args.sta_file)
associator = associators.TS_Assoc(\
    sta_dict,
    assoc_num = cfg.assoc_num,
    ot_dev = cfg.ot_dev,
    max_res = cfg.max_res)
# i/o paths
out_root = os.path.split(args.out_ctlg)[0]
if not os.path.exists(out_root): os.makedirs(out_root)
out_ctlg = open(args.out_ctlg,'w')
out_pha = open(args.out_pha,'w')

# get date range
start_date, end_date = [UTCDateTime(date) for date in args.time_range.split('-')]
print('run assoc: picks --> events')
print('time range: {} to {}'.format(start_date.date, end_date.date))

# for all days
num_day = (end_date.date - start_date.date).days
for day_idx in range(num_day):
    # 1. get picks
    date = start_date + day_idx*86400
    picks = get_picks(date, args.ppk_dir)
    # 2. associate picks: picks --> event_picks & event_loc
    associator.associate(picks, out_ctlg, out_pha)
out_pha.close()
out_ctlg.close()
