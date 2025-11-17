import { useEffect, useMemo, useState } from "react";
import Toast from "./Toast";
import WaveText from "./WaveText";
import { listIndexesFromAPI, createIndex, deleteIndexFromAPI, getIndex, upsertFile, deleteFile } from "../services/pineconeMock";

export default function UploadTable() {
  const [indexes, setIndexes] = useState([]);
  const [selected, setSelected] = useState("");
  const [newIdx, setNewIdx] = useState({ name: "", dim: 356 });
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [toastType, setToastType] = useState("success");
  const [creating, setCreating] = useState(false);
  const [deleting, setDeleting] = useState(false);

  // Load indexes từ backend
  const refresh = async () => {
    setLoading(true);
    try {
      const idxs = await listIndexesFromAPI();
      setIndexes(idxs);
    } catch (e) {
      setIndexes([]);
      alert(e.message || "Không tải được danh sách index");
    } finally {
      setLoading(false);
    }
  };
  useEffect(()=>{ refresh(); }, []);

  const current = useMemo(()=> indexes.find(ix => ix.name === selected) || null, [selected, indexes]);

  const handleCreate = async () => {
    if (!newIdx.name.trim()) return alert("Nhập tên index");
    setCreating(true);
    try {
      const created = await createIndex(newIdx.name.trim(), Number(newIdx.dim) || 356);
      setNewIdx({ name: "", dim: 356 });
      setToastType("success");
      setMessage(`Tạo index "${created.name}" thành công!`);
      await refresh();
      setSelected(created.name);
    } catch(e) {
      setToastType("error");
      setMessage(e.message);
    } finally {
      setCreating(false);
    }
  };

  const handleDeleteIndex = async () => {
    if (!selected) return;
    if (!confirm(`Xoá index "${selected}"?`)) return;
    setDeleting(true);
    try {
      await deleteIndexFromAPI(selected);
      setToastType("success");
      setMessage(`Đã xoá index "${selected}" thành công!`);
      setSelected("");
      await refresh();
    } catch(e) {
      setToastType("error");
      setMessage(e.message);
    } finally {
      setDeleting(false);
    }
  };

  const handleUpload = () => {
    if (!selected) return alert("Chọn index trước");
    upsertFile(selected, file || { name: "demo.txt" });
    setFile(null);
    refresh();
  };

  const handleDeleteFile = (id) => {
    if (!selected) return;
    deleteFile(selected, id);
    refresh();
  };

  return (
    <div className="db-grid">
      <Toast message={message} type={toastType} onClose={()=>setMessage("")} />
      <div className="card section">
        <h3>Quản lý Index</h3>
        <div className="row">
          <input placeholder="Tên index" value={newIdx.name} onChange={e=>setNewIdx({...newIdx, name: e.target.value})} />
          <input type="number" placeholder="Dimension" value={newIdx.dim} onChange={e=>setNewIdx({...newIdx, dim: e.target.value})} />
          <button className="primary" onClick={handleCreate} disabled={loading || creating}>
            {creating ? <WaveText text="Đang tạo..." /> : "Tạo index"}
          </button>
        </div>

        <div className="row">
          <select className="index-select" value={selected} onChange={e=>setSelected(e.target.value)}>
            <option value="">-- Chọn index --</option>
            {indexes.map(ix => <option key={ix.id || ix.name} value={ix.name}>{ix.name}</option>)}
          </select>
          <button className="danger" onClick={handleDeleteIndex} disabled={!selected || loading || deleting}>
            {deleting ? <WaveText text="Đang xoá..." /> : "Xoá index"}
          </button>
        </div>

        <table className="table">
          <thead>
            <tr>
              <th>Tên index</th>
              <th>Dimension</th>
              <th>Tạo lúc</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan="3">Đang tải...</td></tr>
            ) : indexes.map(ix => (
              <tr key={ix.id || ix.name}>
                <td><span className="badge">{ix.name}</span></td>
                <td>{ix.dimension}</td>
                <td>{new Date(ix.created_at || ix.createdAt).toLocaleString()}</td>
              </tr>
            ))}
            {!loading && indexes.length===0 && <tr><td colSpan="3">Chưa có index</td></tr>}
          </tbody>
        </table>
      </div>

      <div className="card section">
        <h3>Dữ liệu trong Index <span style={{ color: 'green' }}>&quot;{selected}&quot;</span></h3>
        <div className="row">
          <input type="file" onChange={(e)=>setFile(e.target.files?.[0] || null)} />
          <button onClick={handleUpload} className="primary">Thêm vào index</button>
        </div>

        <table className="table">
          <thead>
            <tr>
              <th>File</th>
              <th>Kích thước</th>
              <th>Thời gian</th>
              <th>Hành động</th>
            </tr>
          </thead>
          <tbody>
            {current?.files?.map(f => (
              <tr key={f.id}>
                <td>{f.name || f.filename}</td>
                <td>{((f.size || f.size_bytes || 0)/1024).toFixed(1)} KB</td>
                <td>{new Date(f.uploadedAt || f.uploaded_at).toLocaleString()}</td>
                <td><button className="danger" onClick={()=>handleDeleteFile(f.id)}>Xoá</button></td>
              </tr>
            ))}
            {(!current || !current.files || current.files.length===0) && <tr><td colSpan="4">Chưa có file trong index đã chọn</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
}
