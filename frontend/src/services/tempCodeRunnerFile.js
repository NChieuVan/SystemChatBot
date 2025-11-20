/**
 * Chat service sử dụng backend 100%
 */
const API_BASE =
  typeof import.meta !== "undefined" &&
  import.meta.env &&
  import.meta.env.VITE_API_URL
    ? import.meta.env.VITE_API_URL
    : "http://localhost:8000";

function buildUrl(path) {
  return `${API_BASE.replace(/\/$/, "")}${path}`;
}

import { getToken } from "./authService";

// Lấy danh sách chat theo user
export async function listChatsByUser() {
  const token = getToken();
  const res = await fetch(buildUrl("/api/chats/"), {
    method: "GET",
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!res.ok) {
    let err = await res.json().catch(() => ({}));
    throw new Error(err.detail || res.statusText);
  }

  return await res.json();
}

// Tạo chat mới
export async function createChat(model = "gpt-4o") {
  const token = getToken();
  const res = await fetch(buildUrl("/api/chats/"), {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ model }).toString(),
  });

  if (!res.ok) {
    let err = await res.json().catch(() => ({}));
    throw new Error(err.detail || res.statusText);
  }

  return await res.json();
}

// Xoá chat
export async function deleteChat(id) {
  const token = getToken();
  const res = await fetch(buildUrl(`/api/chats/${encodeURIComponent(id)}`), {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!res.ok) {
    let err = await res.json().catch(() => ({}));
    throw new Error(err.detail || res.statusText);
  }
}

// Đổi tên chat - backend
export async function renameChat(id, title) {
  const token = getToken();
  const res = await fetch(buildUrl(`/api/chats/${id}/rename`), {
    method: "PUT",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ title }).toString(),
  });

  if (!res.ok) {
    let err = await res.json().catch(() => ({}));
    throw new Error(err.detail || res.statusText);
  }

  return await res.json();
}

// Lấy chi tiết chat
export async function getChat(id) {
  const token = getToken();
  const res = await fetch(buildUrl(`/api/chats/${id}`), {
    method: "GET",
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!res.ok) throw new Error("Không tìm thấy chat");

  return await res.json();
}
