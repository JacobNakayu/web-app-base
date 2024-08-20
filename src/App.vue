<template>
  <div id="app">
    <header>
      <h1>Welcome to My Vue App!</h1>
    </header>
    <main>
      <p>This is the main content area.</p>
      <p>{{ message }}</p>
    </main>
    <footer>
      <p>&copy; 2024 My Vue App</p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Define any reactive variables or methods here
const message = ref('Hello, Vue!')
</script>

<style scoped>
/* Scoped styles for this component */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

header {
  background-color: #42b983;
  padding: 1rem;
  color: white;
}

footer {
  background-color: #42b983;
  padding: 1rem;
  color: white;
  position: fixed;
  bottom: 0;
  width: 100%;
}
</style>
