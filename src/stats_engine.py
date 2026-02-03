import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime

def calculate_basic_stats(hourly_df):
    """
    Tính toán các chỉ số thống kê đặc trưng cho từng nhà máy.
    """
    stats_list = []
    
    # Chia nhóm theo từng nhà máy để phân tích riêng biệt
    for factory, group in hourly_df.groupby('factory_id'):
        counts = group['order_count']
        
        mean_val = counts.mean()      # Kỳ vọng E[N(t)]
        var_val = counts.var()        # Phương sai Var[N(t)]
        std_val = counts.std()        # Độ lệch chuẩn
        
        # Chỉ số phân tán (Index of Dispersion) - Nếu ~ 1 thì là Poisson chuẩn
        iod = var_val / mean_val if mean_val != 0 else 0
        
        stats_list.append({
            'factory_id': factory,
            'lambda_est': round(mean_val, 3),
            'variance': round(var_val, 3),
            'dispersion_index': round(iod, 3),
            'max_orders_hr': counts.max(),
            'total_sample_hours': len(counts)
        })
    
    return pd.DataFrame(stats_list)

def poisson_goodness_of_fit(group_data):
    """
    Kiểm định xem dữ liệu có thực sự tuân theo phân phối Poisson không.
    Sử dụng kiểm định Chi-square.
    """
    obs_counts = group_data.value_counts().sort_index()
    mu = group_data.mean()
    
    # Tính tần suất kỳ vọng dựa trên công thức Poisson
    expected_probs = [stats.poisson.pmf(i, mu) for i in obs_counts.index]
    expected_counts = np.array(expected_probs) * len(group_data)
    
    # Chạy kiểm định Chi-square
    chi2, p_val = stats.chisquare(f_obs=obs_counts, f_exp=expected_counts)
    
    return p_val

def export_report(summary_df, file_name='data/processed/final_report.md'):
    """Tạo báo cáo dưới dạng file Markdown để lưu trữ"""
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write("# BÁO CÁO PHÂN TÍCH QUÁ TRÌNH NGẪU NHIÊN (SOFA)\n\n")
        f.write(f"Ngày lập báo cáo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## 1. Bảng tóm tắt chỉ số các nhà máy\n")
        f.write(summary_df.to_markdown(index=False))
        f.write("\n\n## 2. Nhận xét thống kê\n")
        
        for _, row in summary_df.iterrows():
            f.write(f"### Nhà máy: {row['factory_id']}\n")
            f.write(f"- Tốc độ đơn hàng trung bình (lambda): {row['lambda_est']} đơn/giờ.\n")
            if 0.9 <= row['dispersion_index'] <= 1.1:
                f.write("- Trạng thái: Hoạt động chuẩn theo phân phối Poisson.\n")
            else:
                f.write("- Trạng thái: Có dấu hiệu biến động bất thường (Overdispersion).\n")
    print(f"--- Đã xuất báo cáo chuyên sâu tại {file_name} ---")