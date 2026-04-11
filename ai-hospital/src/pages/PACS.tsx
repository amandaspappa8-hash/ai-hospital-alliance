export default function PACS() {
  return (
    <div style={{ height: "100vh" }}>
      <h1>PACS Viewer</h1>
      <iframe
        src="http://localhost:3005"
        style={{ width: "100%", height: "90%", border: "none" }}
        title="OHIF Viewer"
      />
    </div>
  );
}
