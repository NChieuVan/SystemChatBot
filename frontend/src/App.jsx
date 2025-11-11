import { Routes, Route, Link } from "react-router-dom";
import Chat from "./pages/Chat";
import Database from "./pages/Database";
import Login from "./pages/Login";
import Register from "./pages/Register";
import "./App.css";

export default function App() {
  return (
    <div>
      <nav className="navbar">
        <h2>ChatBot <span>VanJR</span></h2>
        <div className="nav-links">
          <Link to="/">Chat</Link>
          <Link to="/database">Database</Link>
          <Link to="/login">Đăng nhập</Link>
          <Link to="/register">Đăng ký</Link>
        </div>
      </nav>

      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/database" element={<Database />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </div>
  );
}
