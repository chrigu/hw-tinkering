<template>
  <table class="border-collapse border border-green-800">
    <thead>
        <tr>
        <th class="border border-green-600">Component</th>
        <th class="border border-green-600">Data</th>
        <th class="border border-green-600">Command</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <td class="border border-green-600">Indiana</td>
        <td class="border border-green-600">Indianapolis</td>
        <td class="border border-green-600">Indianapolis</td>
        </tr>
        <tr>
        <td class="border border-green-600">Ohio</td>
        <td class="border border-green-600">Columbus</td>
        <td class="border border-green-600">Columbus</td>
        </tr>
        <tr>
        <td class="border border-green-600">Michigan</td>
        <td class="border border-green-600">Detroit</td>
        <td class="border border-green-600">Detroit</td>
        </tr>
    </tbody>
  </table>
</template>

<script lang="ts">
import { defineComponent } from 'vue'


export default defineComponent({
  name: 'ComponentData',
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