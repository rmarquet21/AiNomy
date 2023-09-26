<template>
  <main class="h-screen">
    <Navbar />
    <div class="w-auto h-full flex">
      <Sidebar />
      <div class="p-4 grow">
        <router-view />
      </div>
    </div>
  </main>
</template>
