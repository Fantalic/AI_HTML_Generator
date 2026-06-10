export function fileSaver() {
  return {
    showModal: false,
    fileName: "index.html",

    saveFile(content) {
      if (!content) return;

      const blob = new Blob([content], { type: "text/html" });
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");

      anchor.href = url;
      anchor.download = this.fileName;
      document.body.appendChild(anchor);
      anchor.click();

      document.body.removeChild(anchor);
      URL.revokeObjectURL(url);
      this.showModal = false;
    },
  };
}
