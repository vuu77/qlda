<<<<<<< HEAD
# IT Project Management

## 1. Tạo database
Mở SQL Server Management Studio và chạy file `SQLQuery4.sql`.

## 2. Sửa kết nối SQL Server
Mở file `backend/database.py` và sửa `SERVER` nếu máy bạn không dùng `./SQLEXPRESS`.
Ví dụ:
- `r'.\\SQLEXPRESS'`
- `r'ASUS\\SQLEXPRESS'`
- `r'localhost\\SQLEXPRESS'`

## 3. Chạy backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Nếu backend chạy đúng, mở được:
`http://127.0.0.1:8000/docs`

## 4. Chạy frontend
Tại thư mục gốc project:
```bash
python -m http.server 8080 -d frontend
```
Mở:
`http://127.0.0.1:8080/login.html`

## Tài khoản mẫu
- Email: `admin@project.local`
- Mật khẩu: `123456`

## Chức năng
- Đăng ký / đăng nhập
- Quản lý theo mã dự án
- Quản lý bảng công việc
- Ước lượng thời gian expert
- Ước lượng chi phí
- Quản lý lịch trình dự án
- Lưu dữ liệu thật bằng SQL Server
=======
# quanlyduan
quanlyduan
>>>>>>> d1fa65ab0f382a93e9e21e2b5ad18160b35f250a
