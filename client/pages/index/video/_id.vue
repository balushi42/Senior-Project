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
        <Video class="video-card-video" :sources="video.sources" :options="options" :videoId="id" :category="category" @progress="progress"/>
      </div>
      <h3 class="text-xl mt-3">Reactions</h3>
      <div v-for="reaction in displayedReactions" :key="reaction.date">
        {{ reaction.text }}
      </div>
    </article>
    <div v-if="error" class="text-center text-3xl">
      Video not found!
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import Api, { PostReactionParsed, Video } from '~/services/api';
export default Vue.extend({
  async asyncData(context) {
    let video: Video|null;
    let error = false;
    let category;
    let reactions;

    try {
      const res = await Api.getVideoDetail(context.app.$axios, context.params.id);
      res.sources = [{
        src: `http://localhost:8000${res.file}`,
        type: 'video/mp4'
      }];

      category = await Api.getReactionOptions(context.app.$axios, res.category);
      reactions = await Api.getReactions(context.app.$axios, Number(context.params.id));
      reactions.sort((a, b) => a.timestamp - b.timestamp);

      video = res;
    } catch (e) {
      error = true;
    }

    //@ts-ignore
    return { video, error, category, id: Number(context.params.id), reactions };
  },
  data () {
    return {
      options: {
        autoplay: false,
        volume: 0.9,
        poster: ''
      },
      displayedReactions: [] as PostReactionParsed[]
    }
  },
  methods: {
    progress(time: string) {
      const pieces = time.split(':');
      let total = Number(pieces[0]) * 60 * 60;
      total += Number(pieces[1]) * 60;
      total += Number(pieces[2]);

      //@ts-ignore
      const reactions = this.reactions as PostReactionParsed[];

      this.displayedReactions = reactions.filter(reaction => reaction.timestamp < total);
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