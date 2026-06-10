import Alpine from "alpinejs";
import { htmlEditor } from "./components/htmlEditor.js";
import { loginForm } from "./components/loginForm.js";
import { fileSaver } from "./components/fileSaver.js";

Alpine.store("app", {
  authenticated: false,
  htmlContent: '<div class="rounded-lg p-8 text-center">Your Generated HTML Here</div>',
});

Alpine.data("htmlEditor", htmlEditor);
Alpine.data("loginForm", loginForm);
Alpine.data("fileSaver", fileSaver);

Alpine.start();
