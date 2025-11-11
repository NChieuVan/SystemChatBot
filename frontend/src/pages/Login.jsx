export default function Login() {
  return (
    <div className="auth-container">
      <h2>Đăng Nhập</h2>
      <form className="auth-form">
        <input type="text" placeholder="Email/Số điện thoại" />
        <input type="password" placeholder="Mật khẩu" />
        <button type="submit">ĐĂNG NHẬP</button>
        <a href="#">Quên mật khẩu?</a>
      </form>
    </div>
  );
}
