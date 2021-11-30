<template>
  <tr>
    <td class="border border-green-600">{{name}}</td>
    <td class="border border-green-600">{{queueData}}</td>
    <td class="border border-green-600">{{cmdData}}</td>
  </tr>
</template>

<script lang="ts">
import { defineComponent } from 'vue'


export default defineComponent({
  name: 'ComponentTableRow',
  props: {
    name: {
      type: String,
      required: true
    },
    queueData: {
      type: Object,
      required: true
    },
    cmdData: {
      type: Object,
      required: true
    }
  }
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>