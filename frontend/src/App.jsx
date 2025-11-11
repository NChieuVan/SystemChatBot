
import { Routes, Route, NavLink, Navigate, useNavigate } from "react-router-dom";
import Chat from "./pages/Chat";
import Database from "./pages/Database";
import Login from "./pages/Login";
import RequireAuth from "./routes/RequireAuth";

export default function App() {
  const authed = !!localStorage.getItem("token");
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login", { replace: true });
  };

  return (
    <div>
      {authed && (
        <nav className="top-nav">
          <div className="brand">
            <div className="logo" />
            AI Chatbot Dashboard
          </div>
          <div className="nav-links">
            <NavLink to="/chat" className={({isActive}) => isActive ? "active" : undefined}>Trang chính</NavLink>
            <NavLink to="/database" className={({isActive}) => isActive ? "active" : undefined}>Database</NavLink>
            <button className="logout-btn" onClick={logout}>Đăng xuất</button>
          </div>
        </nav>
      )}

      <Routes>
        <Route path="/" element={<Navigate to={authed ? "/chat" : "/login"} replace />} />
        <Route path="/login" element={<Login />} />

        <Route element={<RequireAuth />}>
          <Route path="/chat" element={<Chat />} />
          <Route path="/database" element={<Database />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}
