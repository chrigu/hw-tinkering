
<template>
  <div class="test">
      <input
          class="border-solid border-2 p2"
          v-model="cmd"
          type="text" />
      <button
          class="border-green-500 border-solid border-2 bg-green-300 p-2"
          @click="sendCommand">Send command</button>
      <QueueDisplay 
        :value="store.latestData"
        :title="'Data'"></QueueDisplay>
      <QueueHistory 
        :queue="store.cmdQueue"
        :title="'Data'"></QueueHistory>
      <QueueDisplay 
        :value="store.latestCmd"
        :title="'Cmd'"></QueueDisplay>
      <ComponentTable :component-data="store.latestValuesForComponents" />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useStore } from '@/store/store';
import {send} from "../../socket";

import QueueDisplay from '@/components/QueueDisplay.vue'
import QueueHistory from '@/components/QueueHistory.vue'
import ComponentTable from '@/components/ComponentTable.vue'

export default defineComponent({
  name: 'Test',
  components: {QueueDisplay, QueueHistory, ComponentTable},
  setup(props) {

      const store = useStore()
      const cmd = ref('')

      const sendCommand = () => {
          console.log(cmd.value)
          send(cmd.value)
          cmd.value = ''
      }

      return {
        cmd,
        sendCommand,
        store
      }
  }
});
</script>
