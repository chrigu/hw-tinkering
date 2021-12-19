
<template>
  <div class="test text-center">
      <div>
        <select>
            <option
                v-for="c in store.components"
                v-bind:key="c"  value="c">{{ c }}</option>
        </select>
        <input
            class="border-solid border-2 p2"
            v-model="cmd"
            type="text" />
        <button
            class="border-green-500 border-solid border-2 bg-green-300 p-2"
            @click="sendCommand">Send command</button>
        <QueueDisplay
          :value="store.latestData"
          :title="'Latest Data'"></QueueDisplay>
        <QueueDisplay
          :value="store.latestCmd"
          :title="'Latest Cmd'"></QueueDisplay>
        <div class="flex flex-col gap-2 sm:flex-row">
          <QueueHistory
            class="sm:w-1/2 w-full"
            :queue="store.cmdQueue"
            :title="'cmd history'"></QueueHistory>
          <QueueHistory
            class="sm:w-1/2 w-full"
            :queue="store.data"
            :title="'data history'"></QueueHistory>
        </div>
        <ComponentTable :component-data="store.latestValuesForComponents" />
      </div>
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
