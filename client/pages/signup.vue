<template>
  <div class="page-container">
    <NuxtLink class="title cursor-pointer select-none" to="/">
      Blimp
    </NuxtLink>
    <TransitionHeight>
      <p v-if="detailError.length > 0" class="error mb-3 font-semibold">{{ detailError }}</p>
    </TransitionHeight>
    <input type="text" name="email" id="email" placeholder="Email" v-model="email" @keydown.enter="signup">
    <TransitionHeight>
      <div v-if="emailErrors.length > 0" class="input-help error">
        <div v-for="error in emailErrors" :key="error">
          {{ error }}
        </div>
      </div>
    </TransitionHeight>
    <div class="mb-4"></div>
    <input type="text" name="username" id="username" placeholder="Username" v-model="username" @keydown.enter="signup">
    <TransitionHeight>
      <div v-if="loginErrors.length > 0" class="input-help error">
        <div v-for="error in loginErrors" :key="error">
          {{ error }}
        </div>
      </div>
    </TransitionHeight>
    <div class="mb-4"></div>
    <input type="password" name="password" id="password" placeholder="Password" v-model="password" @keydown.enter="signup">
    <TransitionHeight>
      <div v-if="passwordErrors.length > 0" class="input-help error">
        <div v-for="error in passwordErrors" :key="error">
          {{ error }}
        </div>
      </div>
    </TransitionHeight>
    <NuxtLink to="/login" custom v-slot="{ navigate }">
      <button class="btn btn-link mt-4" @click="navigate">I already have an account</button>
    </NuxtLink>
    <button class="btn btn-primary mt-4" :class="{ loading }" @click="signup">Create Account</button>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import TransitionHeight from '~/components/TransitionHeight.vue';
import Api from '~/services/api';

export default Vue.extend({
  components: { TransitionHeight },
  data() {
    return {
      loading: false,
      detailError: '',
      emailErrors: [] as string[],
      loginErrors: [] as string[],
      passwordErrors: [] as string[],
      email: '',
      username: '',
      password: ''
    }
  },
  methods: {
    async signup() {
      this.loading = true;

      try {
        const username = this.username;
        const password = this.password;

        await Api.signup(this.$axios, this.email, username, password);
        await this.$auth.loginWith('local', {
          data: {
            username,
            password
          }
        });

        this.loginErrors = [];
        this.passwordErrors = [];
        this.detailError = '';

        this.$auth.setUser(this.username);

        this.$router.push('/');
      } catch (e) {
        this.emailErrors = e.response.data.email ?? [];
        this.loginErrors = e.response.data.username ?? [];
        this.passwordErrors = e.response.data.password ?? [];
        this.detailError = e.response.data.detail ?? '';
        
        if (e.response.status !== 400 && e.response.status !== 401) {
          this.detailError = 'Internal server error';
        }
      } finally {
        this.loading = false;
      }
    }
  }
})
</script>