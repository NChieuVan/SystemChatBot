
import { useEffect, useState } from "react";
import { listChats, createChat, deleteChat, renameChat } from "../services/chatMock";

export default function ChatSidebar({ currentId, onSelect }) {
  const [chats, setChats] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [tempTitle, setTempTitle] = useState("");

  const refresh = () => setChats(listChats());
  useEffect(()=>{ refresh(); }, []);

  const handleNew = () => {
    const c = createChat();
    refresh();
    onSelect?.(c.id);
  };
  const handleDelete = (id) => {
    if (!confirm("Xoá đoạn chat này?")) return;
    deleteChat(id); refresh();
    if (id===currentId && chats.length>0) onSelect?.(chats[0]?.id);
  };
  const startEdit = (c) => { setEditingId(c.id); setTempTitle(c.title); };
  const saveEdit = (id) => { renameChat(id, tempTitle || "Untitled"); setEditingId(null); refresh(); };

  return (
    <div className="card sidebar">
      <button className="new-chat" onClick={handleNew}>+ New chat</button>
      <h3>Chats</h3>
      <div>
        {chats.map(c => (
          <div key={c.id} className="chat-item" onClick={()=>onSelect?.(c.id)} style={{borderColor: c.id===currentId ? "#4d66b3" : undefined}}>
            <div style={{display:"flex", flexDirection:"column"}}>
              {editingId===c.id ? (
                <input value={tempTitle} onChange={e=>setTempTitle(e.target.value)} onBlur={()=>saveEdit(c.id)} onKeyDown={e=>e.key==="Enter"&&saveEdit(c.id)} />
              ) : (
                <span className="title">{c.title}</span>
              )}
              <span className="meta">{new Date(c.createdAt).toLocaleString()}</span>
            </div>
            <div>
              {editingId!==c.id && <button onClick={(e)=>{e.stopPropagation(); startEdit(c);}}>✎</button>}
              <button onClick={(e)=>{e.stopPropagation(); handleDelete(c.id);}}>🗑</button>
            </div>
          </div>
        ))}
        {chats.length===0 && <div className="chat-item"><span className="title">Chưa có chat</span></div>}
      </div>
    </div>
  );
}
