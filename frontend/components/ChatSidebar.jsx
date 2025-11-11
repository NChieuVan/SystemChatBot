export default function ChatSidebar() {
  return (
    <div className="sidebar">
      <button className="new-chat">+ New chat</button>
      <h3>Chat</h3>
      <div className="chat-list">
        <div className="chat-item">Chat medical 🗑</div>
        <div className="chat-item">Chat math 🗑</div>
      </div>

      <h3>Index</h3>
      <label><input type="checkbox" /> medical</label>
      <label><input type="checkbox" /> math</label>
    </div>
  );
}
