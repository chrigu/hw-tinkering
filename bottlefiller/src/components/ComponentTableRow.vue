<template>
  <tr>
    <td class="border border-green-600">{{name}}</td>
    <td class="border border-green-600">{{latestMessages.data}}</td>
    <td class="border border-green-600">{{latestMessages.cmd}}</td>
  </tr>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { LatesComponentData } from '@/store/store';

export default defineComponent({
  name: 'ComponentTableRow',
  props: {
    name: {
      type: String,
      required: true
    },
    latestMessages: {
      type: Object as () => LatesComponentData,
      required: true
    }
  }
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>