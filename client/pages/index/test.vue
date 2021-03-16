<template>
  <Video :sources="video.sources" :options="video.options"></Video>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  data () {
    return {
      video: {
        sources: [{
          src: 'https://www.w3schools.com/html/mov_bbb.mp4',
          type: 'video/mp4'
        }],
        options: {
          autoplay: false,
          volume: 0.5,
          poster: ''
        }
      }
    }
  }
})
</script>
