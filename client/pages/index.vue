<template>
  <div>
    <nav>
      <div>
        <button class="btn-link" @click="open">
          <Fa icon="bars" />
        </button>

        <NuxtLink to="/" tag="a" class="nav-header">
          Blimp
        </NuxtLink>

        <ul v-bind:class="{'show': showBar, 'closing': closingBar}">
          <div class="flex justify-between md:hidden">
            <div class="w-1/4" />
            <NuxtLink to="/" tag="a" class="nav-header w-1/2 h-full text-center">
              Blimp
            </NuxtLink>
            <div class="w-1/4 flex justify-end p-2 self-stretch">
              <button class="mr-4 btn-link" @click="close">
                <Fa icon="times" class="h-auto" />
              </button>
            </div>
          </div>
          <li>
            <NuxtLink to="/" tag="a">
              Home
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/popular" tag="a">
              Popular
            </NuxtLink>
          </li>

          <li class="md:ml-auto md:mr-2" v-if="!loggedIn">
            <NuxtLink to="/login" tag="a" class="btn-primary md:rounded-md">
              Login
            </NuxtLink>
          </li>
          <li class="md:mr-2" v-if="!loggedIn">
            <NuxtLink to="/signup" tag="a">
              Signup
            </NuxtLink>
          </li>

          <li class="md:ml-auto md:mr-2" v-if="loggedIn">
            <a class="btn-primary cursor-pointer md:rounded-md" @click="logout">
              Logout
            </a>
          </li>
        </ul>
      </div>
    </nav>
    <NuxtChild />
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  data () {
    return {
      showBar: false,
      closingBar: false,
      transitioning: false,
      loggedIn: this.$auth.loggedIn
    }
  },
  methods: {
    logout() {
      this.$auth.logout();
      this.loggedIn = false;
    },
    open () {
      if (this.transitioning) return;
      this.transitioning = true;

      this.showBar = true;
      this.closingBar = false;

      setTimeout(() => {
        this.transitioning = false;
      }, 100);
    },
    close () {
      if (this.transitioning) return;
      this.transitioning = true;

      this.closingBar = true;

      setTimeout(() => {
        this.showBar = false;
        this.closingBar = false;

        this.transitioning = false;
      }, 100);
    }
  }
})
</script>
