import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import UploadBox from "@/components/upload/UploadBox";

declare const global: any;

class MockXHR {
  upload: any = {};
  readyState = 0;
  status = 0;
  responseText = "";
  onreadystatechange: any;
  onerror: any;
  onabort: any;
  open() {}
  send() {
    setTimeout(() => {
      this.upload.onprogress &&
        this.upload.onprogress({ lengthComputable: true, loaded: 5, total: 5 });
      this.readyState = 4;
      this.status = 200;
      this.responseText = JSON.stringify({
        ok: true,
        results: [{ file: "a.txt", status: "uploaded", doc_id: "1" }],
      });
      this.onreadystatechange && this.onreadystatechange();
    }, 0);
  }
  abort() {
    this.onabort && this.onabort();
  }
}

global.XMLHttpRequest = MockXHR as any;

test("handles drag drop upload", async () => {
  render(<UploadBox />);
  const dropZone = screen.getByText(/Dateien hier ablegen/);
  const file = new File(["hello"], "a.txt", { type: "text/plain" });
  fireEvent.drop(dropZone, { dataTransfer: { files: [file] } });
  expect(await screen.findByText("a.txt")).toBeInTheDocument();
  await waitFor(() => expect(screen.getByText("Zum Dokument")).toBeInTheDocument());
});
