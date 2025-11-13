
import { useState } from "react";
import { useLocation, useNavigate, Link } from "react-router-dom";
import { login } from "../services/authService";  

export default function Login() {
  const [u, setU] = useState("");
  const [p, setP] = useState("");
  const [err, setErr] = useState("");
  const nav = useNavigate();
  const loc = useLocation();
  const from = loc.state?.from?.pathname || "/chat";

  const submit = async(e) => {
    e.preventDefault();
    if(!u || !p) {
      setErr("Vui lòng nhập đầy đủ thông tin.");
      return;
    }
    try {
      const data = await login(u, p);
      nav(from, { replace: true });
    } catch (error) {
      setErr(error.message || "Đăng nhập thất bại.");
    }
  };

  return (
    <div className="center">
      <div className="auth-card">
        <h2>Đăng nhập</h2>
        <form onSubmit={submit}>
          <input placeholder="Email / Số điện thoại" value={u} onChange={(e)=>setU(e.target.value)} />
          <input type="password" placeholder="Mật khẩu" value={p} onChange={(e)=>setP(e.target.value)} />
          {err && <div style={{color: "#ff9aa2", marginBottom: 10}}>{err}</div>}
          <button type="submit">Vào trang chính</button>
          <div className="note">* Đây là đăng nhập demo (mock). Backend sẽ tích hợp sau.</div>
        </form>
        <div className="note" style={{marginTop:10}}>
          Chưa có tài khoản? <Link to="/register">Đăng ký tài khoản</Link>
        </div>
      </div>
    </div>
  );
}
