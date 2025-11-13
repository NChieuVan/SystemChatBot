import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { register } from "../services/authService";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [err, setErr] = useState("");
  const [success, setSuccess] = useState("");
  const nav = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setErr("");
    setSuccess("");
    if (!email || !password) {
      setErr("Vui lòng nhập email và mật khẩu.");
      return;
    }
    try {
      const res = await register(email, password, name);
      setSuccess("Đăng ký thành công! Bạn có thể đăng nhập.");
    } catch (error) {
      setErr(error.message || "Đăng ký thất bại.");
    }
  };

  return (
    <div className="center">
      <div className="auth-card">
        <h2>Đăng ký tài khoản</h2>
        <form onSubmit={submit}>
          <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
          <input type="password" placeholder="Mật khẩu" value={password} onChange={e => setPassword(e.target.value)} />
          <input placeholder="Tên (tuỳ chọn)" value={name} onChange={e => setName(e.target.value)} />
          {err && <div style={{color: "#ff9aa2", marginBottom: 10}}>{err}</div>}
          {success && <div style={{color: "#4caf50", marginBottom: 10}}>{success}</div>}
          <button type="submit">Đăng ký</button>
        </form>
        <div className="note" style={{marginTop:10}}>
          Đã có tài khoản? <Link to="/login">Quay về đăng nhập</Link>
        </div>
      </div>
    </div>
  );
}