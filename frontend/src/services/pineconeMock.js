/**
 * Mock Pinecone-like service
 * Schema in localStorage:
 * indexes: [{name, dimension, files: [{id, name, size, uploadedAt}], createdAt}]
 */
import { getToken } from "./authService";

const API_BASE = typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_URL
  ? import.meta.env.VITE_API_URL
  : 'http://localhost:8000';

function buildUrl(path) {
  if (!API_BASE) return path;
  return `${API_BASE.replace(/\/$/, '')}${path}`;
}

const KEY = "demo_indexes_v1";

function load() {
  try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; }
}
function save(idxs) { localStorage.setItem(KEY, JSON.stringify(idxs)); }

export function listIndexes() { return load().sort((a,b)=>a.name.localeCompare(b.name)); }


// Create Index with user dependency token
export async function createIndex(name, dimension = 1536) {
  const token = getToken();
  if (!token) throw new Error("Bạn chưa đăng nhập.");
  const res = await fetch(buildUrl("/api/indexes/"), {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "Authorization": `Bearer ${token}`
    },
    body: new URLSearchParams({ name, dimension }).toString()
  });
  if (!res.ok) {
    let err = await res.json().catch(() => ({}));
    throw new Error(err.detail || res.statusText);
  }
  return res.json();
}


// Xóa index đã chọn qua backend
export async function deleteIndexFromAPI(name) {
  const token = getToken();
  if (!token) throw new Error("Bạn chưa đăng nhập.");
  const res = await fetch(buildUrl(`/api/indexes/${encodeURIComponent(name)}`), {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${token}`
    },
  });
  if (!res.ok) {
    let err = await res.json().catch(() => ({}));
    throw new Error(err.detail || res.statusText);
  }
  return res.json();
}
// 
export function getIndex(name) {
  return load().find(x=>x.name===name) || null;
}

export async function upsertFile(indexName, file) {
  const token = getToken();
  if (!token) throw new Error("Bạn chưa đăng nhập.");
    const formData = new FormData();
    formData.append("index_name", indexName);
    formData.append("file", file);
    const res = await fetch(buildUrl(`/api/upload/`), {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`
    },
    body: formData
  });
  if (!res.ok) {
    let err = await res.json().catch(() => ({}));
    throw new Error(err.detail || res.statusText);
  }
  return res.json();
}


export async function deleteFile(indexName, fileId) {
  const token = getToken();
  if (!token) throw new Error("Bạn chưa đăng nhập.");
  const res = await fetch(buildUrl(`/api/fileindex/${encodeURIComponent(indexName)}/files/${encodeURIComponent(fileId)}`), {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${token}`
    },
  });
  if (!res.ok) {
    let err = await res.json().catch(() => ({}));
    throw new Error(err.detail || res.statusText);
  }
  return res.json();
}

// Lấy toàn bộ index của user hiện tại từ backend
export async function listIndexesFromAPI() {
  const token = getToken();
  if (!token) throw new Error("Bạn chưa đăng nhập.");
  const res = await fetch(buildUrl("/api/indexes/"), {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`
    },
  });
  if (!res.ok) {
    let err = await res.json().catch(() => ({}));
    throw new Error(err.detail || res.statusText);
  }
  return res.json();
}

export async function listFileInIndex(index_name) {
  const token = getToken();
  if (!token) throw new Error("Bạn chưa đăng nhập.");
  const res = await fetch(buildUrl(`/api/fileindex/${encodeURIComponent(index_name)}/files`), {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`
    },
  });
  if (!res.ok) {
    let err = await res.json().catch(() => ({}));
    throw new Error(err.detail || res.statusText);
  }
  return res.json();
}


