
import UploadTable from "../components/UploadTable";

export default function Database() {
  return (
    <div className="page">
      <div className="card section">
        <h3>Tổng quan Database Vector (Pinecone - Demo)</h3>
        <div className="row">
          <span className="badge">Tạo/Xoá index</span>
          <span className="badge">Thêm/Xoá file trong index được chọn</span>
          <span className="badge">Dữ liệu demo lưu trong localStorage</span>
        </div>
      </div>
      <UploadTable />
    </div>
  );
}
