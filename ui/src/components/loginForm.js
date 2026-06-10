import { login } from "../services/api.js";

export function loginForm() {
  return {
    email: "test@test.de",
    password: "test",
    error: "",

    async handleLogin() {
      this.error = "";

      try {
        await login(this.email, this.password);
        this.$store.app.authenticated = true;
      } catch (err) {
        this.error = "Invalid credentials";
      }
    },
  };
}
