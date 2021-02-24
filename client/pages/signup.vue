<template>
  <div class="page-container">
    <div class="title">Blimb</div>
    <input type="text" name="email" id="email" placeholder="Email" class="mb-4">
    <input type="text" name="username" id="username" placeholder="Username" class="mb-4">
    <input type="password" name="password" id="password" placeholder="Password">
    <NuxtLink class="btn btn-link mt-4" to="/login">I already have an account</NuxtLink>
    <button class="btn btn-primary mt-4">Create Account</button>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({})
</script>