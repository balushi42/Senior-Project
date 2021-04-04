<template>
  <div class="container mx-auto p-3 md:p-0 mt-5">
    <article v-for="video in videos" :key="video.id" class="video-card">
      <div class="video-card-title">
        <NuxtLink :to="`/video/${video.id}`">{{ video.title }}</NuxtLink>
        <div class="video-card-author">
          Posted by <NuxtLink :to="`/profile/${video.user.id}`">@{{ video.user.username }}</NuxtLink>
        </div>
      </div>
      <Video :sources="video.sources" :options="options"/>
      <div class="video-card-footer">
        <NuxtLink :to="`/video/${video.id}`">{{ 0 }} comments</NuxtLink>
        <button class="btn btn-link btn-report">Report</button>
      </div>
    </article>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Api from '~/services/api';

export default Vue.extend({
  middleware: 'auth',
  auth: true,
  async asyncData(context) {
    const videos = await Api.getViralVideos(context.app.$axios);
    for (let video of videos) {
      video.sources = [{
        src: `http://localhost:8000${video.file}`,
        type: 'video/mp4'
      }];
    }

    return { videos }
  },
  data () {
    return {
      options: {
        autoplay: false,
        volume: 0.9,
        poster: ''
      }
    }
  }
})
</script>

<style lang="postcss" scoped>
.video-card {
  border-width: 1px;

  @apply border-solid rounded-md border-gray-300 w-full max-w-3xl md:mx-auto mb-4;
}

.video-card-author {
  @apply font-normal text-sm;
}

.video-card-author > a {
  @apply hover:underline;
}

.video-card-title {
  @apply block p-2 font-semibold;
}

.video-card-title > a {
  @apply text-green-700 hover:underline;
}

.video-card-footer {
  @apply p-2 flex justify-between items-center;
}

.video-card-footer > a {
  @apply hover:underline;
}

.btn-report {
  @apply py-1;
}
</style>