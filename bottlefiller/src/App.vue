<template>
  <nav id="nav">
    <div>
      <router-link to="/">Home</router-link> |
      <router-link to="/debug">Debug</router-link>
    </div>
    <div>
      <p>connected</p>
    </div>
  </nav>
  <router-view/>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import {setupSocket} from "../socket";
import { useStore } from '@/store/store';

export default defineComponent({
  setup(_props) {

    const store = useStore()
    setupSocket(store.updateQueue, store.setWsConnected)

    return {}
  }
});
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
