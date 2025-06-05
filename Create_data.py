# Create_data.py - Tạo dữ liệu lương tổng hợp nhân tạo với các yếu tố mở rộng

# Tái nhập các thư viện cần thiết để đảm bảo môi trường chạy lại sạch
import pandas as pd # Thư viện mạnh mẽ để xử lý và phân tích dữ liệu dạng bảng (DataFrame)
import numpy as np  # Thư viện cơ bản cho các phép toán số học trên mảng và ma trận, cũng như tạo số ngẫu nhiên

# Thiết lập seed cho trình tạo số ngẫu nhiên để đảm bảo rằng kết quả có thể lặp lại
# Khi sử dụng cùng một seed, mỗi lần chạy script sẽ tạo ra cùng một bộ dữ liệu ngẫu nhiên
np.random.seed(42)

# Định nghĩa hàm để tạo một mẫu dữ liệu lương ngẫu nhiên cho một cá nhân
def generate_sample():
    # Các yếu tố đã có từ trước (Đặc trưng cơ bản của nhân viên)
    exp = np.random.randint(0, 11)  # 'Kinh nghiệm': số năm kinh nghiệm (0-10)
    edu = np.random.choice(['THCS', 'THPT', 'CĐ', 'ĐH']) # 'Trình độ': THCS, THPT, CĐ (Cao đẳng), ĐH (Đại học)
    cert = np.random.choice([0, 1])  # 'Chứng chỉ': 0 (không có), 1 (có)
    night = np.random.choice([0, 1])  # 'Ca đêm': 0 (không), 1 (có)
    overtime = np.random.choice([0, 1])  # 'Làm thêm': 0 (không có), 1 (có)

    # --- Bổ sung các yếu tố mới dựa trên phân tích hình ảnh (Đặc trưng bổ sung) ---
    # 6. Chức vụ: 'Nhân viên', 'Tổ trưởng', 'Đội trưởng' với xác suất tương ứng để tạo phân phối thực tế hơn
    position = np.random.choice(['Nhân viên', 'Tổ trưởng', 'Đội trưởng'], p=[0.7, 0.2, 0.1])
    # 7. Loại hợp đồng: 'Thời vụ', 'Chính thức'
    contract_type = np.random.choice(['Thời vụ', 'Chính thức'])
    # 8. Kỹ năng đặc thù (0: Không, 1: Có) - Ví dụ: Kỹ năng võ thuật, PCCC, sơ cứu...
    special_skills = np.random.choice([0, 1])
    # 9. Khu vực làm việc (dựa trên vùng lương tối thiểu ở Việt Nam để tạo sự đa dạng)
    work_area = np.random.choice(['Vùng I (TP.HCM, Hà Nội)', 'Vùng II (TP. Đà Nẵng, Hải Phòng)', 'Vùng III (TP. Buôn Ma Thuột, Huế)', 'Vùng IV (Nông thôn)'])
    # 10. Loại hình mục tiêu (khách hàng/địa điểm làm việc) - Ảnh hưởng đến tính chất công việc và mức lương
    client_type = np.random.choice(['Ngân hàng', 'Khách sạn 5 sao', 'Trường học', 'Nhà máy', 'VIP'])
    # 11. Phụ cấp, phúc lợi công ty (tỷ lệ phần trăm trên lương cơ bản) - Mô phỏng các khoản phúc lợi khác
    allowances_percentage = np.random.uniform(0.0, 0.30) # Từ 0% đến 30%

    # --- Tính toán lương cơ bản ban đầu dựa trên Khu vực làm việc (tương ứng lương tối thiểu vùng) ---
    # Đây là điểm khởi đầu cho việc tính toán lương, phản ánh chi phí sinh hoạt và quy định vùng
    base_salary_regional = 0
    if work_area == 'Vùng I (TP.HCM, Hà Nội)':
        base_salary_regional = 5_000_000  # Gần với lương tối thiểu vùng I (khoảng 4.68 triệu VND)
    elif work_area == 'Vùng II (TP. Đà Nẵng, Hải Phòng)':
        base_salary_regional = 4_500_000  # Gần với lương tối thiểu vùng II (khoảng 4.16 triệu VND)
    elif work_area == 'Vùng III (TP. Buôn Ma Thuột, Huế)':
        base_salary_regional = 4_000_000  # Gần với lương tối thiểu vùng III (khoảng 3.64 triệu VND)
    elif work_area == 'Vùng IV (Nông thôn)':
        base_salary_regional = 3_500_000  # Gần với lương tối thiểu vùng IV (khoảng 3.25 triệu VND)

    # Lương khởi điểm chính thức sẽ được điều chỉnh từ base_salary_regional
    current_salary = float(base_salary_regional) # Đảm bảo là float để tính toán chính xác

    # --- Áp dụng các yếu tố ảnh hưởng lên mức lương hiện tại ---

    # 1. Kinh nghiệm làm việc: Cứ mỗi 3 năm kinh nghiệm, lương tăng thêm 1 triệu VND
    current_salary += (exp // 3) * 1_000_000

    # 2. Trình độ học vấn: Áp dụng tỷ lệ tăng lương dựa trên trình độ
    if edu == 'CĐ':
        current_salary *= 1.10  # Cao đẳng: tăng 10% lương
    elif edu == 'ĐH':
        current_salary *= 1.15  # Đại học: tăng 15% lương
    # THCS và THPT không có thay đổi tỷ lệ

    # 3. Chứng chỉ nghiệp vụ: Tăng lương nếu có chứng chỉ
    if cert:
        current_salary *= 1.07  # Có chứng chỉ: tăng 7%

    # 6. Chức vụ: Áp dụng tỷ lệ tăng lương dựa trên chức vụ (có một khoảng ngẫu nhiên để tăng tính đa dạng)
    if position == 'Tổ trưởng':
        current_salary *= np.random.uniform(1.10, 1.15) # Tổ trưởng: tăng từ 10-15%
    elif position == 'Đội trưởng':
        current_salary *= np.random.uniform(1.20, 1.30) # Đội trưởng: tăng từ 20-30%

    # 7. Loại hợp đồng: Hợp đồng thời vụ có thể có lương thấp hơn hợp đồng chính thức
    if contract_type == 'Thời vụ':
        current_salary *= 0.80 # Thời vụ: giảm 20% lương (giả định đơn giản)

    # 8. Kỹ năng đặc thù: Cộng thêm một khoản tiền cố định nếu có kỹ năng đặc biệt
    if special_skills:
        current_salary += np.random.uniform(2_000_000, 5_000_000) # Thêm 2-5 triệu VND

    # 10. Loại hình mục tiêu (khách hàng/địa điểm làm việc): Lương có thể cao hơn tùy loại mục tiêu
    if client_type == 'Ngân hàng':
        current_salary *= 1.08 # Ngân hàng: tăng 8%
    elif client_type == 'Khách sạn 5 sao':
        current_salary *= 1.05 # Khách sạn 5 sao: tăng 5%
    elif client_type == 'VIP':
        current_salary *= 1.15 # Khách hàng VIP: tăng 15%

    # 4. Ca làm việc (ca đêm): Áp dụng phụ cấp làm ca đêm
    if night:
        current_salary *= 1.30 # Làm ca đêm: tăng 30%

    # 5. Làm thêm giờ: Áp dụng phụ cấp làm thêm giờ
    if overtime:
        current_salary *= 1.50 # Làm thêm giờ: tăng 50%

    # 11. Phụ cấp, phúc lợi công ty: Áp dụng tỷ lệ phần trăm cuối cùng sau tất cả các điều chỉnh khác
    current_salary *= (1 + allowances_percentage)

    # Trả về một danh sách chứa tất cả các đặc trưng và mức lương đã tính toán
    return [exp, edu, cert, night, overtime, position, contract_type,
            special_skills, work_area, client_type, allowances_percentage, current_salary]

# Tạo một danh sách gồm 300 mẫu dữ liệu (có thể tăng lên để có nhiều dữ liệu hơn cho mô hình học)
data = [generate_sample() for _ in range(300)]
# Chuyển đổi danh sách dữ liệu này thành một DataFrame của pandas với các tên cột rõ ràng
df_data = pd.DataFrame(data, columns=[
    "Kinh nghiệm", "Trình độ", "Chứng chỉ", "Ca đêm", "Làm thêm",
    "Chức vụ", "Loại hợp đồng", "Kỹ năng đặc thù", "Khu vực làm việc",
    "Loại hình mục tiêu", "Tỷ lệ phụ cấp", "Lương"
])

# In ra 5 dòng đầu tiên của DataFrame để kiểm tra nhanh cấu trúc và nội dung dữ liệu
print("5 dòng đầu tiên của dữ liệu lương:")
print(df_data.head())
print("\nThông tin tóm tắt về dữ liệu (số lượng bản ghi, kiểu dữ liệu, non-null counts):")
print(df_data.info())
print("\nThống kê mô tả dữ liệu (mean, std, min, max, quartiles):")
print(df_data.describe(include='all')) # include='all' để hiển thị cả thống kê cho cột object (phân loại)
