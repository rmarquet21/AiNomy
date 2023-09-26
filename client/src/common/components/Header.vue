<script lang="ts" setup>

</script>

<template>
  <nav class="flex px-12 font-heading font-medium bg-blue-800 w-full fixed top-0 left-0">
    <div class="flex w-screen items-center justify-center">
      <div class="w-1/3">
        <router-link to="/">
          <img class="" src="/assets/logos/ainomy.svg" alt="">
        </router-link>
      </div>
      <ul class="flex px-4 w-1/3 justify-center h-full items-center">
        <li class="flex hover:border-b-2 h-full items-center border-b-2 border-transparent hover:border-sky-200">
          <router-link class="flex items-center text-white hover:text-sky-200 h-full" to="analysis">
            Analysis
          </router-link>
        </li>
      </ul>
      <div class="w-1/3" />
    </div>
  </nav>
</template>
