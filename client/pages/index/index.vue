<template>
    <div></div>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
    middleware(context) {
        if (context.$auth.loggedIn) {
            return context.redirect('/timeline');
        }

        return context.redirect('/popular');
    }
})
</script>