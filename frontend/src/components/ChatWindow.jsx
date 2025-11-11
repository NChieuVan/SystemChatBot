
import { useEffect, useMemo, useState } from "react";
import { getChat, sendMessage, setModel, createChat } from "../services/chatMock";

const MODELS = [
  { id: "gpt-4o", label: "GPT-4o" },
  { id: "gemini-1.5", label: "Gemini 1.5" },
  { id: "meta-llama-3", label: "Llama 3" },
];

export default function ChatWindow({ chatId, onNeedChat }) {
  const [input, setInput] = useState("");
  const [chat, setChat] = useState(null);
  const model = chat?.model || MODELS[0].id;

  useEffect(()=>{
    if (chatId) {
      setChat(getChat(chatId));
    } else {
      const c = createChat(MODELS[0].id);
      onNeedChat?.(c.id);
      setChat(c);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [chatId]);

  const messages = useMemo(()=> chat?.messages || [], [chat]);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || !chat) return;
    const updated = await sendMessage(chat.id, "user", text);
    setChat(updated);
    setInput("");
  };

  const changeModel = (e) => {
    if (!chat) return;
    setModel(chat.id, e.target.value);
    setChat(getChat(chat.id));
  };

  return (
    <div className="card chat-window">
      <div className="model-bar">
        <span className="badge">Model</span>
        <select value={model} onChange={changeModel} className="model-select">
          {MODELS.map(m => <option key={m.id} value={m.id}>{m.label}</option>)}
        </select>
      </div>

      <div className="messages">
        {messages.map((m,i)=>(
          <div key={i} className={"bubble " + (m.role==="user" ? "from-user" : "from-bot")}>
            {m.content}
          </div>
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
