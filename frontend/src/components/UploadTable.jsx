import { useEffect, useMemo, useState } from "react";
import Toast from "./Toast";
import WaveText from "./WaveText";
import { 
  listIndexesFromAPI, 
  createIndex, 
  deleteIndexFromAPI, 
  upsertFile, 
  deleteFile,
  listFileInIndex 
} from "../services/pineconeMock";

export default function UploadTable() {
  const [indexes, setIndexes] = useState([]);
  const [selected, setSelected] = useState("");
  const [newIdx, setNewIdx] = useState({ name: "", dim: 356 });
  const [file, setFile] = useState(null);

  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [embedding, setEmbedding] = useState(false);

  const [message, setMessage] = useState("");
  const [toastType, setToastType] = useState("success");

  const [creating, setCreating] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const [selectedFile, setSelectedFile] = useState(null);

  // ----------------------------
  // Load Indexes
  // ----------------------------
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

  useEffect(() => { 
    refresh(); 
  }, []);

  // -----------------------------------------------------
  // Load Files when selected index changes
  // -----------------------------------------------------
  useEffect(() => {
    if (!selected) {
      setSelectedFile(null);
      return;
    }

    async function loadFiles() {
      try {
        const backendFiles = await listFileInIndex(selected);

        setIndexes(prev =>
          prev.map(ix =>
            ix.name === selected
              ? { ...ix, files: backendFiles }
              : ix
          )
        );

        setSelectedFile(null);   // reset file selection when index changes

      } catch (err) {
        console.error("Load file error:", err);
      }
    }

    loadFiles();
  }, [selected]);

  const current = useMemo(() => {
    return indexes.find(ix => ix.name === selected) || null;
  }, [selected, indexes]);

  // ----------------------------
  // Create Index
  // ----------------------------
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

    } catch (e) {
      setToastType("error");
      setMessage(e.message);
    } finally {
      setCreating(false);
    }
  };

  // ----------------------------
  // Delete Index
  // ----------------------------
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

    } catch (e) {
      setToastType("error");
      setMessage(e.message);
    } finally {
      setDeleting(false);
    }
  };

  // ----------------------------
  // Upload File
  // ----------------------------
  const handleUpload = async () => {
    if (!selected) {
      setToastType("warning");
      setMessage("Chọn index trước");
      return;
    }
    if (!file) {
      setToastType("warning");
      setMessage("Chưa chọn file để upload");
      return;
    }

    setUploading(true);
    try {
      await upsertFile(selected, file);
      setToastType("success");
      setMessage("Upload file thành công!");
      setFile(null);

      const backendFiles = await listFileInIndex(selected);

      setIndexes(prev =>
        prev.map(ix =>
          ix.name === selected
            ? { ...ix, files: backendFiles }
            : ix
        )
      );

    } catch (e) {
      setToastType("error");
      setMessage(e.message || "Upload thất bại");
    } finally {
      setUploading(false);
    }
  };

  // ----------------------------
  // Embedding file (only selected row)
  // ----------------------------
  const handeEmbedding = async () => {
    if (!selected) {
      setToastType("warning");
      setMessage("Chọn index trước");
      return;
    }

    if (!selectedFile) {
      setToastType("warning");
      setMessage("Bạn phải chọn một file trong bảng để nhúng");
      return;
    }

    setEmbedding(true);
    try {
      // TODO: Replace with real API
      await upsertFile(selected, selectedFile);

      setToastType("success");
      setMessage(`Nhúng dữ liệu file "${selectedFile.filename}" thành công!`);

    } catch (e) {
      setToastType("error");
      setMessage(e.message || "Nhúng thất bại");
    } finally {
      setEmbedding(false);
    }
  };

  // ----------------------------
  // Delete File
  // ----------------------------
  const handleDeleteFile = async (id) => {
    if (!selected) return;

    try {
      await deleteFile(selected, id);
      setToastType("success");
      setMessage("Xoá file thành công!");

    } catch (e) {
      setToastType("error");
      setMessage(e.message || "Xoá file thất bại");
    }

    const backendFiles = await listFileInIndex(selected);

    setIndexes(prev =>
      prev.map(ix =>
        ix.name === selected
          ? { ...ix, files: backendFiles }
          : ix
      )
    );

    setSelectedFile(null);
  };

  // ======================================================================
  // RENDER UI
  // ======================================================================
  return (
    <div className="db-grid">
      <Toast message={message} type={toastType} onClose={() => setMessage("")} />

      {/* INDEX MANAGER */}
      <div className="card section">
        <h3>Quản lý Index</h3>

        <div className="row">
          <input placeholder="Tên index" 
            value={newIdx.name} 
            onChange={e => setNewIdx({ ...newIdx, name: e.target.value })} />

          <input type="number" placeholder="Dimension"
            value={newIdx.dim}
            onChange={e => setNewIdx({ ...newIdx, dim: e.target.value })} />

          <button className="primary" onClick={handleCreate} disabled={loading || creating}>
            {creating ? <WaveText text="Đang tạo..." /> : "Tạo index"}
          </button>
        </div>

        <div className="row">
          <select className="index-select" value={selected} onChange={e => setSelected(e.target.value)}>
            <option value="">-- Chọn index --</option>
            {indexes.map(ix => (
              <option key={ix.id || ix.name} value={ix.name}>{ix.name}</option>
            ))}
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
            {!loading && indexes.length === 0 && (
              <tr><td colSpan="3">Chưa có index</td></tr>
            )}
          </tbody>
        </table>
      </div>

      {/* FILE MANAGER */}
      <div className="card section">
        <h3>Dữ liệu trong Index <span style={{ color: 'green' }}>"{selected}"</span></h3>

        <div className="row">
          <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />

          <button onClick={handleUpload} className="primary"  disabled={uploading}>
            {uploading ? <WaveText text="Đang upload..." /> : "Thêm vào index"}
          </button>

          <button 
            onClick={handeEmbedding} 
            className={`embed-btn ${selectedFile ? "active" : "inactive"}`}
            disabled={!selectedFile || embedding}
          >
            {embedding ? <WaveText text="Đang nhúng..." /> : "Nhúng dữ liệu"}
          </button>
        </div>

        <table className="table">
          <thead>
            <tr>
              <th>File</th>
              <th>Kích thước</th>
              <th>Thời gian</th>
              <th>Trạng thái</th>
              <th>Hành động</th>
            </tr>
          </thead>

          <tbody>
            {current?.files?.map(f => {
              const fid = f.file_id || f.id;

              return (
                <tr
                  key={fid}
                  onClick={() => setSelectedFile(f)}
                  style={{
                    cursor: "pointer",
                    background:
                      selectedFile &&
                      (selectedFile.file_id || selectedFile.id) === fid
                        ? "#3999b9a6"
                        : "transparent"
                  }}
                >
                  <td>{f.filename || f.name}</td>
                  <td>{((f.size_bytes || f.size || 0) / 1024).toFixed(1)} KB</td>
                  <td>{new Date(f.uploaded_at || f.uploadedAt).toLocaleString()}</td>
                  <td>{f.status}</td>

                  <td>
                    <button
                      className="btn-delete"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDeleteFile(fid);
                      }}
                    >
                      🗑️ Xoá
                    </button>
                  </td>
                </tr>
              );
            })}

            {(!current || !current.files || current.files.length === 0) && (
              <tr><td colSpan="5">Chưa có file trong index đã chọn</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
