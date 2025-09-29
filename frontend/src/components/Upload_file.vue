<template>
  <div class="dash-box-shadow rounded-lg p-6">
    <div>
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold text-gray-800">File Upload</h2>
        <div class="text-sm text-gray-500">Max 5 files • 10MB each</div>
      </div>

      <!-- Upload Area -->
      <div
        id="upload-area"
        class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-gray-500 transition-colors"
      >
        <input type="file" id="file-input" multiple accept=".xls,.xlsx,.csv" class="hidden" />
        <div class="text-gray-500">
          <i class="fas fa-cloud-upload-alt text-4xl mb-4"></i>
          <p class="text-lg font-medium mb-2">Drag & drop files here</p>
          <p class="text-sm">
            or
            <button class="text-primary hover:underline">browse files</button>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "upload_file_section",
};
</script>
