<template>
  <div class="dropdown">
    <input type="text" v-model="categoryText" @blur="blur" @focus="focus" @input="input" :class="{ error }">
    <div class="dropdown-text" :class="{'invisible': categoryText.length > 0, 'text-gray-400': selected}">{{ category.title }}</div>
    <div class="dropdown-menu" v-if="selected" :class="{ 'dropdown-error': error }">
      <button v-for="category of filtered" :key="category.id" class="dropdown-item" :data-id="category.id">
        {{ category.title }}
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { Category } from '~/services/api';

export default Vue.extend({
  props: {
    categories: Array,
    error: Boolean
  },
  data() {
    return {
      category: {
        id: null as number|null,
        title: 'Select Category'
      },
      filtered: this.categories as Category[],
      categoryText: '',
      selected: false,
    }
  },
  methods: {
    input() {
      if (this.categoryText.length < 1) {
        this.filtered = this.categories as Category[];
        return;
      }

      let reg = new RegExp(this.categoryText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gmi');
      this.filtered = this.categories.filter(category => (category as Category).title.match(reg)) as Category[];
    },
    blur(e: FocusEvent) {
      if ((e.relatedTarget as HTMLElement)?.classList.contains('dropdown-item')) {
        const id = Number((e.relatedTarget as HTMLElement).getAttribute('data-id') as string);
        this.category = (this.categories as Category[]).find(category => category.id === id)!;

        this.$emit('input', id);
      }

      this.filtered = this.categories as Category[];

      this.categoryText = '';
      this.selected = false;
    },
    focus() {
      this.selected = true;
    }
  }
});
</script>

<style lang="scss" scoped>
.dropdown {
  @apply w-full md:w-6/12 relative px-4 py-3;

  input {
    @apply absolute w-full top-0 left-0;
  }

  .dropdown-text {
    @apply relative pointer-events-none left-0.5 border-2 border-transparent;
  }

  .dropdown-menu {
    top: calc(100% - 3px);
    left: -3px;
    border-width: 5px;
    width: calc(100% + 6px);

    @apply z-50 absolute bg-white border-green-400 border-t-0 rounded-b-md;

    .dropdown-item {
      @apply block w-full text-left p-1 pl-4;
    }

    .dropdown-item:hover {
      @apply bg-green-200;
    }

    .dropdown-item:focus {
      @apply outline-none;
    }
  }

  .dropdown-menu.dropdown-error {
    @apply border-red-500;
  }
}
</style>