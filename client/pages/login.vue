<template>
  <div class="page-container">
    <div class="title">
      Blimp
    </div>
    <input id="username" type="text" name="username" placeholder="Username" class="mb-4">
    <input id="password" type="password" name="password" placeholder="Password">
    <NuxtLink class="btn btn-link mt-4" to="/signup" tag="button">
      I need an account
    </NuxtLink>
    <button class="btn btn-primary mt-4" tag="button">
      Login
    </button>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({})
</script>
