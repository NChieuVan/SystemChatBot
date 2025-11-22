import { useEffect, useMemo, useState } from "react";
import { getChat, sendMessage, setModel, createChat } from "../services/chatMock";
import { listIndexesFromAPI } from "../services/pineconeMock";

const MODELS = [
  { id: "gpt-4o", label: "GPT-4o" },
  { id: "gemini-1.5", label: "Gemini 1.5" },
  { id: "meta-llama-3", label: "Llama 3" },
];

export default function ChatWindow({ chatId, onNeedChat }) {
  const [input, setInput] = useState("");
  const [chat, setChat] = useState(null);
  const [indexes, setIndexes] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState("");
  const model = chat?.model || MODELS[0].id;

  // Load chat không tạo chat mới, khi nào click new chat thì mới tạo
  useEffect(() => {
    const loadChat = async () => {
      if (!chatId) {
        setChat(null);
        return;
      }
      try {
        const data = await getChat(chatId);
        setChat(data);
      } catch (e) {
        console.error("Load chat error:", e);
        setChat(null);
      }
    };
    loadChat();
  }, [chatId]);

  useEffect(() => {
    listIndexesFromAPI().then(setIndexes).catch(() => setIndexes([]));
  }, []);

  const messages = useMemo(() => chat?.messages || [], [chat]);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || !chat || !selectedIndex) return;
    const updated = await sendMessage(chat.id, text, selectedIndex);
    setChat(updated);
    setInput("");
  };

  const changeModel = async (e) => {
    if (!chat) return;
    await setModel(chat.id, e.target.value);
    const data = await getChat(chat.id);
    setChat(data);
  };

  return (
    <div className="card chat-window">
      <div className="model-bar">
        <span className="badge">Model</span>
        <select value={model} onChange={changeModel} className="model-select">
          {MODELS.map(m => <option key={m.id} value={m.id}>{m.label}</option>)}
        </select>
        <span className="badge" style={{marginLeft:16}}>Index</span>
        <select value={selectedIndex} onChange={e=>setSelectedIndex(e.target.value)} className="model-select">
          <option value="">-- Chọn index --</option>
          {indexes.map(idx => <option key={idx.id} value={idx.name}>{idx.name}</option>)}
        </select>
      </div>

      <div className="messages">
        {messages.map((m,i)=>(
          <div key={i} className={"bubble " + (m.role==="user" ? "from-user" : "from-bot")}>{m.content}</div>
        ))}
        {messages.length===0 && (
          <div className="bubble from-bot">Chào bạn! Hãy nhập câu hỏi để bắt đầu.</div>
        )}
      </div>

      <div className="input-row">
        <input
          value={input}
          onChange={(e)=>setInput(e.target.value)}
          placeholder="Nhập tin nhắn..."
          onKeyDown={(e)=>e.key==="Enter" && handleSend()}
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}
