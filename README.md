# SystemChatBot - Hướng dẫn sử dụng

## 1. Tổng quan
Hệ thống ChatBot hỗ trợ quản lý index, upload file, embedding dữ liệu lên Pinecone, lưu trữ file trên MinIO, đồng bộ trạng thái và vector_ids giữa backend và frontend.

## 2. Chức năng chính

## 3. Hướng dẫn sử dụng

### 3.1. Đăng nhập

### 3.2. Tạo index
    - Tham số: `name`, `dimension`
    - Trả về: thông tin index vừa tạo

### 3.3. Liệt kê index
    - Trả về: danh sách các index của user

### 3.4. Xóa index
    - Tham số: `name` (tên index)
    - Trả về: thông báo xóa thành công

### 3.5. Upload file
    - Tham số: file
    - Trả về: thông tin file

### 3.6. Embedding file
    - Thực hiện: lấy file từ MinIO, tách chunk, embedding, upsert Pinecone, lưu vector_ids vào bảng `file_vector_maps`, cập nhật trạng thái file thành `embedded`.
    - Trả về: trạng thái embedding, chi tiết vector_ids

### 3.7. Hiển thị trạng thái file

### 3.8. Truy vấn dữ liệu

## 4. Luồng hoạt động backend
    1. Lấy file từ MinIO
    2. Tách chunk bằng Preprocessor
    3. Sinh embedding bằng OpenAI
    4. Upsert lên Pinecone
    5. Lấy danh sách vector_ids vừa upsert
    6. Lưu vector_ids vào bảng `file_vector_maps` (update nếu đã tồn tại)
    7. Cập nhật trạng thái file thành `embedded`
    8. Trả về kết quả cho frontend

## 5. Lưu ý

## 6. Tham khảo API

## 7. Liên hệ hỗ trợ

## 8. Lưu trữ database
    - Người dùng (users)
    - Index vector (vector_indexes)
    - File metadata (index_files)
    - Mapping vector_ids (file_vector_maps)
    - Lịch sử chat, message, metadata

## 9. Chatbot RAG (Retrieval-Augmented Generation)
    1. Người dùng gửi câu hỏi qua giao diện chat
    2. Backend nhận câu hỏi, thực hiện truy vấn Pinecone để lấy các chunk liên quan
    3. Kết hợp nội dung truy xuất với câu hỏi, gửi tới mô hình ngôn ngữ (OpenAI, v.v.) để sinh câu trả lời
    4. Trả kết quả về frontend
    - Truy vấn vector: sử dụng Pinecone để tìm các chunk gần nhất với câu hỏi
    - Sinh câu trả lời: dùng LLM (GPT, v.v.) kết hợp context truy xuất

## 10. Mở rộng

File này mô tả chi tiết chức năng, luồng hoạt động và cách sử dụng hệ thống SystemChatBot.
# SystemChatBot

## Tổng quan

SystemChatBot là hệ thống ChatBot hỗ trợ quản lý, truy vấn dữ liệu văn bản lớn với các tính năng:
- Quản lý index (vector database) trên Pinecone
- Upload, embedding file, lưu trữ trên MinIO
- Tích hợp xác thực người dùng, lưu lịch sử chat, hỗ trợ multi-user
- Truy vấn dữ liệu theo mô hình RAG (Retrieval-Augmented Generation)
- Giao diện web hiện đại với React + Vite

## Kiến trúc

- **Backend:** FastAPI, SQLAlchemy, Pinecone, MinIO, Redis, OpenAI/LangChain/LangGraph
- **Frontend:** React (Vite), giao tiếp qua REST API
- **Database:** PostgreSQL (metadata, user, chat, mapping vector)
- **Vector DB:** Pinecone (lưu embedding)
- **Object Storage:** MinIO (lưu file gốc)
- **Memory:** Redis (lưu 20 message gần nhất mỗi user/chat)

## Chức năng chính

- Đăng nhập, xác thực JWT
- Tạo, xóa, liệt kê index
- Upload file PDF vào index
- Embedding file (tách chunk, sinh vector, upsert Pinecone)
- Lưu vector_ids vào database
- Hiển thị trạng thái file (uploaded/embedded)
- Truy vấn, hỏi đáp trên dữ liệu đã embedding
- Lưu lịch sử chat, hỗ trợ multi-user

## Hướng dẫn sử dụng

### 1. Cài đặt

#### Backend
```bash
# Clone repo

cd SystemChatBot

# Tạo và kích hoạt môi trường (conda hoặc venv)
conda create -n chatbot python=3.10
conda activate chatbot

# Cài đặt requirements
pip install -r requirements.txt

# Chỉnh sửa file .env (nếu cần) cho thông tin DB, MinIO, Pinecone, Redis, OpenAI
# Khởi động backend
uvicorn backend.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Docker (nếu dùng)
```bash
docker-compose up -d
```

### 2. Sử dụng

- Truy cập `http://localhost:5173` (frontend)
- Đăng nhập bằng tài khoản đã đăng ký
- Tạo index, upload file, nhấn "Embed" để sinh vector
- Chọn index, bắt đầu chat với dữ liệu đã embedding

### 3. API chính

- Đăng nhập: `POST /api/auth/login`
- Tạo index: `POST /api/indexes/`
- Liệt kê index: `GET /api/indexes/`
- Xóa index: `DELETE /api/indexes/{name}`
- Upload file: `POST /api/indexes/{index_id}/upload`
- Embedding file: `POST /api/indexes/{index_name}/{file_name}`
- Gửi tin nhắn chat: `POST /api/chat/sendMessage` (body: content, index_name)

### 4. Lưu ý

- Luôn gửi token xác thực (JWT) khi gọi các API bảo mật
- Đảm bảo các service (MinIO, Pinecone, Redis, PostgreSQL) đang chạy
- Nếu gặp lỗi embedding hoặc trạng thái không cập nhật, kiểm tra lại kết nối backend và database

### 5. Mở rộng

- Có thể tích hợp thêm nguồn dữ liệu, mô hình LLM khác, hoặc các chức năng phân tích nâng cao
- Đảm bảo bảo mật dữ liệu và xác thực người dùng khi truy vấn hoặc upload dữ liệu

---

**Mọi thắc mắc hoặc cần hỗ trợ, vui lòng liên hệ admin hoặc tạo issue trên GitHub.**

---

Bạn muốn bổ sung phần nào chi tiết hơn (ví dụ: hướng dẫn phát triển, cấu trúc code, ví dụ API request) hãy cho biết!



