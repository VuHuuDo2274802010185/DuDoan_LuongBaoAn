# Predict_engine.py - Engine dự đoán lương nhân viên (chỉ xử lý logic ML, không gọi AI trực tiếp)

# Import các thư viện cần thiết cho việc xử lý dữ liệu và huấn luyện mô hình
import pandas as pd # Thư viện để làm việc với cấu trúc dữ liệu DataFrame
from sklearn.model_selection import train_test_split # Hàm để chia tập dữ liệu thành tập huấn luyện và tập kiểm tra
from sklearn.ensemble import RandomForestRegressor # Mô hình học máy Random Forest Regression
from sklearn.preprocessing import LabelEncoder # Đối tượng để mã hóa các biến phân loại (như trình độ học vấn, chức vụ,...) thành dạng số
from sklearn.metrics import mean_absolute_error, r2_score # Các độ đo để đánh giá hiệu suất của mô hình hồi quy

class SalaryPredictionEngine:
    def __init__(self):
        # Khởi tạo các thuộc tính của lớp
        self.model = None          # Đối tượng mô hình học máy (ban đầu là None)
        self.encoders = {}         # Dictionary để lưu trữ các LabelEncoder cho từng biến phân loại
                                   # Mỗi biến phân loại (Trình độ, Chức vụ,...) sẽ có một encoder riêng
        self.mae = None            # Sai số tuyệt đối trung bình của mô hình (ban đầu là None)
        self.r2 = None             # Hệ số xác định R-squared của mô hình (ban đầu là None)
        self.is_trained = False    # Cờ trạng thái cho biết mô hình đã được huấn luyện hay chưa

    def load_and_prepare_data(self):
        """
        Tải và chuẩn bị dữ liệu từ Create_data.py để huấn luyện mô hình.
        Phương thức này sẽ mã hóa các biến phân loại và chia thành X (đặc trưng) và y (mục tiêu).
        """
        try:
            # Import DataFrame df_data từ file Create_data.py
            # Lưu ý: Điều này giả định Create_data.py đã chạy và tạo ra df_data global
            from Create_data import df_data

            # Định nghĩa các cột phân loại (kiểu object/string) cần mã hóa thành dạng số
            categorical_cols = ["Trình độ", "Chức vụ", "Loại hợp đồng", "Khu vực làm việc", "Loại hình mục tiêu"]

            # Vòng lặp qua từng cột phân loại để khởi tạo và áp dụng LabelEncoder
            for col in categorical_cols:
                if col not in self.encoders: # Nếu encoder cho cột này chưa được tạo, hãy tạo mới
                    self.encoders[col] = LabelEncoder()
                # Áp dụng LabelEncoder: fit (học các nhãn duy nhất) và transform (chuyển đổi sang số)
                df_data[f"{col}_encoded"] = self.encoders[col].fit_transform(df_data[col])

            # Chuẩn bị các đặc trưng (features - X) và biến mục tiêu (target - y) cho mô hình
            # X bao gồm tất cả các cột đặc trưng (đã mã hóa nếu là phân loại) sẽ được dùng để dự đoán
            X = df_data[[
                "Kinh nghiệm", "Trình độ_encoded", "Chứng chỉ", "Ca đêm", "Làm thêm",
                "Chức vụ_encoded", "Loại hợp đồng_encoded", "Kỹ năng đặc thù",
                "Khu vực làm việc_encoded", "Loại hình mục tiêu_encoded", "Tỷ lệ phụ cấp"
            ]]
            # y là cột mà mô hình sẽ cố gắng dự đoán (mức lương)
            y = df_data["Lương"]

            return X, y
        except Exception as e:
            # Xử lý nếu có lỗi trong quá trình tải hoặc chuẩn bị dữ liệu
            raise Exception(f"Lỗi khi load hoặc chuẩn bị dữ liệu: {e}")

    def train_model(self):
        """
        Huấn luyện mô hình dự đoán lương.
        Phương thức này sẽ tải dữ liệu, chia thành tập huấn luyện/kiểm tra,
        huấn luyện mô hình Random Forest, và đánh giá hiệu suất.
        """
        # Kiểm tra nếu mô hình đã được huấn luyện rồi thì không huấn luyện lại
        # Điều này giúp tránh lãng phí tài nguyên khi ứng dụng khởi động lại hoặc khi route được gọi nhiều lần
        if self.is_trained:
            print("Mô hình đã được huấn luyện. Bỏ qua huấn luyện lại.")
            return True

        try:
            # Tải và chuẩn bị dữ liệu bằng cách gọi phương thức nội bộ load_and_prepare_data
            X, y = self.load_and_prepare_data()

            # Tách dữ liệu thành tập huấn luyện (80%) và tập kiểm tra (20%)
            # X_train, y_train: dữ liệu dùng để huấn luyện mô hình
            # X_test, y_test: dữ liệu dùng để đánh giá hiệu suất mô hình sau khi huấn luyện
            # test_size=0.2: 20% dữ liệu sẽ được dùng để kiểm tra
            # random_state=42: đảm bảo việc tách dữ liệu là cố định và có thể lặp lại (quan trọng cho tính nhất quán)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Khởi tạo mô hình Random Forest Regressor
            # n_estimators=100: số lượng cây quyết định trong "rừng" (số cây càng nhiều thường càng chính xác, nhưng tốn thời gian hơn)
            # random_state=42: đảm bảo quá trình huấn luyện mô hình có thể lặp lại
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            # Huấn luyện mô hình sử dụng dữ liệu huấn luyện
            self.model.fit(X_train, y_train)

            # Đánh giá hiệu suất của mô hình trên tập kiểm tra
            y_pred = self.model.predict(X_test)
            # Tính Sai số tuyệt đối trung bình (Mean Absolute Error - MAE)
            # MAE đo lường độ lớn trung bình của sai số giữa giá trị dự đoán và giá trị thực tế
            self.mae = mean_absolute_error(y_test, y_pred)
            # Tính Hệ số xác định R-squared (R2 Score)
            # R2 cho biết mức độ phù hợp của mô hình với dữ liệu, giá trị càng gần 1 càng tốt
            self.r2 = r2_score(y_test, y_pred)

            self.is_trained = True # Đặt cờ trạng thái là True sau khi huấn luyện thành công
            return True
        except Exception as e:
            # In ra thông báo lỗi nếu có vấn đề trong quá trình huấn luyện
            print(f"Lỗi khi huấn luyện mô hình: {e}")
            self.is_trained = False # Đảm bảo cờ trạng thái là False nếu huấn luyện thất bại
            return False

    def get_model_performance(self):
        """
        Trả về thông tin hiệu suất của mô hình (MAE và R2).
        Trả về None nếu mô hình chưa được huấn luyện.
        """
        if not self.is_trained:
            return None
        return {
            'mae': self.mae,
            'r2': self.r2
        }

    def get_categorical_levels(self, category_name):
        """
        Lấy danh sách các mức độ (levels) của một biến phân loại đã được mã hóa.
        category_name: Tên của cột gốc (ví dụ: 'Trình độ', 'Chức vụ').
        """
        encoder = self.encoders.get(category_name)
        if encoder is None:
            # Nếu encoder cho category_name không tồn tại (chưa được huấn luyện), trả về danh sách rỗng
            return []
        return list(encoder.classes_) # Trả về các lớp (categories) đã học của encoder

    def predict_salary(self, experience, education, certificate, night_shift, overtime,
                       position, contract_type, special_skills, work_area, client_type, allowances_percentage):
        """
        Dự đoán lương với thông tin đã nhập từ người dùng.
        Thực hiện kiểm tra đầu vào và mã hóa các biến phân loại trước khi dự đoán.
        """
        if not self.is_trained:
            # Ném lỗi nếu mô hình chưa được huấn luyện trước khi dự đoán
            raise Exception("Mô hình chưa được huấn luyện. Vui lòng huấn luyện mô hình trước.")

        try:
            # --- Xác thực và mã hóa dữ liệu đầu vào ---
            # 1. Kinh nghiệm: Đảm bảo giá trị nằm trong phạm vi hợp lý
            if not (0 <= experience <= 50):
                raise ValueError("Kinh nghiệm phải là số và nằm trong khoảng từ 0 đến 50 năm.")

            # 2. Trình độ học vấn: Kiểm tra xem trình độ có hợp lệ không và mã hóa
            if education not in self.encoders['Trình độ'].classes_:
                raise ValueError(f"Trình độ '{education}' không hợp lệ! Chọn: {', '.join(self.encoders['Trình độ'].classes_)}")
            edu_encoded = self.encoders['Trình độ'].transform([education])[0]

            # 6. Chức vụ: Kiểm tra và mã hóa chức vụ
            if position not in self.encoders['Chức vụ'].classes_:
                raise ValueError(f"Chức vụ '{position}' không hợp lệ! Chọn: {', '.join(self.encoders['Chức vụ'].classes_)}")
            position_encoded = self.encoders['Chức vụ'].transform([position])[0]

            # 7. Loại hợp đồng: Kiểm tra và mã hóa loại hợp đồng
            if contract_type not in self.encoders['Loại hợp đồng'].classes_:
                raise ValueError(f"Loại hợp đồng '{contract_type}' không hợp lệ! Chọn: {', '.join(self.encoders['Loại hợp đồng'].classes_)}")
            contract_type_encoded = self.encoders['Loại hợp đồng'].transform([contract_type])[0]

            # 9. Khu vực làm việc: Kiểm tra và mã hóa khu vực
            if work_area not in self.encoders['Khu vực làm việc'].classes_:
                raise ValueError(f"Khu vực làm việc '{work_area}' không hợp lệ! Chọn: {', '.join(self.encoders['Khu vực làm việc'].classes_)}")
            work_area_encoded = self.encoders['Khu vực làm việc'].transform([work_area])[0]

            # 10. Loại hình mục tiêu: Kiểm tra và mã hóa loại hình mục tiêu
            if client_type not in self.encoders['Loại hình mục tiêu'].classes_:
                raise ValueError(f"Loại hình mục tiêu '{client_type}' không hợp lệ! Chọn: {', '.join(self.encoders['Loại hình mục tiêu'].classes_)}")
            client_type_encoded = self.encoders['Loại hình mục tiêu'].transform([client_type])[0]

            # 11. Tỷ lệ phụ cấp: Kiểm tra giá trị tỷ lệ phần trăm hợp lệ (từ 0 đến 30%)
            if not (0 <= allowances_percentage <= 0.30):
                raise ValueError("Tỷ lệ phụ cấp phải là số từ 0 đến 30%.")

            # Tạo một DataFrame mới từ dữ liệu đầu vào đã được mã hóa.
            # Đảm bảo thứ tự các cột phải khớp CHÍNH XÁC với thứ tự các cột đã dùng để huấn luyện mô hình (X_train)
            new_data = pd.DataFrame([[
                experience, edu_encoded, certificate, night_shift, overtime,
                position_encoded, contract_type_encoded, special_skills,
                work_area_encoded, client_type_encoded, allowances_percentage
            ]], columns=[
                "Kinh nghiệm", "Trình độ_encoded", "Chứng chỉ", "Ca đêm", "Làm thêm",
                "Chức vụ_encoded", "Loại hợp đồng_encoded", "Kỹ năng đặc thù",
                "Khu vực làm việc_encoded", "Loại hình mục tiêu_encoded", "Tỷ lệ phụ cấp"
            ])

            # Dự đoán lương sử dụng mô hình đã huấn luyện (đây là mức lương cơ bản từ ML)
            predicted_salary = self.model.predict(new_data)[0]

            return predicted_salary
        except ValueError as ve:
            # Xử lý các lỗi liên quan đến giá trị đầu vào không hợp lệ
            raise ValueError(f"Lỗi xác thực dữ liệu đầu vào: {ve}")
        except Exception as e:
            # Xử lý các lỗi khác trong quá trình dự đoán (ví dụ: mô hình không hợp lệ)
            raise Exception(f"Lỗi trong quá trình dự đoán: {e}")

# Khởi tạo một đối tượng SalaryPredictionEngine toàn cục.
# Đối tượng này sẽ được sử dụng bởi ứng dụng Flask để huấn luyện mô hình và thực hiện dự đoán.
prediction_engine = SalaryPredictionEngine()
