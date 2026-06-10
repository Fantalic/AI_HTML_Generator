import { login } from "../services/api.js";

export function loginForm() {
  return {
    email: "",
    password: "",
    error: "",

    async handleLogin() {
      this.error = "";

      try {
        const response = await login(this.email, this.password);

        if (response.status === 302) {
          window.location.href = "/";
        } else {
          this.error = "Invalid credentials";
        }
      } catch (err) {
        this.error = "Login failed. Please try again.";
      }
    },
  };
}
