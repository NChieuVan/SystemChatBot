export default function UploadTable() {
  return (
    <div className="upload-section">
      <h3>Create Index</h3>
      <input type="text" placeholder="name index" />
      <input type="file" />
      <button>Upload</button>

      <h3>List index</h3>
      <label><input type="checkbox" /> medical 🗑</label>
      <label><input type="checkbox" /> math 🗑</label>

      <table>
        <thead>
          <tr>
            <th>File Name</th>
            <th>Uploaded On</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>example.pdf</td><td>Feb 1, 2024</td><td>🗑</td></tr>
          <tr><td>example.png</td><td>Feb 1, 2024</td><td>🗑</td></tr>
        </tbody>
      </table>
    </div>
  );
}
