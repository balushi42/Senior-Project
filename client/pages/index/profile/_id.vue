<template>
  <div class="container mx-auto p-3 md:p-0 mt-5">
    <div class="user-card" v-if="!error">
      <div class="user-card-header">
        <h1 class="user-card-title">@{{ user.username }}</h1>
        <div>
          <button class="btn btn-primary">Add Friend</button>
          <button class="btn btn-link">Report</button>
        </div>
      </div>
      <div>
        Last Active: 4/6/2021 5:58pm
      </div>
      <div>
        Account Created: 3/30/2021 2:09pm
      </div>
    </div>
    <div v-if="error" class="text-center text-3xl">
      User not found!
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import Api, { User } from '~/services/api';

export default Vue.extend({
  async asyncData(context) {
    let user: User|null;
    let error = false;

    try {
      const res = await Api.getProfile(context.app.$axios, context.params.id);

      user = res;
    } catch (e) {
      error = true;
    }

    //@ts-ignore
    return { user, error };
  }
});
</script>

<style lang="postcss" scoped>
.user-card {
  @apply mx-auto w-full max-w-3xl;
}

.user-card-title {
  @apply text-3xl;
}

.user-card-header {
  @apply flex justify-between items-center;
}
</style>