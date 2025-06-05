# Create_templates.py - Tạo file HTML template cho ứng dụng web (Với logic AI ở Frontend)

import os # Thư viện để tương tác với hệ điều hành, ví dụ: tạo thư mục

def create_html_template():
    """
    Tạo file HTML template chính cho ứng dụng dự đoán lương.
    Template này sử dụng Tailwind CSS để tối ưu hóa thiết kế responsive,
    và chứa logic JavaScript để gọi cả backend ML và API AI Gemini.
    """
    html_content = '''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dự Đoán Lương Nhân Viên (AI Enhanced)</title>
    <!-- Tải Tailwind CSS từ CDN để sử dụng các lớp tiện ích -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Thiết lập cấu hình Tailwind để sử dụng các lớp mặc định -->
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'], // Sử dụng font Inter hoặc sans-serif mặc định
                    },
                }
            }
        }
    </script>
</head>
<body class="bg-gradient-to-br from-indigo-500 to-purple-600 min-h-screen p-4 flex items-center justify-center font-sans">
    <div class="container bg-white rounded-xl shadow-2xl overflow-hidden max-w-3xl w-full mx-auto my-8">
        <div class="header bg-gradient-to-br from-gray-800 to-blue-500 text-white p-8 text-center rounded-t-xl">
            <h1 class="text-4xl font-bold mb-2">🎯 Dự Đoán Lương Nhân Viên</h1>
            <p class="opacity-90 text-lg">Sử dụng Machine Learning và AI để dự đoán mức lương phù hợp</p>
        </div>

        <div class="form-container p-8">
            <!-- Hiển thị thông tin mô hình nếu có dữ liệu hiệu suất -->
            {% if performance %}
            <div class="model-info bg-blue-50 border-l-4 border-blue-500 text-gray-800 p-4 rounded-lg mb-6 shadow-sm">
                <h4 class="text-xl font-semibold text-gray-700 mb-3">📊 Thông tin mô hình:</h4>
                <p class="text-gray-600 mb-1"><strong>Sai số tuyệt đối trung bình (MAE):</strong> {{ "%.2f"|format(performance.mae) }} VND</p>
                <p class="text-gray-600"><strong>Độ chính xác (R²):</strong> {{ "%.4f"|format(performance.r2) }}</p>
            </div>
            {% endif %}

            <form id="predictionForm" class="space-y-6">
                <!-- Hàng 1 -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="form-group">
                        <label for="experience" class="block text-gray-700 font-semibold mb-2 text-lg">💼 Số năm kinh nghiệm (0-50):</label>
                        <input type="number" id="experience" name="experience" min="0" max="50" step="0.1" required
                               class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-transparent transition duration-200 ease-in-out shadow-sm">
                    </div>

                    <div class="form-group">
                        <label for="education" class="block text-gray-700 font-semibold mb-2 text-lg">🎓 Trình độ học vấn:</label>
                        <select id="education" name="education" required
                                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-transparent transition duration-200 ease-in-out shadow-sm bg-white appearance-none">
                            {% for level in education_levels %}
                            <option value="{{ level }}">{{ level }}</option>
                            {% endfor %}
                        </select>
                    </div>
                </div>

                <!-- Hàng 2 -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="form-group">
                        <label for="position" class="block text-gray-700 font-semibold mb-2 text-lg">👨‍💼 Chức vụ:</label>
                        <select id="position" name="position" required
                                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-transparent transition duration-200 ease-in-out shadow-sm bg-white appearance-none">
                            {% for pos in position_levels %}
                            <option value="{{ pos }}">{{ pos }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="contract_type" class="block text-gray-700 font-semibold mb-2 text-lg">📄 Loại hợp đồng:</label>
                        <select id="contract_type" name="contract_type" required
                                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-transparent transition duration-200 ease-in-out shadow-sm bg-white appearance-none">
                            {% for type in contract_types %}
                            <option value="{{ type }}">{{ type }}</option>
                            {% endfor %}
                        </select>
                    </div>
                </div>

                <!-- Hàng 3 -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="form-group">
                        <label for="work_area" class="block text-gray-700 font-semibold mb-2 text-lg">📍 Khu vực làm việc:</label>
                        <select id="work_area" name="work_area" required
                                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-transparent transition duration-200 ease-in-out shadow-sm bg-white appearance-none">
                            {% for area in work_areas %}
                            <option value="{{ area }}">{{ area }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="client_type" class="block text-gray-700 font-semibold mb-2 text-lg">🏢 Loại hình mục tiêu:</label>
                        <select id="client_type" name="client_type" required
                                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-transparent transition duration-200 ease-in-out shadow-sm bg-white appearance-none">
                            {% for client in client_types %}
                            <option value="{{ client }}">{{ client }}</option>
                            {% endfor %}
                        </select>
                    </div>
                </div>

                <!-- Hàng 4: Checkboxes và Tỷ lệ phụ cấp -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="form-group flex flex-col justify-around">
                        <div class="flex items-center space-x-3 mb-4">
                            <input type="checkbox" id="certificate" name="certificate" value="1"
                                   class="h-5 w-5 text-blue-600 rounded border-gray-300 focus:ring-blue-500">
                            <label for="certificate" class="text-gray-700 font-medium text-lg">📜 Có chứng chỉ nghề nghiệp</label>
                        </div>
                        <div class="flex items-center space-x-3 mb-4">
                            <input type="checkbox" id="night_shift" name="night_shift" value="1"
                                   class="h-5 w-5 text-blue-600 rounded border-gray-300 focus:ring-blue-500">
                            <label for="night_shift" class="text-gray-700 font-medium text-lg">🌙 Làm ca đêm</label>
                        </div>
                        <div class="flex items-center space-x-3">
                            <input type="checkbox" id="overtime" name="overtime" value="1"
                                   class="h-5 w-5 text-blue-600 rounded border-gray-300 focus:ring-blue-500">
                            <label for="overtime" class="text-gray-700 font-medium text-lg">⏰ Làm thêm giờ</label>
                        </div>
                    </div>

                    <div class="form-group">
                        <div class="flex items-center space-x-3 mb-4">
                            <input type="checkbox" id="special_skills" name="special_skills" value="1"
                                   class="h-5 w-5 text-blue-600 rounded border-gray-300 focus:ring-blue-500">
                            <label for="special_skills" class="text-gray-700 font-medium text-lg">🥋 Có kỹ năng đặc thù (Võ thuật, PCCC)</label>
                        </div>
                        <label for="allowances_percentage" class="block text-gray-700 font-semibold mb-2 text-lg">💰 Tỷ lệ phụ cấp/phúc lợi (%):</label>
                        <input type="number" id="allowances_percentage" name="allowances_percentage" min="0" max="30" step="0.1" value="0"
                               class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-transparent transition duration-200 ease-in-out shadow-sm">
                        <p class="text-sm text-gray-500 mt-1">Nhập giá trị từ 0 đến 30 (ví dụ: 10 cho 10%)</p>
                    </div>
                </div>

                <!-- Hàng AI Insight -->
                <div class="form-group">
                    <label for="ai_prompt" class="block text-gray-700 font-semibold mb-2 text-lg">🧠 Gợi ý AI bổ sung (ví dụ: "Nhân viên có năng lực tốt", "Thị trường đang thiếu nhân sự"):</label>
                    <textarea id="ai_prompt" name="ai_prompt" rows="3"
                              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-transparent transition duration-200 ease-in-out shadow-sm"
                              placeholder="Nhập các yếu tố đặc biệt mà bạn muốn AI xem xét..."></textarea>
                </div>
                
                <button type="submit" class="btn w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition duration-300 ease-in-out transform hover:-translate-y-1 shadow-md hover:shadow-lg">
                    🔮 Dự Đoán Lương
                </button>
            </form>

            <!-- Khu vực hiển thị trạng thái tải -->
            <div id="loading" class="loading hidden text-center p-6 bg-blue-50 rounded-lg mt-6 shadow-sm">
                <div class="spinner border-t-4 border-blue-500 border-solid rounded-full w-10 h-10 animate-spin mx-auto mb-3"></div>
                <p id="loadingMessage" class="text-blue-700 font-medium">Đang xử lý...</p>
            </div>

            <!-- Khu vực hiển thị kết quả dự đoán hoặc lỗi -->
            <div id="result" class="result hidden mt-6 p-6 rounded-lg border-l-4 border-green-500 bg-green-50 shadow-md">
                <h3 class="text-2xl font-bold text-green-700 mb-4">💰 Kết Quả Dự Đoán</h3>
                <div id="resultContent" class="space-y-3"></div>
            </div>
        </div>
    </div>

    <script>
        // Hàm định dạng tiền tệ
        const formatCurrency = (amount) => {
            return Number(amount).toLocaleString('vi-VN', { style: 'currency', currency: 'VND' });
        };

        // Hàm hiển thị kết quả dự đoán thành công
        function displayResult(data) {
            const resultDiv = document.getElementById('result');
            const contentDiv = document.getElementById('resultContent');

            contentDiv.innerHTML = `
                <div class="flex justify-between items-center py-2 border-b border-green-200">
                    <span class="text-gray-700">🔹 Kinh nghiệm:</span>
                    <span class="font-medium text-green-800">${data.experience} năm</span>
                </div>
                <div class="flex justify-between items-center py-2 border-b border-green-200">
                    <span class="text-gray-700">🔹 Trình độ:</span>
                    <span class="font-medium text-green-800">${data.education}</span>
                </div>
                <div class="flex justify-between items-center py-2 border-b border-green-200">
                    <span class="text-gray-700">🔹 Chứng chỉ:</span>
                    <span class="font-medium text-green-800">${data.certificate ? '✅ Có' : '❌ Không'}</span>
                </div>
                <div class="flex justify-between items-center py-2 border-b border-green-200">
                    <span class="text-gray-700">🔹 Ca đêm:</span>
                    <span class="font-medium text-green-800">${data.night_shift ? '✅ Có' : '❌ Không'}</span>
                </div>
                <div class="flex justify-between items-center py-2 border-b border-green-200">
                    <span class="text-gray-700">🔹 Làm thêm:</span>
                    <span class="font-medium text-green-800">${data.overtime ? '✅ Có' : '❌ Không'}</span>
                </div>
                <div class="flex justify-between items-center py-2 border-b border-green-200">
                    <span class="text-gray-700">🔹 Chức vụ:</span>
                    <span class="font-medium text-green-800">${data.position}</span>
                </div>
                <div class="flex justify-between items-center py-2 border-b border-green-200">
                    <span class="text-gray-700">🔹 Loại hợp đồng:</span>
                    <span class="font-medium text-green-800">${data.contract_type}</span>
                </div>
                <div class="flex justify-between items-center py-2 border-b border-green-200">
                    <span class="text-gray-700">🔹 Kỹ năng đặc thù:</span>
                    <span class="font-medium text-green-800">${data.special_skills ? '✅ Có' : '❌ Không'}</span>
                </div>
                <div class="flex justify-between items-center py-2 border-b border-green-200">
                    <span class="text-gray-700">🔹 Khu vực làm việc:</span>
                    <span class="font-medium text-green-800">${data.work_area}</span>
                </div>
                <div class="flex justify-between items-center py-2 border-b border-green-200">
                    <span class="text-gray-700">🔹 Loại hình mục tiêu:</span>
                    <span class="font-medium text-green-800">${data.client_type}</span>
                </div>
                <div class="flex justify-between items-center py-2 border-b border-green-200">
                    <span class="text-gray-700">🔹 Tỷ lệ phụ cấp/phúc lợi:</span>
                    <span class="font-medium text-green-800">${(data.allowances_percentage * 100).toFixed(1)}%</span>
                </div>
                <div class="flex justify-between items-center py-2 border-b border-purple-200">
                    <span class="text-gray-700 font-semibold">✨ Điều chỉnh AI:</span>
                    <span class="font-medium text-purple-700">${(data.ai_adjustment_percentage * 100).toFixed(1)}% (${data.ai_insight_text})</span>
                </div>
                <div class="flex justify-between items-center py-2 pt-4 text-lg font-bold text-green-700">
                    <span>💰 Lương dự đoán/tháng:</span>
                    <span>${formatCurrency(data.predicted_salary)}</span>
                </div>
                <div class="flex justify-between items-center py-2 text-lg font-bold text-green-700">
                    <span>💰 Lương dự đoán/năm:</span>
                    <span>${formatCurrency(data.predicted_salary_year)}</span>
                </div>
            `;

            resultDiv.classList.remove('hidden'); // Hiển thị khối kết quả
            resultDiv.classList.remove('bg-red-50', 'border-red-500'); // Đảm bảo không có styling lỗi
            resultDiv.classList.add('bg-green-50', 'border-green-500'); // Thêm styling thành công
        }

        // Hàm hiển thị thông báo lỗi
        function displayError(error) {
            const resultDiv = document.getElementById('result');
            const contentDiv = document.getElementById('resultContent');

            contentDiv.innerHTML = `<p class="text-red-700 font-semibold text-lg"><strong>❌ Lỗi:</strong> ${error}</p>`;
            resultDiv.classList.remove('hidden'); // Hiển thị khối kết quả (với nội dung lỗi)
            resultDiv.classList.remove('bg-green-50', 'border-green-500'); // Xóa styling thành công
            resultDiv.classList.add('bg-red-50', 'border-red-500'); // Thêm styling lỗi
        }

        document.getElementById('predictionForm').addEventListener('submit', async function(e) {
            e.preventDefault(); // Ngăn chặn hành vi gửi form mặc định

            const formData = new FormData(this);
            const inputData = {
                experience: parseFloat(formData.get('experience')),
                education: formData.get('education'),
                certificate: formData.get('certificate') ? 1 : 0,
                night_shift: formData.get('night_shift') ? 1 : 0,
                overtime: formData.get('overtime') ? 1 : 0,
                position: formData.get('position'),
                contract_type: formData.get('contract_type'),
                special_skills: formData.get('special_skills') ? 1 : 0,
                work_area: formData.get('work_area'),
                client_type: formData.get('client_type'),
                allowances_percentage: parseFloat(formData.get('allowances_percentage')) / 100,
                ai_prompt: formData.get('ai_prompt') || '' // Lấy prompt AI hoặc chuỗi rỗng nếu không có
            };

            // Hiển thị trạng thái loading và ẩn kết quả/lỗi trước đó
            const loadingDiv = document.getElementById('loading');
            const loadingMessage = document.getElementById('loadingMessage');
            loadingDiv.classList.remove('hidden');
            loadingMessage.textContent = 'Đang dự đoán lương cơ bản...'; // Set initial loading message

            document.getElementById('result').classList.add('hidden');
            document.getElementById('result').classList.remove('error'); // Xóa lớp error nếu có

            let predicted_salary_ml_only;
            let ai_adjustment_percentage = 0;
            let ai_insight_text = "Không có gợi ý AI nào được cung cấp.";

            try {
                // Bước 1: Gửi yêu cầu đến Flask backend để lấy lương dự đoán cơ bản (chỉ ML)
                const ml_response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    // Gửi tất cả các dữ liệu ngoại trừ ai_prompt đến backend ML
                    body: JSON.stringify({
                        experience: inputData.experience,
                        education: inputData.education,
                        certificate: inputData.certificate,
                        night_shift: inputData.night_shift,
                        overtime: inputData.overtime,
                        position: inputData.position,
                        contract_type: inputData.contract_type,
                        special_skills: inputData.special_skills,
                        work_area: inputData.work_area,
                        client_type: inputData.client_type,
                        allowances_percentage: inputData.allowances_percentage
                    })
                });
                const ml_result = await ml_response.json();

                if (!ml_response.ok || !ml_result.success) {
                    throw new Error(ml_result.error || 'Lỗi khi dự đoán lương cơ bản từ ML.');
                }
                predicted_salary_ml_only = ml_result.data.predicted_salary;

                // Bước 2: Nếu có ai_prompt, gọi Gemini API để lấy điều chỉnh AI
                if (inputData.ai_prompt.trim() !== '') {
                    loadingMessage.textContent = 'Đang điều chỉnh lương bằng AI...'; // Update loading message for AI
                    const features_summary = `Kinh nghiệm: ${inputData.experience} năm, Trình độ: ${inputData.education}, Chứng chỉ: ${inputData.certificate ? 'Có' : 'Không'}, Ca đêm: ${inputData.night_shift ? 'Có' : 'Không'}, Làm thêm: ${inputData.overtime ? 'Có' : 'Không'}, Chức vụ: ${inputData.position}, Loại HĐ: ${inputData.contract_type}, Kỹ năng đặc thù: ${inputData.special_skills ? 'Có' : 'Không'}, Khu vực: ${inputData.work_area}, Loại mục tiêu: ${inputData.client_type}, Phụ cấp: ${(inputData.allowances_percentage * 100).toFixed(1)}%`;
                    
                    const prompt_text = (
                        `Dựa trên hồ sơ nhân viên sau: ${features_summary}. ` +
                        `Và yêu cầu cụ thể từ người dùng: '${inputData.ai_prompt}'. ` +
                        `Bạn đề xuất mức lương dự đoán (${predicted_salary_ml_only} VND) nên được điều chỉnh bao nhiêu phần trăm? ` +
                        `Chỉ trả lời bằng một giá trị phần trăm (ví dụ: '+5%', '-2%', '0%'). ` +
                        `Nếu không có sự điều chỉnh rõ ràng nào được ngụ ý, hãy trả lời bằng '0%'.` +
                        `Ví dụ: +7.5% hoặc -3% hoặc 0% kèm theo lý do ngắn gọn.`
                    );

                    let chatHistory = [];
                    chatHistory.push({ role: "user", parts: [{ text: prompt_text }] });
                    const payload = { contents: chatHistory };
                    // *******************************************************************
                    // API KEY ĐƯỢC TRUYỀN TỪ FLASK SERVER QUA TEMPLATE
                    const apiKey = "{{ gemini_api_key }}";
                    // *******************************************************************
                    const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

                    if (!apiKey || apiKey === 'YOUR_GEMINI_API_KEY_HERE') { // Kiểm tra nếu API Key không hợp lệ
                        throw new Error("API Key cho Gemini AI chưa được cung cấp hoặc không hợp lệ. Vui lòng kiểm tra file .env và khởi động lại server.");
                    }

                    const ai_response = await fetch(apiUrl, {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify(payload)
                            });
                    const ai_result = await ai_response.json();

                    if (ai_result.candidates && ai_result.candidates.length > 0 &&
                        ai_result.candidates[0].content && ai_result.candidates[0].content.parts &&
                        ai_result.candidates[0].content.parts.length > 0) {
                        ai_insight_text = ai_result.candidates[0].content.parts[0].text;
                        // Trích xuất phần trăm từ phản hồi AI
                        const match = ai_insight_text.match(/([+-]?\d+\.?\d*)%/);
                        if (match) {
                            ai_adjustment_percentage = parseFloat(match[1]) / 100;
                        } else {
                            ai_adjustment_percentage = 0; // Mặc định không điều chỉnh nếu không tìm thấy %
                            ai_insight_text = "AI không đưa ra điều chỉnh rõ ràng từ phản hồi: " + (ai_insight_text.length > 100 ? ai_insight_text.substring(0, 100) + "..." : ai_insight_text);
                        }
                    } else {
                        // Log the full AI result to console for debugging
                        console.error("AI API response was not valid:", ai_result);
                        let errorDetail = "Cấu trúc phản hồi không hợp lệ.";
                        if (ai_result.error && ai_result.error.message) {
                            errorDetail = `Lỗi từ AI: ${ai_result.error.message}`;
                        } else if (JSON.stringify(ai_result).length > 2) {
                            errorDetail = `Phản hồi: ${JSON.stringify(ai_result).substring(0, 100)}...`;
                        }
                        ai_insight_text = `Không nhận được phản hồi hợp lệ từ AI. (${errorDetail})`;
                        ai_adjustment_percentage = 0;
                    }
                }

                // Áp dụng điều chỉnh từ AI vào lương dự đoán cơ bản
                const final_predicted_salary = predicted_salary_ml_only * (1 + ai_adjustment_percentage);

                // Chuẩn bị dữ liệu để hiển thị
                const displayData = {
                    ...inputData, // Giữ nguyên các input ban đầu
                    predicted_salary: final_predicted_salary,
                    predicted_salary_year: final_predicted_salary * 12,
                    ai_adjustment_percentage: ai_adjustment_percentage,
                    ai_insight_text: ai_insight_text
                };
                displayResult(displayData);

            } catch (error) {
                console.error("Error during prediction:", error); // Log detailed error
                displayError('Lỗi: ' + error.message);
            } finally {
                loadingDiv.classList.add('hidden'); // Always hide loading indicator
            }
        });
    </script>
</body>
</html>'''

    # Tạo thư mục 'templates' nếu nó chưa tồn tại
    template_dir = 'templates'
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)
        print(f"Đã tạo thư mục: {template_dir}")

    # Ghi nội dung HTML vào file index.html trong thư mục 'templates'
    file_path = os.path.join(template_dir, 'index.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Đã tạo file HTML template: {file_path}")

