<template>
  <div class="container mx-auto p-3 md:p-0 w-full max-w-3xl">
    <div v-if="!error">
      <div class="text-3xl font-semibold pt-3 pb-5">Pending Friend Requests</div>
      <article v-for="friend of pending" :key="friend.creator" class="w-full flex justify-between border-2 border-solid border-gray-200 rounded-md p-4 mb-3">
        <div>
          <div>User</div>
          <NuxtLink class="text-green-500 hover:underline" :to="`/profile/${friend.creator}/`">@{{ friend.user.username }}</NuxtLink>
        </div>
        <div>
          <button class="btn btn-primary" :class="{ loading }" @click="accept(friend.creator)">Accept</button>
        </div>
      </article>
      <div v-if="pending.length < 1" class="text-center text-3xl">
        No Pending Friend Requests
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import Api, { PendingFriendRequest } from '~/services/api';

export default Vue.extend({
  async asyncData(context) {
    let pending: PendingFriendRequest[]|null;
    let error = false;

    try {
      const res = await Api.getMe(context.app.$axios);
      pending = await Api.getMyPending(context.app.$axios, res.id);

    } catch (e) {
      error = true;
    }

    //@ts-ignore
    return { error, pending };
  },
  data() {
    return {
      loading: false,
    }
  },
  methods: {
    async accept(friend: number) {
      this.loading = true;
      try {
        const req = await Api.acceptFriend(this.$axios, friend);

        //@ts-ignore
        this.pending = this.pending.filter(p => p.creator !== friend);        
        console.log(req);
      } catch (e) {
        console.error(e.response.data);
      } finally {
        this.loading = false;
      }
    }
  }
});
</script>
