<template>
  <table class="border-collapse border border-green-800 table-fixed w-5/6 m-auto">
    <thead>
        <tr>
        <th class="w-1/3 border border-green-600">Component</th>
        <th class="w-1/3 border border-green-600">Data</th>
        <th class="w-1/3 border border-green-600">Command</th>
        </tr>
    </thead>
    <tbody>
        <ComponentTableRow 
        v-for="c in components" 
        v-bind:key="c" 
        :latest-messages="componentData[c]"
        :name="c"/>
    </tbody>
  </table>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { LatestData } from '@/store/store';
import ComponentTableRow from '@/components/ComponentTableRow.vue'


export default defineComponent({
  name: 'ComponentData',
  components: {ComponentTableRow},
  props: {
    componentData: {
      type: Object as () => LatestData,
      required: true
    }
  },
  setup(props) {
      console.log(props.componentData)
      const components = ref(Object.keys(props.componentData))

return {
        components
      }
  }
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>