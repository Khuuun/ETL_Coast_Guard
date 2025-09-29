<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-lg p-8">
      <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Login</h2>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <!-- Email -->
        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="you@example.com"
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none"
            required
          />
        </div>

        <!-- Password -->
        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">Password</label>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none"
            required
          />
        </div>

        <!-- Error message -->
        <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>

        <!-- Submit Button -->
        <button
          type="submit"
          class="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 rounded-lg font-semibold transition"
        >
          Login
        </button>
      </form>

      <!-- Extra Links -->
      <p class="text-sm text-center text-gray-500 mt-4">
        Don’t have an account?
        <a href="#" class="text-blue-500 hover:underline">Register</a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const email = ref("");
const password = ref("");
const error = ref("");

async function handleLogin() {
  if (!email.value || !password.value) {
    error.value = "Please fill in all fields.";
    return;
  }
  error.value = "";

  try {
    const res = await fetch("http://127.0.0.1:5000/api/users/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email.value, password: password.value }),
    });

    const data = await res.json();

    if (res.ok && data.access_token) {
      // ✅ Save token to localStorage
      localStorage.setItem("token", data.access_token);

      // ✅ You can also store user info if you want
      localStorage.setItem("user", JSON.stringify(data.user));

      // ✅ Redirect to dashboard
      window.location.replace("/dashboard");
    } else {
      error.value = data.error || "Invalid email or password";
    }
  } catch (err) {
    error.value = "Error connecting to server.";
    console.error(err);
  }
}
</script>

