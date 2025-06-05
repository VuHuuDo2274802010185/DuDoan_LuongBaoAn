# Main.py - Flask Web Application cho ứng dụng dự đoán lương nhân viên

# Import các module cần thiết từ Flask và các file Python tùy chỉnh
from flask import Flask, render_template, request, jsonify # Flask: Framework web; render_template: để render HTML; request: xử lý yêu cầu HTTP; jsonify: trả về JSON
import os # Thư viện để tương tác với hệ điều hành (ví dụ: kiểm tra/tạo thư mục, biến môi trường)
from Predict_engine import prediction_engine # Import đối tượng engine dự đoán lương đã khởi tạo từ Predict_engine.py
from Create_templates import create_html_template # Import hàm để tạo file HTML template
import sys # Thư viện để truy cập các tham số và hàm hệ thống (sử dụng cho sys.stderr)
from dotenv import load_dotenv # Import hàm để tải biến môi trường từ file .env

# Tải các biến môi trường từ file .env
load_dotenv()

# Khởi tạo ứng dụng Flask
app = Flask(__name__) # __name__ giúp Flask tìm đúng thư mục resources

# --- Khởi tạo và huấn luyện mô hình khi ứng dụng bắt đầu ---
# Sử dụng ngữ cảnh ứng dụng để đảm bảo mô hình được huấn luyện một lần duy nhất khi server khởi động
with app.app_context():
    print("🔄 Đang khởi tạo và huấn luyện mô hình...", file=sys.stderr)
    # Gọi phương thức train_model của prediction_engine
    success = prediction_engine.train_model()
    if success:
        performance = prediction_engine.get_model_performance()
        print(f"✅ Mô hình đã được huấn luyện thành công!", file=sys.stderr)
        print(f"📊 Sai số tuyệt đối trung bình (MAE): {performance['mae']:.2f} VND", file=sys.stderr)
        print(f"📊 Hệ số xác định (R2): {performance['r2']:.4f}", file=sys.stderr)
    else:
        print("❌ Lỗi khi khởi tạo hoặc huấn luyện mô hình!", file=sys.stderr)

# --- Định nghĩa các Routes (đường dẫn URL) của ứng dụng ---

@app.route('/')
def home():
    """
    Route cho trang chủ của ứng dụng.
    Hiển thị form dự đoán lương và thông tin về hiệu suất mô hình.
    """
    # Lấy danh sách các trình độ học vấn từ prediction_engine để hiển thị trong dropdown
    education_levels = prediction_engine.get_categorical_levels('Trình độ')
    position_levels = prediction_engine.get_categorical_levels('Chức vụ')
    contract_types = prediction_engine.get_categorical_levels('Loại hợp đồng')
    work_areas = prediction_engine.get_categorical_levels('Khu vực làm việc')
    client_types = prediction_engine.get_categorical_levels('Loại hình mục tiêu')

    # Lấy thông tin hiệu suất mô hình để hiển thị trên trang
    performance = prediction_engine.get_model_performance()

    # Lấy API Key từ biến môi trường để truyền cho frontend
    gemini_api_key = os.getenv('GEMINI_API_KEY', '') # Lấy GEMINI_API_KEY, nếu không có thì trả về chuỗi rỗng

    # Render file index.html và truyền các biến vào template
    return render_template('index.html',
                           education_levels=education_levels,
                           position_levels=position_levels,
                           contract_types=contract_types,
                           work_areas=work_areas,
                           client_types=client_types,
                           performance=performance,
                           gemini_api_key=gemini_api_key) # Truyền API key tới template

@app.route('/predict', methods=['POST'])
def predict(): # Đây là hàm đồng bộ, chỉ xử lý dự đoán ML cơ bản
    """
    API endpoint để nhận dữ liệu từ form và trả về dự đoán lương cơ bản (từ mô hình ML).
    Chỉ chấp nhận yêu cầu POST.
    """
    try:
        # Ghi log thông tin request để debug
        print(f"Incoming request headers: {request.headers}", file=sys.stderr)
        print(f"Is JSON: {request.is_json}", file=sys.stderr)
        print(f"Raw data: {request.get_data(as_text=True)}", file=sys.stderr)

        # Lấy dữ liệu gửi từ frontend (dạng JSON)
        if not request.is_json:
            print("Request is not JSON. Expected Content-Type: application/json", file=sys.stderr)
            raise ValueError("Invalid Content-Type. Expected application/json.")

        data = request.get_json()

        if not isinstance(data, dict):
            print(f"Received data is not a dictionary: {data}", file=sys.stderr)
            raise ValueError("Invalid JSON format. Expected a JSON object.")

        # Trích xuất và chuyển đổi dữ liệu từ yêu cầu JSON
        # Đảm bảo chuyển đổi đúng kiểu dữ liệu và kiểm tra các trường bắt buộc
        experience = float(data.get('experience'))
        education = data.get('education', '').strip().upper() # .strip().upper() để chuẩn hóa dữ liệu
        certificate = int(data.get('certificate', 0)) # Mặc định là 0 nếu không có
        night_shift = int(data.get('night_shift', 0))
        overtime = int(data.get('overtime', 0))

        # Các yếu tố bổ sung
        position = data.get('position', '').strip()
        contract_type = data.get('contract_type', '').strip()
        special_skills = int(data.get('special_skills', 0))
        work_area = data.get('work_area', '').strip()
        client_type = data.get('client_type', '').strip()
        allowances_percentage = float(data.get('allowances_percentage', 0.0))
        
        # ai_prompt không được xử lý ở đây, nó được xử lý trực tiếp ở frontend JS

        # Gọi phương thức predict_salary từ prediction_engine để nhận dự đoán lương cơ bản từ mô hình ML
        predicted_salary = prediction_engine.predict_salary(
            experience, education, certificate, night_shift, overtime,
            position, contract_type, special_skills, work_area, client_type, allowances_percentage
        )

        # Chuẩn bị dữ liệu kết quả để gửi về client dưới dạng JSON
        # Chỉ trả về lương dự đoán cơ bản từ ML
        result = {
            'success': True, # Cờ thành công
            'data': {
                'experience': experience,
                'education': education,
                'certificate': certificate,
                'night_shift': night_shift,
                'overtime': overtime,
                'position': position,
                'contract_type': contract_type,
                'special_skills': special_skills,
                'work_area': work_area,
                'client_type': client_type,
                'allowances_percentage': allowances_percentage,
                'predicted_salary': round(predicted_salary, 0), # Làm tròn lương dự đoán
                'predicted_salary_year': round(predicted_salary * 12, 0) # Lương dự đoán hàng năm
            }
        }
        return jsonify(result) # Trả về kết quả JSON

    except (ValueError, TypeError) as e:
        # Xử lý lỗi khi dữ liệu đầu vào không hợp lệ (ví dụ: sai kiểu, thiếu trường)
        print(f"Input data error: {e}", file=sys.stderr)
        return jsonify({
            'success': False,
            'error': f"Dữ liệu đầu vào không hợp lệ: {e}"
        }), 400 # Mã trạng thái HTTP 400 Bad Request

    except Exception as e:
        # Xử lý các lỗi chung khác
        print(f"General prediction error: {e}", file=sys.stderr)
        return jsonify({
            'success': False,
            'error': f"Đã xảy ra lỗi trong quá trình dự đoán: {e}"
        }), 500 # Mã trạng thái HTTP 500 Internal Server Error

@app.route('/api/model-info')
def model_info():
    """
    API endpoint để lấy thông tin về mô hình (hiệu suất, trình độ học vấn, v.v.).
    """
    performance = prediction_engine.get_model_performance()
    
    # Lấy tất cả các mức độ của các biến phân loại để hiển thị qua API
    education_levels = prediction_engine.get_categorical_levels('Trình độ')
    position_levels = prediction_engine.get_categorical_levels('Chức vụ')
    contract_types = prediction_engine.get_categorical_levels('Loại hợp đồng')
    work_areas = prediction_engine.get_categorical_levels('Khu vực làm việc')
    client_types = prediction_engine.get_categorical_levels('Loại hình mục tiêu')

    return jsonify({
        'performance': performance,
        'education_levels': education_levels,
        'position_levels': position_levels,
        'contract_types': contract_types,
        'work_areas': work_areas,
        'client_types': client_types,
        'is_trained': prediction_engine.is_trained
    })

# --- Khởi chạy ứng dụng Flask ---
if __name__ == '__main__':
    # Tạo thư mục 'templates' nếu nó chưa tồn tại.
    # Điều này đảm bảo rằng file HTML template có thể được lưu đúng chỗ.
    if not os.path.exists('templates'):
        os.makedirs('templates')

    # Tạo (hoặc cập nhật) file HTML template index.html
    # Bước này sẽ tạo ra file HTML với logic AI và yêu cầu API key ở JS
    create_html_template()

    print("🚀 Khởi động ứng dụng Flask...", file=sys.stderr)
    print("📱 Truy cập ứng dụng tại: http://localhost:5000", file=sys.stderr)
    # Chạy ứng dụng Flask
    # debug=True: Bật chế độ debug (tự động tải lại khi code thay đổi, hiển thị lỗi chi tiết)
    # host='0.0.0.0': Cho phép truy cập từ mọi địa chỉ IP (cần cho môi trường container/cloud)
    # port=5000: Ứng dụng sẽ chạy trên cổng 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
