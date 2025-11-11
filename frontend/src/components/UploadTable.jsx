
import { useEffect, useMemo, useState } from "react";
import { listIndexes, createIndex, deleteIndex, getIndex, upsertFile, deleteFile } from "../services/pineconeMock";

export default function UploadTable() {
  const [indexes, setIndexes] = useState([]);
  const [selected, setSelected] = useState("");
  const [newIdx, setNewIdx] = useState({ name: "", dim: 1536 });
  const [file, setFile] = useState(null);

  const refresh = () => setIndexes(listIndexes());
  useEffect(()=>{ refresh(); }, []);

  const current = useMemo(()=> getIndex(selected), [selected, indexes]);

  const handleCreate = () => {
    if (!newIdx.name.trim()) return alert("Nhập tên index");
    try {
      createIndex(newIdx.name.trim(), Number(newIdx.dim) || 1536);
      setNewIdx({ name: "", dim: 1536 });
      refresh();
      setSelected(newIdx.name.trim());
    } catch(e) {
      alert(e.message);
    }
  };

  const handleDeleteIndex = () => {
    if (!selected) return;
    if (!confirm(`Xoá index "${selected}"?`)) return;
    deleteIndex(selected);
    setSelected("");
    refresh();
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
      <div className="card section">
        <h3>Quản lý Index</h3>
        <div className="row">
          <input placeholder="Tên index" value={newIdx.name} onChange={e=>setNewIdx({...newIdx, name: e.target.value})} />
          <input type="number" placeholder="Dimension" value={newIdx.dim} onChange={e=>setNewIdx({...newIdx, dim: e.target.value})} />
          <button className="primary" onClick={handleCreate}>Tạo index</button>
        </div>

        <div className="row">
          <select className="index-select" value={selected} onChange={e=>setSelected(e.target.value)}>
            <option value="">-- Chọn index --</option>
            {indexes.map(ix => <option key={ix.name} value={ix.name}>{ix.name} (dim {ix.dimension})</option>)}
          </select>
          <button className="danger" onClick={handleDeleteIndex} disabled={!selected}>Xoá index</button>
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
            {indexes.map(ix => (
              <tr key={ix.name}>
                <td><span className="badge">{ix.name}</span></td>
                <td>{ix.dimension}</td>
                <td>{new Date(ix.createdAt).toLocaleString()}</td>
              </tr>
            ))}
            {indexes.length===0 && <tr><td colSpan="3">Chưa có index</td></tr>}
          </tbody>
        </table>
      </div>

      <div className="card section">
        <h3>Dữ liệu trong Index</h3>
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
                <td>{f.name}</td>
                <td>{(f.size/1024).toFixed(1)} KB</td>
                <td>{new Date(f.uploadedAt).toLocaleString()}</td>
                <td><button className="danger" onClick={()=>handleDeleteFile(f.id)}>Xoá</button></td>
              </tr>
            ))}
            {(!current || current.files.length===0) && <tr><td colSpan="4">Chưa có file trong index đã chọn</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
}
