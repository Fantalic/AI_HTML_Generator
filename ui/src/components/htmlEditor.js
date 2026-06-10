import { generateHtml } from "../services/api.js";

export function htmlEditor() {
  return {
    prompt: "",
    loading: false,

    init() {
      document.addEventListener("click", (event) => {
        const container = document.getElementById("container");
        if (!container || container.contains(event.target)) return;

        const editable = container.querySelectorAll("[contenteditable='true']");
        editable.forEach((el) => el.removeAttribute("contenteditable"));
      });
    },

    async handleSubmit() {
      if (!this.prompt) return;

      const oldHtml = this.$store.app.htmlContent;
      this.loading = true;

      try {
        const html = await generateHtml(this.prompt, oldHtml);
        this.$store.app.htmlContent = html;
      } catch (error) {
        console.error("Error generating HTML:", error);
        this.$store.app.htmlContent =
          '<p class="text-red-500">Error generating HTML. Please try again.</p>';
      } finally {
        this.loading = false;
      }
    },

    editHTML(event) {
      const container = document.getElementById("container");
      const target = event.target;

      if (target !== container && container.contains(target)) {
        target.setAttribute("contenteditable", "true");
        target.focus();

        target.addEventListener(
          "blur",
          () => {
            this.$store.app.htmlContent = document.getElementById("container").innerHTML;
          },
          { once: true }
        );
      }
    },

    editCode(event) {
      const el = event.target;
      el.contentEditable =
        el.contentEditable === "true" ? "false" : "true";
      el.focus();
    },
  };
}
