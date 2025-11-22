# SystemChatBot - Hướng dẫn sử dụng

## 1. Tổng quan
Hệ thống ChatBot hỗ trợ quản lý index, upload file, embedding dữ liệu lên Pinecone, lưu trữ file trên MinIO, đồng bộ trạng thái và vector_ids giữa backend và frontend.

## 2. Chức năng chính
- Đăng nhập, xác thực người dùng
- Tạo, xóa, liệt kê index (vector database)
- Upload file vào index
- Embedding file (tách chunk, sinh vector, upsert Pinecone)
- Lưu vector_ids vào database
- Hiển thị trạng thái file (uploaded/embedded)
- Tìm kiếm, truy vấn dữ liệu

## 3. Hướng dẫn sử dụng

### 3.1. Đăng nhập
- Truy cập giao diện frontend, nhập email và mật khẩu để đăng nhập.
- Token xác thực sẽ được lưu và sử dụng cho các API tiếp theo.

### 3.2. Tạo index
- Vào trang quản lý index, nhấn "Tạo index".
- Nhập tên index, dimension (ví dụ: 1536 cho OpenAI embedding).
- Token xác thực sẽ được gửi kèm khi gọi API.
- API backend: `POST /api/indexes/`
    - Tham số: `name`, `dimension`
    - Trả về: thông tin index vừa tạo

### 3.3. Liệt kê index
- API backend: `GET /api/indexes/`
    - Trả về: danh sách các index của user

### 3.4. Xóa index
- API backend: `DELETE /api/indexes/{name}`
    - Tham số: `name` (tên index)
    - Trả về: thông báo xóa thành công

### 3.5. Upload file
- Chọn index, upload file PDF lên hệ thống.
- File sẽ được lưu vào MinIO, metadata lưu vào database.
- API backend: `POST /api/indexes/{index_id}/upload`
    - Tham số: file
    - Trả về: thông tin file

### 3.6. Embedding file
- Nhấn nút "Embed" trên giao diện file.
- API backend: `POST /api/indexes/{index_name}/{file_name}`
    - Thực hiện: lấy file từ MinIO, tách chunk, embedding, upsert Pinecone, lưu vector_ids vào bảng `file_vector_maps`, cập nhật trạng thái file thành `embedded`.
    - Trả về: trạng thái embedding, chi tiết vector_ids

### 3.7. Hiển thị trạng thái file
- Frontend sẽ gọi API lấy danh sách file, hiển thị trạng thái (uploaded/embedded).
- Sau khi embedding, trạng thái sẽ tự động cập nhật.

### 3.8. Truy vấn dữ liệu
- Tìm kiếm, hỏi đáp trên dữ liệu đã embedding (tùy vào chức năng mở rộng).

## 4. Luồng hoạt động backend
- Khi embedding file:
    1. Lấy file từ MinIO
    2. Tách chunk bằng Preprocessor
    3. Sinh embedding bằng OpenAI
    4. Upsert lên Pinecone
    5. Lấy danh sách vector_ids vừa upsert
    6. Lưu vector_ids vào bảng `file_vector_maps` (update nếu đã tồn tại)
    7. Cập nhật trạng thái file thành `embedded`
    8. Trả về kết quả cho frontend

## 5. Lưu ý
- Đảm bảo các service (MinIO, Pinecone, database) đang chạy.
- Token xác thực phải được gửi kèm khi gọi các API bảo mật.
- Nếu gặp lỗi embedding hoặc trạng thái không cập nhật, kiểm tra lại kết nối backend và database.

## 6. Tham khảo API
- Tạo index: `POST /api/indexes/`
- Liệt kê index: `GET /api/indexes/`
- Xóa index: `DELETE /api/indexes/{name}`
- Upload file: `POST /api/indexes/{index_id}/upload`
- Embedding file: `POST /api/indexes/{index_name}/{file_name}`

## 7. Liên hệ hỗ trợ
- Nếu cần hỗ trợ, liên hệ admin hoặc kiểm tra log backend để xác định nguyên nhân lỗi.

## 8. Lưu trữ database
- Hệ thống sử dụng PostgreSQL để lưu trữ các thông tin:
    - Người dùng (users)
    - Index vector (vector_indexes)
    - File metadata (index_files)
    - Mapping vector_ids (file_vector_maps)
    - Lịch sử chat, message, metadata
- Kết nối qua SQLAlchemy ORM, các bảng được định nghĩa trong `backend/models.py`.
- Dữ liệu embedding (vector) được lưu trên Pinecone, metadata mapping lưu trong bảng `file_vector_maps`.

## 9. Chatbot RAG (Retrieval-Augmented Generation)
- Chatbot sử dụng mô hình RAG để trả lời dựa trên dữ liệu đã embedding:
    1. Người dùng gửi câu hỏi qua giao diện chat
    2. Backend nhận câu hỏi, thực hiện truy vấn Pinecone để lấy các chunk liên quan
    3. Kết hợp nội dung truy xuất với câu hỏi, gửi tới mô hình ngôn ngữ (OpenAI, v.v.) để sinh câu trả lời
    4. Trả kết quả về frontend
- Các bước chính:
    - Truy vấn vector: sử dụng Pinecone để tìm các chunk gần nhất với câu hỏi
    - Sinh câu trả lời: dùng LLM (GPT, v.v.) kết hợp context truy xuất
- Lịch sử chat và metadata được lưu vào database để phục vụ truy vấn và phân tích sau này.

## 10. Mở rộng
- Có thể tích hợp thêm các nguồn dữ liệu khác, các mô hình LLM khác, hoặc các chức năng phân tích nâng cao.
- Đảm bảo bảo mật dữ liệu và xác thực người dùng khi truy vấn hoặc upload dữ liệu.

---
File này mô tả chi tiết chức năng, luồng hoạt động và cách sử dụng hệ thống SystemChatBot.



