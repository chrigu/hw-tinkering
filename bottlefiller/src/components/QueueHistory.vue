<template>
  <div>
    <h2>{{title}}</h2>
    <ul class="bg-gray-700 text-gray-50 p-2">
      <li class="list-none"
          v-for="item in queue"
          :key="item"><span class="text-green-100">{{item.node}}</span>: <span>{{item.data}}</span></li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import {Message} from "@/interfaces";


export default defineComponent({
  name: 'QueueHistory',
  props: {
    queue: {
      type: Object as () => Message[],
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