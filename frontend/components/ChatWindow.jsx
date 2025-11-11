export default function ChatWindow() {
  return (
    <div className="chat-window">
      <div className="message bot">How can I help you?</div>
      <div className="message user">Hello</div>
      <input placeholder="Type your message..." className="chat-input" />
      <button className="send-btn">Send</button>
    </div>
  );
}
