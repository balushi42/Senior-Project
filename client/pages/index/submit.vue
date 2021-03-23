<template>
  <div class="container mx-auto p-3 md:p-0">
    <div class="text-3xl font-semibold pt-3 pb-5">Post a new highlight</div>
    <input type="text" placeholder="Title" />
    <File class="mt-3" @error="error" @upload="upload" :error="uploadError.length > 0" />
    <TransitionHeight>
      <p v-if="uploadError.length > 0" class="error mb-3 font-semibold">{{ uploadError }}</p>
    </TransitionHeight>
    <div v-for="category in categories" :key="category.id">
      {{ category.title }}
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Api, { Category } from '~/services/api';

export default Vue.extend({
  middleware: 'auth',
  auth: true,
  async asyncData(context) {
    const categories = await Api.getCategories(context.app.$axios);
    return { categories }
  },
  data () {
    return {
      uploadError: '',
      file: null as File|null,
      cateogries: [] as Category[]
    }
  },
  methods: {
    error(message: string) {
      this.uploadError = message;
    },
    upload(file: File|null) {
      this.uploadError = '';
      this.file = file;
    }
  }
})
</script>
