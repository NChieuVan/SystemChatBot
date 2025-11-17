import { useEffect } from "react";

/**
 * Toast component
 * @param {string} message - Nội dung thông báo
 * @param {string} type - success | warning | error | info
 * @param {function} onClose - Hàm đóng toast
 * @param {number} duration - Thời gian tự ẩn (ms)
 */
export default function Toast({ message, type = "info", onClose, duration = 2500 }) {
  useEffect(() => {
    if (!message) return;
    const timer = setTimeout(() => onClose && onClose(), duration);
    return () => clearTimeout(timer);
  }, [message, duration, onClose]);

  if (!message) return null;

  let bg = "#2196f3";
  if (type === "success") bg = "#4caf50";
  else if (type === "warning") bg = "#ff9800";
  else if (type === "error") bg = "#f44336";

  return (
    <div style={{
      position: "fixed",
      top: 32,
      left: "50%",
      transform: "translateX(-50%)",
      zIndex: 9999,
      background: bg,
      color: "#fff",
      padding: "14px 32px",
      borderRadius: 8,
      boxShadow: "0 2px 12px #0003",
      fontSize: 16,
      minWidth: 220,
      textAlign: "center",
      display: "flex",
      alignItems: "center",
      gap: 12
    }}>
      <span style={{fontWeight:600}}>{message}</span>
      <button onClick={onClose} style={{background:"none",border:0,color:"#fff",fontSize:20,cursor:"pointer",marginLeft:8}}>&times;</button>
    </div>
  );
}
