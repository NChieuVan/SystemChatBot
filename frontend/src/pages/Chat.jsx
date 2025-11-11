
import { useEffect, useState } from "react";
import ChatSidebar from "../components/ChatSidebar";
import ChatWindow from "../components/ChatWindow";

export default function Chat() {
  const [currentChatId, setCurrentChatId] = useState(null);

  useEffect(()=>{
    // Ensure a chat is selected in ChatWindow if none
  }, []);

  return (
    <div className="page">
      <div className="grid">
        <ChatSidebar currentId={currentChatId} onSelect={setCurrentChatId} />
        <ChatWindow chatId={currentChatId} onNeedChat={setCurrentChatId} />
      </div>
    </div>
  );
}
