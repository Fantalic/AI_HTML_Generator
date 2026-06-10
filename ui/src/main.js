import Alpine from "alpinejs";
import { htmlEditor } from "./components/htmlEditor.js";
import { loginForm } from "./components/loginForm.js";
import { fileSaver } from "./components/fileSaver.js";

Alpine.data("htmlEditor", htmlEditor);
Alpine.data("loginForm", loginForm);
Alpine.data("fileSaver", fileSaver);

Alpine.start();
