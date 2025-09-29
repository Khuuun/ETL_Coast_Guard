<template>
  <div class="h-full flex">
    <Sidebar v-if="isSidebarOpen" />
    <div class="w-full overflow-auto">
      <Topbar @toggleSidebar="toggleSidebar" />
      <div class="flex flex-col p-8 gap-5">
        <div class="p-5 rounded-md shadow-xl">
          <div class="flex gap-2 items-center mb-3 text-xl font-bold">
            <i class="bxr bx-cog"></i>
            <p>Coast Guard Audit Data Pipeline</p>
          </div>
          <div class="grid grid-cols-5 gap-5">
            <div
              class="flex flex-col items-center w-full p-5 rounded-md gap-2 bg-blue-100 border border-blue-300 status-card"
            >
              <div class="bg-blue-500 p-4 rounded-full text-white flex items-center justify-center">
                <i class="bxr bx-arrow-in-down-square-half"></i>
              </div>
              <div class="flex flex-col items-center">
                <p class="text-blue-800 font-semibold text-xs">EXTRACT</p>
                <p class="text-xs text-blue-600">CSV File Upload</p>
              </div>
              <progress :value="stageProgress.extract" max="100" class="h-2 w-full"></progress>
            </div>
            <div
              class="flex flex-col items-center w-full p-5 rounded-md gap-2 bg-yellow-100 border border-yellow-300 status-card"
            >
              <div
                class="bg-yellow-500 p-4 rounded-full text-white flex items-center justify-center"
              >
                <i class="bxr bx-check-circle"></i>
              </div>
              <div class="flex flex-col items-center">
                <p class="text-yellow-800 font-semibold text-xs">VALIDATE</p>
                <p class="text-xs text-yellow-600">Data Quality Check</p>
              </div>
              <progress :value="stageProgress.validate" max="100" class="h-2 w-full"></progress>
            </div>
            <div
              class="flex flex-col items-center w-full p-5 rounded-md gap-2 bg-purple-100 border border-purple-300 status-card"
            >
              <div
                class="bg-purple-500 p-4 rounded-full text-white flex items-center justify-center"
              >
                <i class="bxr bx-swap-vertical"></i>
              </div>
              <div class="flex flex-col items-center">
                <p class="text-purple-800 font-semibold text-xs">TRANSFORM</p>
                <p class="text-xs text-purple-600">Data Processing</p>
              </div>
              <progress value="0" max="100" class="h-2 w-full"></progress>
            </div>
            <div
              class="flex flex-col items-center w-full p-5 rounded-md gap-2 bg-green-100 border border-green-300 status-card"
            >
              <div
                class="bg-green-500 p-4 rounded-full text-white flex items-center justify-center"
              >
                <i class="bxr bx-window-arrow-in"></i>
              </div>
              <div class="flex flex-col items-center">
                <p class="text-green-800 font-semibold text-xs">LOAD</p>
                <p class="text-xs text-green-600">Database Insert</p>
              </div>
              <progress value="0" max="100" class="h-2 w-full"></progress>
            </div>
            <div
              class="flex flex-col items-center w-full p-5 rounded-md gap-2 bg-gray-100 border border-gray-300 status-card"
            >
              <div class="bg-gray-500 p-4 rounded-full text-white flex items-center justify-center">
                <i class="bxr bx-flag-chequered"></i>
              </div>
              <div class="flex flex-col items-center">
                <p class="text-gray-800 font-semibold text-xs">COMPLETE</p>
                <p class="text-xs text-gray-600">ETL Finished</p>
              </div>
              <progress value="0" max="100" class="h-2 w-full"></progress>
            </div>
          </div>
        </div>
      </div>
      <div class="grid grid-cols-3 p-5 gap-5 px-8">
        <div class="col-span-2">
          <div class="rounded-md w-full dash-box-shadow p-2">
            <div class="rounded-lg p-6 flex flex-col gap-4">
              <div>
                <div class="flex items-center justify-between mb-4">
                  <h2 class="text-lg font-semibold text-gray-800">File Upload</h2>
                  <div class="text-sm text-gray-500">Max 5 files • 10MB each</div>
                </div>

                <!-- Upload Area -->
                <div
                  id="upload-area"
                  class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-gray-500 transition-colors"
                  @dragover.prevent="handleDragOver"
                  @dragleave.prevent="handleDragLeave"
                  @drop.prevent="handleDrop"
                  :class="{ 'border-blue-500 bg-blue-50': isDragging }"
                >
                  <input
                    type="file"
                    ref="fileInput"
                    multiple
                    accept=".xls,.xlsx,.csv"
                    class="hidden"
                    @change="handleFiles"
                  />
                  <div class="text-gray-500">
                    <i class="fas fa-cloud-upload-alt text-4xl mb-4"></i>
                    <p class="text-lg font-medium mb-2">Drag & drop files here</p>
                    <p class="text-sm">
                      or
                      <button class="text-primary hover:underline" @click="$refs.fileInput.click()">
                        browse files
                      </button>
                    </p>
                  </div>
                </div>
                <div v-if="selectedFiles.length" class="mt-4 text-left text-sm">
                  <h3 class="font-semibold mb-2">Selected Files:</h3>
                  <ul class="list-disc ml-5">
                    <li v-for="(file, index) in selectedFiles" :key="index">
                      <span class="font-medium">{{ file.name }}</span>
                      <span class="text-gray-500 ml-2"
                        >({{ (file.size / 1024 / 1024).toFixed(2) }} MB)</span
                      >
                    </li>
                  </ul>
                </div>
              </div>

              <div class="flex justify-between text-sm">
                <div>
                  <p>Data Quality Rules</p>
                  <div>
                    <div class="flex gap-2">
                      <input type="checkbox" />
                      <p>Validate date formats</p>
                    </div>
                    <div class="flex gap-2">
                      <input type="checkbox" />
                      <p>Check required fields</p>
                    </div>
                  </div>
                </div>
                <div>
                  <p>Processing Mode</p>
                  <select>
                    <option>Upsert (Update/Insert)</option>
                    <option>Append Only</option>
                    <option>Replace All</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="rounded-md w-full flex flex-col gap-4">
          <div class="flex flex-col gap-4 dash-box-shadow p-4 rounded-md">
            <div>
              <p>Process Control</p>
            </div>
            <button
              class="flex items-center justify-center bg-gray-400 text-white rounded-md p-1 hover:opacity-80"
              @click="uploadFiles"
            >
              <i class="bxr bx-play"></i>
              <span>Start ETL Process</span>
            </button>
            <button
              class="flex items-center justify-center bg-red-400 text-white rounded-md p-1 text-lg hover:opacity-80"
            >
              <i class="bxr bx-pause"></i>
              <p>Stop Process</p>
            </button>
            <div>
              <div class="flex justify-between">
                <p>Overall Progress</p>
                <p>0%</p>
              </div>
              <progress :value="stageProgress.extract" class="w-full"></progress>
            </div>
          </div>
          <div class="flex flex-col gap-2 dash-box-shadow rounded-md p-4">
            <div>
              <span>>_ Processing Logs</span>
            </div>
            <div class="bg-black text-green-300 p-2 rounded-md h-56 overflow-auto">
              <div class="break-words text-xs" v-if="results.length">
                <h3 class="font-bold mb-2">Upload Results</h3>
                <ul>
                  <li class="mb-3" v-for="res in results" :key="res.file">
                    <strong>{{ res.file }}</strong>
                    <span> | Upload: {{ res.upload_status }}</span>
                    <span>
                      | DB Save:
                      <span :class="res.database_save_success ? 'text-green-400' : 'text-red-400'">
                        {{ res.database_save_success ? "Success" : "Failed" }}
                      </span>
                    </span>
                    <span v-if="res.records_saved"> | Records: {{ res.records_saved }}</span>
                    <span v-if="res.database_message"> | {{ res.database_message }}</span>
                    <div v-if="res.missing_columns?.length" class="text-yellow-300">
                      Missing: {{ res.missing_columns.join(", ") }}
                    </div>
                    <div v-if="res.extra_columns?.length" class="text-blue-300">
                      Extra: {{ res.extra_columns.join(", ") }}
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div class="flex flex-col gap-2 dash-box-shadow p-4 text-sm rounded-md">
            <div>
              <p>Statistics</p>
            </div>
            <div class="flex justify-between">
              <p>Total Records:</p>
              <span>0</span>
            </div>
            <div class="flex justify-between">
              <p>Valid Records:</p>
              <span class="text-green-700">0</span>
            </div>
            <div class="flex justify-between">
              <p>Errors:</p>
              <span class="text-red-700">0</span>
            </div>
            <div class="flex justify-between">
              <p>Processing Rate:</p>
              <span class="font-bold">0 records/sec</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
progress {
  appearance: none;
  -webkit-appearance: none;
}

progress::-webkit-progress-bar {
  background-color: #dcdde0; /* gray-200 */
  border-radius: 9999px;
}

progress::-webkit-progress-value {
  background-color: #7072e2; /* blue-500 */
  border-radius: 9999px;
}

progress::-moz-progress-bar {
  background-color: #3b82f6; /* Firefox */
  border-radius: 9999px;
}
.dash-box-shadow {
  box-shadow: rgba(0, 0, 0, 0.05) 0px 6px 24px 0px, rgba(0, 0, 0, 0.08) 0px 0px 0px 1px;
}
.status-card:hover {
  transform: scale(1.03);
}
</style>

<script>
import { ref } from "vue";
import Sidebar from "../components/Sidebar.vue";
import Topbar from "../components/Topbar.vue";
import Upload from "../components/Upload_file.vue";
import axios from "axios";

const stageProgress = ref({
  extract: 0,
  validate: 0,
  transform: 0,
  load: 0,
  complete: 0,
});

const overallProgress = ref(0);
const loading = ref(false);

const selectedFiles = ref([]);
const results = ref([]);
const summary = ref({});

export default {
  components: { Sidebar, Topbar, Upload },
  setup() {
    const isSidebarOpen = ref(true); // Sidebar starts visible
    const selectedFiles = ref([]);
    const results = ref([]);
    const isDragging = ref(false);

    function toggleSidebar() {
      isSidebarOpen.value = !isSidebarOpen.value;
    }

    const handleFiles = (event) => {
      selectedFiles.value = event.target.files;
    };

    const handleDragOver = () => {
      isDragging.value = true;
    };
    const handleDragLeave = () => {
      isDragging.value = false;
    };
    const handleDrop = (event) => {
      isDragging.value = false;
      selectedFiles.value = event.dataTransfer.files;
    };

    const uploadFiles = async () => {
      if (!selectedFiles.value.length) return;
      loading.value = true;

      const formData = new FormData();
      for (let i = 0; i < selectedFiles.value.length; i++) {
        formData.append("files", selectedFiles.value[i]);
      }

      try {
        // ===== EXTRACT STEP =====
        stageProgress.value.extract = 0;
        for (let i = 0; i < selectedFiles.value.length; i++) {
          stageProgress.value.extract = Math.round(((i + 1) / selectedFiles.value.length) * 100);
          overallProgress.value = stageProgress.value.extract * 0.5; // EXTRACT = 50% of overall progress
          await new Promise((resolve) => setTimeout(resolve, 200)); // simulate delay
        }

        // ===== VALIDATE STEP =====
        stageProgress.value.validate = 0;
        for (let i = 0; i < selectedFiles.value.length; i++) {
          stageProgress.value.validate = Math.round(((i + 1) / selectedFiles.value.length) * 100);
          overallProgress.value = 50 + stageProgress.value.validate * 0.5; // VALIDATE = next 50%
          await new Promise((resolve) => setTimeout(resolve, 200)); // simulate delay
        }

        overallProgress.value = 100;

        // ===== Upload to backend =====
        const response = await axios.post("http://127.0.0.1:5000/api/files/upload", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        results.value = response.data.results;
        summary.value = response.data.summary;
      } catch (err) {
        console.error("Upload failed:", err);
      } finally {
        loading.value = false;
      }
    };

    const user = JSON.parse(localStorage.getItem("user") || "{}");

    return {
      isSidebarOpen,
      toggleSidebar,
      selectedFiles,
      results,
      handleFiles,
      uploadFiles,
      user,
      stageProgress,
      overallProgress,
      loading,
      handleDragOver,
      handleDragLeave,
      handleDrop,
      isDragging,
      uploadFiles,
    };
  },
  computed: {
    isAdmin() {
      return this.user.role === "admin";
    },
  },
};
</script>
