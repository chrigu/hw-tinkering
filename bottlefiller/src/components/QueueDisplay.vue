<template>
  <div>
    {{value}}
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'


export default defineComponent({
  name: 'QueueDisplay',
  props: {
    value: {
      type: Object,
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