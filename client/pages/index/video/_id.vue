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
      <h3 class="text-xl mt-3 pb-2">Reactions</h3>
      <div class="p-1" v-for="reaction in displayedReactions" :key="reaction.date">
        <span class="border-r-2 border-solid border-gray-300 pr-1 mr-1 text-gray-500">{{ reaction.timestamp }}</span>{{ reaction.text }}
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
    let id: number;

    try {
      id = Number(context.params.id);

      [video, reactions] = await Promise.all([Api.getVideoDetail(context.app.$axios, id), Api.getReactions(context.app.$axios, id)]);
      video.sources = [{
        src: `http://localhost:8000${video.file}`,
        type: 'video/mp4'
      }];

      reactions = reactions.filter(reaction => reaction.text !== '');
      reactions.sort((a, b) => a.moment - b.moment);

      category = await Api.getReactionOptions(context.app.$axios, video.category);
    } catch (e) {
      error = true;
    }

    //@ts-ignore
    return { video, error, category, id, reactions };
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

      this.displayedReactions = reactions.filter(reaction => reaction.moment <= total);
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