// services/auth.js
import axios from "axios";

export async function login(email, password) {
  const res = await axios.post("http://127.0.0.1:5000/login", {
    email,
    password,
  });
  const token = res.data.access_token;
  localStorage.setItem("token", token);
  return token;
}
