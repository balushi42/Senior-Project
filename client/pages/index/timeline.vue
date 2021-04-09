<template>
  <div class="container mx-auto p-3 md:p-0 mt-5">
    <div class="text-3xl font-semibold pt-3 pb-5 w-full max-w-3xl md:mx-auto">Your Timeline</div>
    <article v-for="video in videos" :key="video.id" class="video-card">
      <div class="video-card-title">
        <NuxtLink :to="`/video/${video.id}`">{{ video.title }}</NuxtLink>
        <div class="video-card-author">
          Posted by <NuxtLink :to="`/profile/${video.user.id}`">@{{ video.user.username }}</NuxtLink>
        </div>
      </div>
      <div class="video-card-container">
        <Video class="video-card-video" :sources="video.sources" :options="options" :videoId="video.id" :category="categories[video.id]"/>
      </div>
      <div class="video-card-footer">
        <NuxtLink :to="`/video/${video.id}`">{{ 0 }} comments</NuxtLink>
        <button class="btn btn-link btn-report">Report</button>
      </div>
    </article>
    <div v-if="videos.length < 1" class="text-center text-3xl w-full max-w-3xl md:mx-auto">
      Nothing In Your Timeline
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Api, { Reactions } from '~/services/api';

export default Vue.extend({
  middleware: 'auth',
  auth: true,
  async asyncData(context) {
    const videos = await Api.getTimeline(context.app.$axios);
    let categories: Record<number, Reactions> = {};

    for (let video of videos) {
      video.sources = [{
        src: `http://localhost:8000${video.file}`,
        type: 'video/mp4'
      }];

      if (!categories[video.category]) {
        categories[video.category] = await Api.getReactionOptions(context.app.$axios, video.category);
      }
    }

    return { videos, categories };
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
@import '~/assets/css/video.scss';
</style>