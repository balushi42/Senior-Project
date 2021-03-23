<template>
  <transition
    name="expand"
    @enter="enter"
    @after-enter="afterEnter"
    @leave="leave"
  >
    <slot />
  </transition>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'TransitionHeight',
  methods: {
    enter(e: HTMLStyleElement) {
      const width = getComputedStyle(e).width;

      e.style.width = width;
      e.style.position = 'absolute';
      e.style.visibility = 'hidden';
      e.style.height = 'auto';

      const height = getComputedStyle(e).height;

      //@ts-ignore
      e.style.width = null;
      //@ts-ignore
      e.style.position = null;
      //@ts-ignore
      e.style.visibility = null;
      e.style.height = '0';

      // Force repaint to make sure the
      // animation is triggered correctly.
      getComputedStyle(e).height;

      // Trigger the animation.
      // We use `requestAnimationFrame` because we need
      // to make sure the browser has finished
      // painting after setting the `height`
      // to `0` in the line above.
      requestAnimationFrame(() => {
        e.style.height = height;
      });
    },
    afterEnter(e: HTMLStyleElement) {
      e.style.height = 'auto';
    },
    leave(e: HTMLStyleElement) {
      const height = getComputedStyle(e).height;
      
      e.style.height = height;

      // Force repaint to make sure the
      // animation is triggered correctly.
      getComputedStyle(e).height;

      requestAnimationFrame(() => {
        e.style.height = '0';
      });
    }
  }
});
</script>

<style scoped>
.expand-enter-active,
.expand-leave-active {
  transition: height 0.2s ease-in-out, margin 0.2s ease-in-out;
  overflow: hidden;
}

.expand-enter,
.expand-leave-to {
  height: 0;
}
</style>