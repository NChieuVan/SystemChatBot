import { useEffect, useState } from "react";
import { listChatsByUser, createChat, deleteChat, renameChat } from "../services/chatMock";
import { listIndexesFromAPI } from "../services/pineconeMock";

export default function ChatSidebar({ currentId, onSelect, onIndexSelect }) {
  const [chats, setChats] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [tempTitle, setTempTitle] = useState("");
  const [indexes, setIndexes] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState("");

  // Load danh sách chat từ backend
  const refresh = async (keepSelection = false) => {
    try {
      const list = await listChatsByUser();
      setChats(list);

      // Nếu chưa chọn chat thì chọn cái đầu tiên
      if (!keepSelection && !currentId && list.length > 0) {
        onSelect(list[0].id);
      }
    } catch (e) {
      console.error("Load chats error:", e);
      setChats([]);
    }
  };

  useEffect(() => {
    refresh(true);
    // Load indexes
    listIndexesFromAPI().then(setIndexes).catch(() => setIndexes([]));
  }, []);

  // Tạo chat mới
  const handleNew = async () => {
    try {
      const chat = await createChat();
      await refresh(true);
      onSelect(chat.id);
    } catch (e) {
      alert(e.message || "Tạo chat mới thất bại");
    }
  };

  // Xoá chat
  const handleDelete = async (id) => {
    if (!confirm("Bạn chắc chắn muốn xoá đoạn chat này?")) return;

    try {
      await deleteChat(id);

      const list = await listChatsByUser();
      setChats(list);

      // Nếu vừa xoá chat hiện tại → chọn cái tiếp theo
      if (id === currentId) {
        onSelect(list.length ? list[0].id : null);
      }
    } catch (e) {
      alert(e.message || "Xoá chat thất bại");
    }
  };

  // Lưu tên chat sau khi sửa
  const saveEdit = async (id) => {
    try {
      await renameChat(id, tempTitle || "Untitled");
      setEditingId(null);
      refresh(true);
    } catch (e) {
      alert(e.message || "Đổi tên thất bại");
    }
  };

  return (
    <div className="card sidebar" style={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <div style={{ flex: 7, overflowY: "auto", minHeight: 0 }}>
        <button className="new-chat" onClick={handleNew}>+ New chat</button>
        <h3>Chats</h3>
        <div>
          {chats.map(c => (
            <div
              key={c.id}
              className="chat-item"
              onClick={() => onSelect(c.id)}
              style={{
                borderColor: c.id === currentId ? "#4d66b3" : undefined,
                background: c.id === currentId ? "#60a4ad9a" : "transparent",
                transition: "0.15s"
              }}
            >
              <div style={{ display: "flex", flexDirection: "column", flex: 1 }}>
                {editingId === c.id ? (
                  <input
                    value={tempTitle}
                    autoFocus
                    onChange={e => setTempTitle(e.target.value)}
                    onBlur={() => saveEdit(c.id)}
                    onKeyDown={e => e.key === "Enter" && saveEdit(c.id)}
                  />
                ) : (
                  <span className="title">{c.title}</span>
                )}
                <span className="meta">
                  {c.created_at ? new Date(c.created_at).toLocaleString() : ""}
                </span>
              </div>
              <div style={{ display: "flex", gap: 4 }}>
                {editingId !== c.id && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setEditingId(c.id);
                      setTempTitle(c.title);
                    }}
                  >
                    ✎
                  </button>
                )}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDelete(c.id);
                  }}
                >
                  🗑
                </button>
              </div>
            </div>
          ))}
          {chats.length === 0 && (
            <div className="chat-item">
              <span className="title">Chưa có chat</span>
            </div>
          )}
        </div>
      </div>
      <div style={{ flex: 3, overflowY: "auto", minHeight: 0, borderTop: "1px solid #eee", padding: 8 }}>
        <h4>Chọn index</h4>
        {indexes.map(idx => (
          <label key={idx.id} style={{ display: "block", marginBottom: 4 }}>
            <input
              type="radio"
              name="index-radio"
              value={idx.name}
              checked={selectedIndex === idx.name}
              onChange={() => {
                setSelectedIndex(idx.name);
                onIndexSelect?.(idx.name);
              }}
            />
            {idx.name}
          </label>
        ))}
        {indexes.length === 0 && <div>Chưa có index</div>}
      </div>
    </div>
  );
}
