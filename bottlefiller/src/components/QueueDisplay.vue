<template>
  <h3>{{title}}</h3>
  <div>
    {{value}}
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import {Message} from "@/interfaces";


export default defineComponent({
  name: 'QueueDisplay',
  props: {
    value: {
      type: Object as () => Message,
      required: true
    },
    title: {
      type: String,
      default: ''
    }
  }
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>