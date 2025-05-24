<template>
  <div id="app">
    <NavbarComponent />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "App",
  components: {
    NavbarComponent,
  },
};
</script>

<style lang="scss">
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 20px 0;
}
</style>
