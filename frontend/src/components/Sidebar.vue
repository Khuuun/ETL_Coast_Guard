<template>
  <transition name="slide">
    <aside class="h-full flex flex-col bar-box-shadow p-6 text-nowrap">
      <div class="flex gap-2 items-center mb-2">
        <img
          class="w-8 h-8"
          src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiByeD0iOCIgZmlsbD0iIzFlNDBhZiIvPgo8cGF0aCBkPSJNMTIgMTJIMjhWMjhIMTJWMjhaIiBmaWxsPSJ3aGl0ZSIvPgo8cGF0aCBkPSJNMTggMThIMjJWMjJIMThWMThaIiBmaWxsPSIjZjU5ZTBiIi8+Cjwvc3ZnPgo="
        />
        <div class="flex flex-col">
          <p class="font-bold text-lg">Coast Guard</p>
          <p class="text-xs text-gray-500">File Upload System</p>
        </div>
      </div>
      <nav class="space-y-2 px-2">
        <a
          href="/dashboard"
          class="flex items-center space-x-3 py-2 rounded-lg hover:bg-gray-100 px-2"
        >
          <i class="bxr bx-dashboard"></i>
          <p>Dashboard</p>
        </a>
        <!-- <a class="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-gray-100">
        <i class="bxr bx-folder-up-arrow"></i>
        <p>File Upload</p>
      </a>
      <a class="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-gray-100">
        <i class="bxr bx-history"></i>
        <p>Upload History</p>
      </a>
      <a class="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-gray-100">
        <i class="bxr bx-user-square"></i>
        <p>Users</p>
      </a> -->
        <a
          href="/dashboard/upload"
          class="flex items-center space-x-3 py-2 rounded-lg hover:bg-gray-100 px-2"
          v-if="isAdmin"
        >
          <i class="bxr bx-folder-up-arrow"></i>
          <p>Upload File</p>
        </a>
        <button
          @click="logout"
          class="flex items-center space-x-3 py-2 rounded-lg hover:bg-gray-100 px-2 w-full"
        >
          <i class="bxr bx-arrow-out-left-square-half"></i>
          <p>Logout</p>
        </button>
      </nav>
      <div class="flex items-center gap-2 border-t border-gray-300 py-2 mt-2">
        <img
          src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIiIGhlaWdodD0iMzIiIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMTYiIGN5PSIxNiIgcj0iMTYiIGZpbGw9IiNlNWU3ZWIiLz4KPHBhdGggZD0iTTE2IDE4QzE4LjIwOTEgMTggMjAgMTYuMjA5MSAyMCAxNEMyMCAxMS43OTA5IDE4LjIwOTEgMTAgMTYgMTBDMTMuNzkwOSAxMCAxMiAxMS43OTA5IDEyIDE0QzEyIDE2LjIwOTEgMTMuNzkwOSAxOCAxNiAxOFoiIGZpbGw9IiM2YjcyODAiLz4KPHBhdGggZD0iTTI0IDI0QzI0IDIxLjc5MDkgMjIuMjA5MSAyMCAyMCAyMEgxMkM5Ljc5MDkgMTIgOCAyMS43OTA5IDggMjRWOEM4IDIxLjc5MDkgOS43OTA5IDI0IDEyIDI0SDIwQzIyLjIwOTEgMjQgMjQgMjIuMjA5MSAyNCAyMFoiIGZpbGw9IiM2YjcyODAiLz4KPC9zdmc+Cg=="
          alt="User"
          class="w-8 h-8 rounded-full"
        />
        <div>
          <p class="text-xs">John Doe</p>
          <p class="text-xs text-gray-500">Regional Manager</p>
        </div>
      </div>
    </aside>
  </transition>
</template>

<style>
.bar-box-shadow {
  height: 100%;
  box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}
</style>

<script>
export default {
  name: "Sidebar",
  props: {
    isAdmin: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    logout() {
      if (confirm("Are you sure you want to logout?")) {
        // 1️⃣ Remove token and user info
        localStorage.removeItem("token");
        localStorage.removeItem("user");

        // 2️⃣ Redirect to login page
        window.location.replace("/login");
      }
    },
  },
};
</script>
