
# Statistical Order Flow Analytics (SOFA)

## 1. Tổng quan dự án

**Mục tiêu:** sử dụng các phương pháp thống kê để mô tả và phân tích dữ liệu dòng đơn hàng theo **Poisson process** (quá trình ngẫu nhiên), từ đó trực quan hóa sự khác biệt về số đơn theo thời gian và giữa các nhà máy.

**Bối cảnh:** hệ thống gồm **n nhà máy** (mặc định `n = 3`). Số lượng và tham số sinh dữ liệu có thể tinh chỉnh tại `data_gen.py`. Mục tiêu là mô hình hóa việc xuất hiện ngẫu nhiên của đơn hàng theo **đơn/giờ**, sau đó so sánh sự khác biệt giữa các nhà máy với số  **đơn/giờ** khác nhau dựa trên thống kê của chuỗi thời gian.


---

## 2. Các thành phần trọng tâm

### A. Data Modeling (Thiết kế dữ liệu)

Thay vì sử dụng các dữ liệu mẫu có sẵn, dự án xây dựng `data_gen.py` để tự động tạo dữ liệu cho các nhà máy nhằm tối ưu hiệu suất và tăng tính linh động khi người dùng muốn kiểm tra sự khác nhau giữa các bộ dữ liệu tương đồng nhưng có số lượng/đặc tính khác nhau.


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


### C. Vận hành & Kỹ thuật

* **Tech Stack:**
  - **Python**: điều phối pipeline chạy toàn bộ quá trình tạo dữ liệu → nạp dữ liệu → thống kê → trực quan hóa.
  - **pandas**: đọc/ghép CSV, xử lý `timestamp`, group theo thời gian (hourly aggregation).
  - **numpy**: sinh dữ liệu giả lập theo phân phối **Poisson** trong `data_gen.py` và hỗ trợ tính toán.
  - **scipy**: thực hiện kiểm định thống kê (Poisson goodness-of-fit bằng **Chi-square**).
  - **matplotlib** + **seaborn**: vẽ biểu đồ xu hướng và histogram so sánh phân phối trong `src/visualizer.py`.

* **Cấu trúc module:** Phân tách mã nguồn thành các file/chức năng riêng biệt:
  - `data_gen.py`: tạo dữ liệu giả lập (Poisson events) và ghi ra `data/raw/*.csv`.
  - `src/data_loader.py`: tải CSV, lọc theo khoảng năm, sau đó chuyển sang dạng theo giờ (`order_count`).
  - `src/stats_engine.py`: tính thống kê (mean/variance/std, dispersion index) và xuất báo cáo Markdown.
  - `src/visualizer.py`: vẽ rolling mean và histogram phân phối.

* **Tính linh hoạt:** Hệ thống cho phép tùy chọn khoảng thời gian phân tích (ví dụ: 2016-2018), tinh chỉnh tham số `lam` (thay đổi tốc độ đơn/giờ) và so sánh nhiều nhà máy thông qua cấu hình chạy ở `main.py`.


Code ví dụ:

```python
generate_factory_data(factory_name="name", lam=x)
```

Trong đó:
- `factory_name` (str): tên nhà máy.
- `x` / `lam` (float): **tốc độ trung bình** λ = số đơn hàng kỳ vọng **trong 1 giờ**.

Ghi chú:
- `lam` là tham số điều khiển cường độ của quá trình Poisson (tạo số đơn/giờ từ phân phối Poisson).
- Dữ liệu sinh ra là các **sự kiện rời rạc theo thời gian** (`timestamp`) và sau đó được **gom theo giờ** để phân tích chuỗi `order_count`.

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

## 4. hướng dẫn triển khai (Step-by-Step)

1. **Bước 1:** Kích hoạt môi trường ảo tại terminal `.venv\Scripts\Activate.ps1`
2. **Bước 2:** Chạy `data_gen.py` để tạo dữ liệu giả lập Poisson cho giai đoạn 2016 - 2018.
3. **Bước 3:** chạy `main.py` để chạy toàn bộ dự án hoặc tinh chỉnh các thông số tại dự án
4. **Bước 4:** Xem kết quả đã được trực quan hóa và các kiểm định thống kê để so sánh hiệu suất nhà máy tại `final_report.md`.

---
