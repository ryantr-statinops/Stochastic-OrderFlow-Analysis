
# Statistical Time Series Analytics (SOFA)

## 1. Tổng quan dự án

**Mục tiêu:** sử dụng các phương pháp thông kê cho các loại dữ liệu tuân theo quy luật phân phối Possion, nhằm đơn giản và trực quan hóa được sự khác biệt của số lượng dữ liệu trong mô hình chuỗi Poisson 
**Quá trình ngẫu nhiên (Stochastic Process)** 

**Bối cảnh** Cho mạng lưới gồm 3 nhà máy. Hệ thống tập trung vào việc mô hình hóa sự xuất hiện của đơn hàng để tối ưu hóa năng lực vận hành.

---

## 2. Các thành phần trọng tâm

### A. Data Modeling (Thiết kế dữ liệu)

Thay vì các file Excel rời rạc, dự án xây dựng cấu trúc dữ liệu theo hướng chuỗi thời gian (**Time-series**):

* **Dữ liệu nguồn:** 3 file CSV riêng biệt cho 3 nhà máy (Factory A, B, C).
* **Biến số chính:** `timestamp` (thời điểm đơn hàng đến), `order_id`, và `factory_id`.
* **Logic:** Chuyển đổi dữ liệu từ dạng "Sự kiện rời rạc" (Discrete Events) sang dạng "Tần suất theo khung giờ" (Hourly Aggregation) để phục vụ mô hình hóa.

### B. Statistics (Thống kê chuyên sâu)

Các phương pháp phân tích trong dự án sử dụng gồm:

* **Aggregation theo giờ (hourly aggregation):** Gom dữ liệu sự kiện rời rạc theo từng khung giờ để thu được chuỗi thời gian `order_count` cho mỗi `factory_id`.
* **Tính toán các chỉ số thống kê cơ bản theo factory:** Tính **mean (ước lượng λ)**, **variance**, **std** của số đơn/giờ.
* **Chỉ số phân tán (dispersion index):**
  - `dispersion_index = variance / mean`
  - Nếu gần **1** ⇒ phù hợp với giả định **Poisson**; nếu khác nhiều ⇒ có thể **overdispersion**.
* **Kiểm định phù hợp phân phối Poisson (Poisson goodness-of-fit):**
  - Dùng **Chi-square** để so sánh tần suất quan sát với tần suất kỳ vọng theo **Poisson**.
* **Trực quan hóa:**
  - **Rolling mean (trung bình trượt 24h)** để quan sát xu hướng.
  - **Histogram so sánh phân phối** cho từng nhà máy.


### C. DA-Ops (Vận hành & Kỹ thuật)
* **Tổng quan phương pháp triển khai:** Sử dụng Python làm môi trường giao tiếp chính cùng các thư viện chuyên môn để tối ưu hệ sinh thái của Python trong phân tích dữ liệu

* **Cấu trúc Module:** Phân tách mã nguồn thành các folder/file chức năng riêng biệt: `data_gen.py`, `data_loader.py`, `stats_engine.py`.
* **Tính linh hoạt:** Hệ thống cho phép tùy chọn khoảng thời gian phân tích (ví dụ: 2016-2018), tinh chỉnh dữ liệu(thay đổi giá trị lamda) và lựa chọn số lượng nhà máy thông qua cấu hình tập trung tại `main`.

Code ví dụ:
```
generate_factory_data("name", lam=x) 
```
Trong đó:
"name"(string): là tên nhà máy
x = $lamda (số đơn hàng trung bình trong 1 giờ )
lưu ý: Giá trị $lamda tuân theo quy luật phân phối chuẩn với giá trị x là số lượng đơn hàng trung bình trong 1 giờ khác với quy luật phân phối Poisson là chuỗi các sự kiện xảy ra liên tục theo thời gian
---

## 3. Cấu trúc thư mục dự án

Dự án chia cấu trúc thư mục phân biệt theo từng chức năng để dễ dàng mở rộng và tái sử dụng cho trường hợp khác:

```plaintext
project_stochastic/
|
├── data/              #chứa dữ liệu thô và dữ liệu sau tính toán
|   |
│   ├── raw/           # Chứa 3 file CSV dữ liệu gốc của các nhà máy
│   └── processed/     # Chứa file Master sau khi tính toán và tổng hợp
|   
├── src/               # Chứa và phân loại các Module tính toán khác nhau
|   |
│   ├── data_loader.py # Module quét và đọc file tự động
│   ├── stats_engine.py# Module tính toán các chỉ số thống kê (Poisson, Mean, Std)
│   └── visualizer.py  # Module vẽ biểu đồ phân tích
|
├── main.py            # Script thực thi chính (điều chỉnh tham số của kết quả tại đây)
|
├── data_gen.py        # Script khởi tạo dữ liệu giả lập ban đầu(điều chỉnh tham số của dữ liệu tại đây)
|
└── requirements.txt   # Danh sách thư viện (pandas, numpy, matplotlib, scipy)

```

---

## 4. Kế hoạch hành động (Step-by-Step)

1. **Bước 1:** Chạy `data_gen.py` để tạo dữ liệu giả lập Poisson cho giai đoạn 2016 - 2018.
2. **Bước 2:** Xây dựng `data_loader.py` để hợp nhất dữ liệu từ các nhà máy và lọc theo thời gian yêu cầu.
3. **Bước 3:** Thực hiện **Gom nhóm (Aggregation)** theo giờ để xác định biến ngẫu nhiên .
4. **Bước 4:** Trực quan hóa và thực hiện các kiểm định thống kê để so sánh hiệu suất nhà máy.

---
