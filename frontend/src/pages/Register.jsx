export default function Register() {
  return (
    <div className="auth-container">
      <h2>Đăng Ký</h2>
      <form className="auth-form">
        <input type="text" placeholder="Tên đăng nhập" />
        <input type="text" placeholder="Email/Số điện thoại" />
        <input type="password" placeholder="Mật khẩu" />
        <button type="submit">ĐĂNG KÝ</button>
      </form>
    </div>
  );
}
