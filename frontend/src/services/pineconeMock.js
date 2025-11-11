
/**
 * Mock Pinecone-like service
 * Schema in localStorage:
 * indexes: [{name, dimension, files: [{id, name, size, uploadedAt}], createdAt}]
 */
const KEY = "demo_indexes_v1";

function load() {
  try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; }
}
function save(idxs) { localStorage.setItem(KEY, JSON.stringify(idxs)); }

export function listIndexes() { return load().sort((a,b)=>a.name.localeCompare(b.name)); }

export function createIndex(name, dimension=1536) {
  const idxs = load();
  if (idxs.find(x=>x.name===name)) throw new Error("Index đã tồn tại");
  const obj = { name, dimension, files: [], createdAt: Date.now() };
  idxs.push(obj); save(idxs); return obj;
}

export function deleteIndex(name) {
  save(load().filter(x=>x.name!==name));
}

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
