
/**
 * Mock chat service using localStorage
 * Schema:
 * chats: [{id, title, model, messages: [{role, content, ts}], createdAt}]
 */
const KEY = "demo_chats_v1";

function load() {
  try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; }
}
function save(chats) {
  localStorage.setItem(KEY, JSON.stringify(chats));
}
export function listChats() {
  return load().sort((a,b)=>b.createdAt-a.createdAt);
}
export function createChat(model="gpt-4o") {
  const chats = load();
  const id = crypto.randomUUID();
  const c = { id, title: "New chat", model, messages: [], createdAt: Date.now() };
  chats.push(c); save(chats); return c;
}
export function deleteChat(id) {
  save(load().filter(c=>c.id!==id));
}
export function getChat(id) {
  return load().find(c=>c.id===id) || null;
}
export function renameChat(id, title) {
  const chats = load();
  const i = chats.findIndex(c=>c.id===id);
  if (i>-1) { chats[i].title = title; save(chats); }
}
export async function sendMessage(id, role, content) {
  const chats = load();
  const i = chats.findIndex(c=>c.id===id);
  if (i===-1) throw new Error("Chat not found");
  const msg = { role, content, ts: Date.now() };
  chats[i].messages.push(msg);
  // Mock AI response
  if (role === "user") {
    const reply = {
      role: "assistant",
      content: `(${chats[i].model}) Demo trả lời: “${content}”`,
      ts: Date.now()+1
    };
    chats[i].messages.push(reply);
  }
  save(chats);
  return getChat(id);
}
export function setModel(id, model) {
  const chats = load();
  const i = chats.findIndex(c=>c.id===id);
  if (i>-1) { chats[i].model = model; save(chats); }
}
