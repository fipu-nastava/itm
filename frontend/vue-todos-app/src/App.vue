<template>
  <div id="app">
    <img alt="TODOs logo" src="./assets/todos.jpg">
    <todos></todos>
  </div>
</template>

<script>
import Todos from './components/Todos.vue'

export default {
  name: 'app',
  components: {
    Todos
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
  margin-top: 40px;
  margin: 0 auto;
  width: 800px;
}

img {
  width: 150px;
  margin: 0 auto;
  display: block;
  padding-bottom: 15px;
}
</style>

<!-- https://codepen.io/Laosing/pen/YozzYN -->