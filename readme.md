
# Statistical Order Flow Analytics (SOFA)

## 1. Tổng quan dự án

**Mục tiêu:** Xây dựng hệ thống quản lý và phân tích dòng chảy đơn hàng dưới dạng **Quá trình ngẫu nhiên (Stochastic Process)** cho mạng lưới gồm 3 nhà máy. Hệ thống tập trung vào việc mô hình hóa sự xuất hiện của đơn hàng để tối ưu hóa năng lực vận hành.

---

## 2. Các thành phần trọng tâm

### A. Data Modeling (Thiết kế dữ liệu)

Thay vì các file Excel rời rạc, dự án xây dựng cấu trúc dữ liệu theo hướng chuỗi thời gian (**Time-series**):

* **Dữ liệu nguồn:** 3 file CSV riêng biệt cho 3 nhà máy (Factory A, B, C).
* **Biến số chính:** `timestamp` (thời điểm đơn hàng đến), `order_id`, và `factory_id`.
* **Logic:** Chuyển đổi dữ liệu từ dạng "Sự kiện rời rạc" (Discrete Events) sang dạng "Tần suất theo khung giờ" (Hourly Aggregation) để phục vụ mô hình hóa.

### B. Statistics (Thống kê chuyên sâu)

Nghiên cứu đơn hàng như một **Biến ngẫu nhiên (Random Variable)**:

* **Phân phối Poisson:** Kiểm định số lượng đơn hàng mỗi giờ .
* **Kiểm tra tính dừng (Stationarity):** So sánh đặc tính dòng chảy đơn hàng giữa các năm (2016 - 2018) để xác định sự thay đổi trong quy luật vận hành.
* **Trực quan hóa:** Sử dụng **Heatmap** (giờ/thứ) và biểu đồ đường để theo dõi sự biến động của tham số  (tốc độ đơn hàng trung bình).

### C. DA-Ops (Vận hành & Kỹ thuật)

* **Cấu trúc Module:** Phân tách mã nguồn thành các file chức năng riêng biệt: `data_gen.py`, `data_loader.py`, `stats_engine.py`.
* **Tính linh hoạt:** Hệ thống cho phép tùy chọn khoảng thời gian phân tích (ví dụ: 2016-2018) và lựa chọn nhà máy thông qua cấu hình tập trung.

---

## 3. Cấu trúc thư mục dự án

Dự án tuân thủ cấu trúc thư mục chuyên nghiệp để dễ dàng mở rộng:

```plaintext
project_stochastic/
├── data/
│   ├── raw/           # Chứa 3 file CSV dữ liệu gốc của các nhà máy
│   └── processed/     # Chứa file Master sau khi gộp và chuẩn hóa
├── src/
│   ├── data_loader.py # Module quét và đọc file tự động
│   ├── stats_engine.py# Module tính toán các chỉ số thống kê (Poisson, Mean, Std)
│   └── visualizer.py  # Module vẽ biểu đồ phân tích
├── main.py            # Script thực thi chính (điều chỉnh tham số năm tại đây)
├── data_gen.py        # Script khởi tạo dữ liệu giả lập ban đầu
└── requirements.txt   # Danh sách thư viện (pandas, numpy, matplotlib, scipy)

```

---

## 4. Kế hoạch hành động (Step-by-Step)

1. **Bước 1:** Chạy `data_gen.py` để tạo dữ liệu giả lập Poisson cho giai đoạn 2016 - 2018.
2. **Bước 2:** Xây dựng `data_loader.py` để hợp nhất dữ liệu từ các nhà máy và lọc theo thời gian yêu cầu.
3. **Bước 3:** Thực hiện **Gom nhóm (Aggregation)** theo giờ để xác định biến ngẫu nhiên .
4. **Bước 4:** Trực quan hóa và thực hiện các kiểm định thống kê để so sánh hiệu suất nhà máy.

---

**Gợi ý tiếp theo:**
Bạn hãy lưu nội dung trên vào file `README.md`. Sau đó, chúng ta sẽ bắt tay vào **Bước 2**: Viết module `src/data_loader.py` để "triệu hồi" dữ liệu từ các file CSV mà bạn vừa tạo ở bước trước nhé. Bạn đã sẵn sàng chưa?