<template>
  <div class="h-full flex text-nowrap">
    <Sidebar v-if="isSidebarOpen" :is-admin="isAdmin" />
    <div class="w-full overflow-auto">
      <Topbar @toggleSidebar="toggleSidebar" />
      <div class="flex flex-col p-8 gap-6">
        <div class="flex gap-4">
          <div
            class="flex p-5 gap-2 items-center dash-box-shadow w-full text-center rounded-lg hover:scale-105"
          >
            <div class="bg-blue-700 p-4 rounded-md text-xl text-white">
              <i class="bxr bx-file-plus"></i>
            </div>
            <div class="flex flex-col">
              <p class="text-gray-500">Total Uploads</p>
              <p class="text-3xl">1,234</p>
            </div>
          </div>
          <div
            class="flex p-5 gap-2 items-center dash-box-shadow w-full text-center rounded-lg hover:scale-105"
          >
            <div class="bg-yellow-500 p-4 rounded-md text-xl text-white">
              <i class="bxr bx-check"></i>
            </div>
            <div class="flex flex-col">
              <p class="text-gray-500">Approved</p>
              <p class="text-3xl">987</p>
            </div>
          </div>
          <div
            class="flex p-5 gap-2 items-center dash-box-shadow w-full text-center rounded-lg hover:scale-105"
          >
            <div class="bg-green-500 p-4 rounded-md text-xl text-white">
              <i class="bxr bx-hourglass"></i>
            </div>
            <div class="flex flex-col">
              <p class="text-gray-500">Pending</p>
              <p class="text-3xl">45</p>
            </div>
          </div>
          <div
            class="flex p-5 gap-2 items-center dash-box-shadow w-full text-center rounded-lg hover:scale-105"
          >
            <div class="bg-red-300 p-4 rounded-md text-xl text-red-700">
              <i class="bxr bx-x"></i>
            </div>
            <div class="flex flex-col">
              <p class="text-gray-500">Rejected</p>
              <p class="text-3xl">12</p>
            </div>
          </div>
        </div>
        <!-- UPLOAD SECTION -->

        <Upload v-if="isAdmin"></Upload>

        <div class="dash-box-shadow rounded-lg p-6">
          <div class="flex justify-between">
            <p class="text-lg text-gray-800 font-semibold">Recent Uploads</p>
            <a>View all</a>
          </div>
          <div>
            <table class="w-full divide-y divide-gray-200">
              <thead>
                <tr
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  <th class="p-3">FILE</th>
                  <th class="p-3">SIZE</th>
                  <th class="p-3">STATUS</th>
                  <th class="p-3">DATE</th>
                  <th class="p-3">ACTIONS</th>
                </tr>
              </thead>
              <tbody class="white divide-y divide-gray-200">
                <tr>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">report_2024.pdf</td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">2.3 MB</td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">Approved</td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">2024-08-28</td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">eye delete</td>
                </tr>
                <tr>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">report_2024.pdf</td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">2.3 MB</td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">Approved</td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">2024-08-28</td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-500">eye delete</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.dash-box-shadow {
  box-shadow: rgba(0, 0, 0, 0.05) 0px 6px 24px 0px, rgba(0, 0, 0, 0.08) 0px 0px 0px 1px;
}
</style>

<script>
import { ref } from "vue";
import Sidebar from "../components/Sidebar.vue";
import Topbar from "../components/Topbar.vue";
import Upload from "../components/Upload_file.vue";

export default {
  components: { Sidebar, Topbar, Upload },
  setup() {
    const isSidebarOpen = ref(true); // Sidebar starts visible

    function toggleSidebar() {
      isSidebarOpen.value = !isSidebarOpen.value;
    }

    const user = JSON.parse(localStorage.getItem("user") || "{}");

    return {
      isSidebarOpen,
      toggleSidebar,
      user,
    };
  },
  computed: {
    isAdmin() {
      return this.user.role === "admin";
    },
  },
};
</script>
