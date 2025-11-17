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


export function deleteIndex(name) {
  save(load().filter(x=>x.name!==name));
}

// 
export function getIndex(name) {
  return load().find(x=>x.name===name) || null;
}

export function upsertFile(indexName, file) {
  const idxs = load();
  const i = idxs.findIndex(x=>x.name===indexName);
  if (i===-1) throw new Error("Index không tồn tại");
  const id = crypto.randomUUID();
  const size = file?.size || Math.floor(Math.random()*2_000_000)+50_000;
  idxs[i].files.push({ id, name: file?.name || "demo.txt", size, uploadedAt: Date.now() });
  save(idxs);
  return getIndex(indexName);
}

export function deleteFile(indexName, fileId) {
  const idxs = load();
  const i = idxs.findIndex(x=>x.name===indexName);
  if (i===-1) throw new Error("Index không tồn tại");
  idxs[i].files = idxs[i].files.filter(f=>f.id!==fileId);
  save(idxs);
  return getIndex(indexName);
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
