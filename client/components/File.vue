<template>
  <div class="flex justify-center items-center w-full md:w-6/12">
    <label class="border-2 border-dashed rounded-md p-4 cursor-pointer w-full" @dragenter="enter" @dragover="enter" @dragleave="leave" @dragend="leave" @drop.stop="drop" :class="{'drag-over': draggingOver, 'file-error': error && !draggingOver}" @change="change">
      <div class="w-full text-center text-2xl pointer-events-none"><Fa icon="upload"/></div>
      <div class="font-semibold text-center pointer-events-none">{{ file }}</div>
      <input class="hidden" type="file" name="file" accept="video/mp4">
    </label>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  props: {
    error: Boolean
  },
  data() {
    return {
      draggingOver: false,
      file: 'Upload File'
    }
  },
  methods: {
    change(e: InputEvent) {
      const files = (e.target as HTMLInputElement).files ?? [];
      if (files.length > 0) {
        this.handleFiles(files[0]);
      }

      e.stopImmediatePropagation();
      e.stopPropagation();
      e.preventDefault();
      return false;
    },
    drop(e: DragEvent) {
      const files = e.dataTransfer?.files ?? [];
      if (files.length > 0) {
        this.handleFiles(files[0]);
      }

      this.leave(e);
    },
    enter(e: DragEvent) {
      this.draggingOver = true;

      e.stopImmediatePropagation();
      e.stopPropagation();
      e.preventDefault();
      return false;
    },
    leave(e: DragEvent) {
      this.draggingOver = false;

      e.stopImmediatePropagation();
      e.stopPropagation();
      e.preventDefault();
      return false;
    },
    handleFiles(file: File) {
      if (file) {
        if (file.type !== 'video/mp4') {
          this.$emit('error', 'File must be an mp4');

          return;
        }

        if (file.size > 10485760) {
          this.$emit('error', 'File is too large (10.48 MB limit)');

          return;
        }

        this.file = file.name;
        this.$emit('upload', file);
      } else {
        this.file = 'Upload File';
        this.$emit('upload', null);
      }
    }
  }
});
</script>

<style lang="postcss">
label {
  transition: all 0.2s;
}

.drag-over {
  @apply border-solid border-green-500 bg-green-100;
}

.file-error {
  @apply border-red-500 text-red-500;
}

</style>