<template>
  <div id="app">
    <header>
      <h1>Welcome to My Vue App!</h1>
    </header>
    <p>
      <strong>Current Rout Path:</strong> {{ $route.fullPath }}
    </p>
    <nav>
      <p><RouterLink to="/home">Go to Home</RouterLink></p>
      <p><RouterLink to="/about">Go to About</RouterLink></p>
      <p><RouterLink to="/">Go Back</RouterLink></p>
    </nav>
    <main>
      <div class="container">
        <RouterView /> <!-- This is where any other Vue files will be loaded when the Router links to them. -->
        <div class="col-4">
          <p>This is the main content area.</p>
          <p>{{ message }}</p>
        </div>
      </div>
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
