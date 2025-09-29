import { createRouter, createWebHistory } from "vue-router";
import Login from "../components/Login.vue";
import Dashboard from "../Pages/Dashboard.vue";
import Upload from "../Pages/UploadFile.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: Login },
  {
    path: "/dashboard",
    component: Dashboard,
    meta: { requiresAuth: true }, // ✅ Protected route
  },
  {
    path: "/dashboard/upload",
    component: Upload,
    meta: { requiresAuth: true }, // ✅ Protected route
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  if (to.meta.requiresAuth && !token) {
    // If trying to access protected route without token → redirect to login
    next("/login");
  } else if (to.path === "/login" && token) {
    // If already logged in and tries to go back to login → redirect to dashboard
    next("/dashboard");
  } else {
    next(); // allow navigation
  }
});

export default router;
