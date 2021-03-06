<template>
  <div>
    <nav>
      <div>
        <p>
          menu
        </p>

        <NuxtLink to="/" tag="a" class="nav-header">
          Blimp
        </NuxtLink>

        <ul>
          <li>
            <NuxtLink to="/" tag="a">
              Home
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/popular" tag="a">
              Popular
            </NuxtLink>
          </li>
        </ul>
      </div>
    </nav>
    <NuxtChild />
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({})
</script>
