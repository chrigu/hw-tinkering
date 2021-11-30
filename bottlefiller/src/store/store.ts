import {Message} from '@/interfaces'
import { defineStore } from 'pinia'

const MAX_QUEUE_LENGTH = 20

export interface State {
  gasVolumeIn: number;
  gasVolumeOut: number;
  data: Message[];
  cmd: Message[];
}

const addToQueue = (queue: Message[], value: Message): Message[] => {
  queue.push(value)
  if (queue.length > MAX_QUEUE_LENGTH) {
    const diff = queue.length = MAX_QUEUE_LENGTH
    return queue.slice(diff)
  }

  return queue
}

export const useStore = defineStore('main', {
  state: () => ({
    gasVolumeIn: 0.0,
    gasVolumeOut: 0.0,
    data: [] as Message[],
    cmd: [] as Message[],
    components: ['sm', 'fm1', 'fm2', 'm1', 'm2', 'web']
  }),
  getters: {
    dataQueue: (state) => state.data.reverse(),
    cmdQueue: (state) => state.cmd.reverse(),
    latestData: (state) => state.data.length == 0 ? {} : state.data[state.data.length-1],
    latestCmd: (state) => state.cmd.length == 0 ? {} : state.cmd[state.cmd.length-1],
    components: (state) => state.components
  },
  actions: {
    updateQueue(queueMsg: Message) {
      console.log('Got message', {queueMsg})
      if (queueMsg.messageType === 'data') {
        this.data = addToQueue(this.data, queueMsg)
      }
      if (queueMsg.messageType === 'cmd') {
        this.cmd = addToQueue(this.cmd, queueMsg)
      }
    }
  },
})
