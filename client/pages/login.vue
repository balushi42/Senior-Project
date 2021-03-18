<template>
  <div class="page-container">
    <NuxtLink class="title cursor-pointer select-none" to="/">
      Blimp
    </NuxtLink>
    <TransitionHeight>
      <p v-if="detailError.length > 0" class="error mb-3 font-semibold">{{  detailError }}</p>
    </TransitionHeight>
    <input id="username" type="text" name="username" placeholder="Username" :class="{ 'error': loginErrors.length > 0 }" @input="resetUsername" v-model="username">
    <TransitionHeight>
      <div v-if="loginErrors.length > 0" class="input-help error">
        <div v-for="error in loginErrors" :key="error">
          {{ error }}
        </div>
      </div>
    </TransitionHeight>
    <div class="mb-4"></div>
    <input id="password" type="password" name="password" placeholder="Password" :class="{ 'error': passwordErrors.length > 0 }" @input="resetPassword" v-model="password">
    <TransitionHeight>
      <div v-if="passwordErrors.length > 0" class="input-help error">
        <div v-for="error in passwordErrors" :key="error">
          {{ error }}
        </div>
      </div>
    </TransitionHeight>
    <NuxtLink class="btn btn-link mt-4" to="/signup" tag="button">
      I need an account
    </NuxtLink>
    <button class="btn btn-primary mt-4" tag="button" :class="{ loading }" @click="login">
      Login
    </button>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import TransitionHeight from '~/components/TransitionHeight.vue';

export default Vue.extend({
  components: { TransitionHeight },
  data() {
    return {
      loading: false,
      loginErrors: [] as string[],
      passwordErrors: [] as string[],
      detailError: '',
      password: '',
      username: ''
    }
  },
  methods: {
    async login() {
      this.loading = true;

      try {
        await this.$auth.loginWith('local', {
          data: {
            username: this.username,
            password: this.password
          }
        });

        this.loginErrors = [];
        this.passwordErrors = [];
        this.detailError = '';

        this.$auth.setUser(this.username);

        this.$router.push('/');
      } catch (e) {
        this.loginErrors = e.response.data.username ?? [];
        this.passwordErrors = e.response.data.password ?? [];
        this.detailError = e.response.data.detail ?? '';
        
        if (e.response.status !== 400 && e.response.status !== 401) {
          this.detailError = 'Internal server error';
        }
      } finally {
        this.loading = false;
      }
    },
    resetUsername() {
      this.loginErrors = [];
    },
    resetPassword() {
      this.passwordErrors = [];
    }
  }
})
</script>
