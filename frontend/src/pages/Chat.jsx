import ChatSidebar from "../components/ChatSidebar";
import ChatWindow from "../components/ChatWindow";

export default function Chat() {
  return (
    <div className="chat-container">
      <ChatSidebar />
      <ChatWindow />
    </div>
  );
}
