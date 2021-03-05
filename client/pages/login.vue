<template>
  <div class="page-container">
    <div class="title">Blimp</div>
    <input type="text" name="username" id="username" placeholder="Username" class="mb-4">
    <input type="password" name="password" id="password" placeholder="Password">
    <NuxtLink class="btn btn-link mt-4" to="/signup">I need an account</NuxtLink>
    <button class="btn btn-primary mt-4">Login</button>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({})
</script>