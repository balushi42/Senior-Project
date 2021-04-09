<template>
  <div class="container mx-auto p-3 md:p-0 w-full max-w-3xl">
    <div class="text-3xl font-semibold pt-3 pb-5">Post a new highlight</div>
    <TransitionHeight>
      <p v-if="detailError.length > 0" class="error mb-3 font-semibold">{{  detailError }}</p>
    </TransitionHeight>

    <input class="w-8/12" type="text" placeholder="Title" v-model="title" :class="{'error': titleErrors.length > 0}" @input="input" />
    <TransitionHeight>
      <div v-if="titleErrors.length > 0" class="input-help error">
        <div v-for="error in titleErrors" :key="error">
          {{ error }}
        </div>
      </div>
    </TransitionHeight>
    <File class="mt-3" @error="error" @upload="upload" :error="fileErrors.length > 0" />
    <TransitionHeight>
      <div v-if="fileErrors.length > 0" class="input-help error">
        <div v-for="error in fileErrors" :key="error">
          {{ error }}
        </div>
      </div>
    </TransitionHeight>
    <SearchOptions :categories="categories" class="mt-3" @input="changeCategory" :error="categoryErrors.length > 0" />
    <TransitionHeight>
      <div v-if="categoryErrors.length > 0" class="input-help error">
        <div v-for="error in categoryErrors" :key="error">
          {{ error }}
        </div>
      </div>
    </TransitionHeight>

    <button class="btn btn-primary mt-3" :class="{ loading }" @click="post">Post</button>
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
      detailError: '',
      titleErrors: [] as string[],
      categoryErrors: [] as string[],
      fileErrors: [] as string[],
      file: null as File|null,
      title: '',
      cateogries: [] as Category[],
      loading: false,
      category: null as number|null
    }
  },
  methods: {
    error(message: string) {
      this.fileErrors = [message];
    },
    upload(file: File|null) {
      this.fileErrors = [];
      this.file = file;
    },
    changeCategory(id: number) {
      this.category = id;

      this.categoryErrors = [];
    },
    input() {
      this.titleErrors = [];
    },
    async post() {
      this.loading = true;

      try {
        await Api.newPost(this.$axios, this.title, this.category ?? 0, this.file!);

        this.detailError = '';
        this.titleErrors = [];
        this.fileErrors = [];
        this.categoryErrors = [];
      } catch (e) {
        this.titleErrors = e.response.data.title ?? [];
        this.detailError = e.response.data.detail ?? '';

        let categoryErrors = [];
        for (let category of (e.response.data.category ?? []) as string[]) {
          let entry = category;
          if (entry.includes('does not exist')) {
            entry = 'The category selected was not found.';
          }

          categoryErrors.push(entry);
        }

        this.categoryErrors = categoryErrors;

        let fileErrors = [];
        for (let file of (e.response.data.file ?? []) as string[]) {
          let entry = file;
          if (entry.includes('null')) {
            entry = 'This field may not be blank..';
          }

          fileErrors.push(entry);
        }

        this.fileErrors = fileErrors;
        console.error(e);
      } finally {
        this.loading = false;
      }
    }
  }
})
</script>
