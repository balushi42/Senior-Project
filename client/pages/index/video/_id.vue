<template>
  <div class="container mx-auto p-3 md:p-0 mt-5">
    <article class="video-card" v-if="!error">
      <div class="video-card-title">
        <h1 class="text-xl font-normal">{{ video.title }}</h1>
        <div class="video-card-author">
          Posted by <NuxtLink :to="`/profile/${video.user.id}`">@{{ video.user.username }}</NuxtLink>
        </div>
      </div>
      <div class="video-card-container">
        <Video class="video-card-video" :sources="video.sources" :options="options"/>
      </div>
      <div class="video-card-footer">
        <div class="select-none">&nbsp;</div>
        <button class="btn btn-link btn-report">Report</button>
      </div>
      <h3 class="text-xl">Comments</h3>
    </article>
    <div v-if="error" class="text-center text-3xl">
      Video not found!
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import Api, { Video } from '~/services/api';
export default Vue.extend({
  async asyncData(context) {
    let video: Video|null;
    let error = false;

    try {
      const res = await Api.getVideoDetail(context.app.$axios, context.params.id);
      res.sources = [{
        src: `http://localhost:8000${res.file}`,
        type: 'video/mp4'
      }];

      video = res;
    } catch (e) {
      error = true;
    }

    //@ts-ignore
    return { video, error };
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
});
</script>

<style lang="scss" scoped>
@import '~/assets/css/video.scss';

.video-card {
  @apply border-0;
}
</style>