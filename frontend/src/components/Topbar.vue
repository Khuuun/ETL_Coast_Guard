<template>
  <div class="flex justify-between p-5 text-2xl border-b-2 border-gray-200 sticky">
    <div class="flex items-center gap-2">
      <i class="bx bx-menu text-2xl cursor-pointer" @click="$emit('toggleSidebar')"></i>
      <p>Dashboard</p>
    </div>
    <div class="flex items-center gap-2">
      <i class="bxr bx-bell"></i>
      <i class="bxr bx-palette"></i>
    </div>
  </div>
</template>

<script>
export default {
  name: "Topbar",
};
</script>
