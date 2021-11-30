<template>
  <div>
    <h2>{{title}}</h2>
    <p v-for="item in queue" :key="item">{{ item }}></p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'


export default defineComponent({
  name: 'QueueHistory',
  props: {
    queue: {
      type: Array,
      required: true
    },
    title: {
      type: String,
      default: 'dfg'
    }
  }
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>