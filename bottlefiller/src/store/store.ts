import {Message} from '@/interfaces'
import { defineStore } from 'pinia'

const MAX_QUEUE_LENGTH = 20

export interface LatesComponentData {
  data: Message | null,
  cmd: Message | null
}

export interface LatestData {
  [k: string]: LatesComponentData
}

export interface State {
  gasVolumeIn: number;
  gasVolumeOut: number;
  data: Message[];
  cmd: Message[];
  wsConnected: boolean;
}

const addToQueue = (queue: Message[], value: Message): Message[] => {
  queue.push(value)
  // if (queue.length > MAX_QUEUE_LENGTH) {
  //   const diff = queue.length = MAX_QUEUE_LENGTH
  //   return queue.slice(diff)
  // }

  return queue
}

const findLatestForComponent = (data: Message[], component: string): Message | null => {
  const dataForComponent = data.filter(message => message.node === component)
  return dataForComponent.length > 0 ? dataForComponent[dataForComponent.length -1] : null
}

export const useStore = defineStore('main', {
  state: () => ({
    gasVolumeIn: 0.0,
    gasVolumeOut: 0.0,
    data: [] as Message[],
    cmd: [] as Message[],
    componentIds: ['sm', 'fm1', 'fm2', 'm1', 'm2', 'web'],
    wsConnected: false
  }),
  getters: {
    dataQueue: state => state.data,
    cmdQueue: state => state.cmd,
    latestData: state => state.data.length == 0 ? {} : state.data[state.data.length-1],
    latestCmd: state => state.cmd.length == 0 ? {} : state.cmd[state.cmd.length-1],
    components: state => state.componentIds,
    latestValuesForComponents: (state) => {
      const values: LatestData = {}

      state.componentIds.forEach(c => {
        values[c] = {
          data: findLatestForComponent(state.data, c),
          cmd: findLatestForComponent(state.cmd, c)
        }
      })
      return values
    },
    connected: state => state.wsConnected
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
    },
    setWsConnected(connected: boolean) {
      this.wsConnected = connected
    }
  },
})
