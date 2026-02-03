import pandas as pd
import glob
import os

def factory_data_loader(data_path='data/raw/*.csv', start_year = None, end_year = None):
    
    all_files = glob.glob(data_path)

    if not all_files:
        raise FileNotFoundError(f"Không tìm thấy tệp nào trong đường dẫn đã chỉ định.: {data_path}")
    

    li = []        

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    master_df = pd.concat(li, axis = 0, ignore_index=True)

    master_df['timestamp'] = pd.to_datetime(master_df['timestamp'])

    if start_year and end_year:
        master_df = master_df[
            (master_df['timestamp'].dt.year >= start_year) & 
            (master_df['timestamp'].dt.year <= end_year)
            ]
        
    master_df = master_df.sort_values(by='timestamp').reset_index(drop=True)
    
    print(f"--- Đã tải và gộp {len(master_df)} đơn hàng từ {len(all_files)} file ---")
    return master_df

def get_hourly_counts(df):
    hourly_df = df.groupby(['factory_id', pd.Grouper(key='timestamp', freq='h')]).size().reset_index(name='order_count')
    return hourly_df