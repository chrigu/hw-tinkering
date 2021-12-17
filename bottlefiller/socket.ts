import {Message} from './src/interfaces'
import set from "@vue/composition-api";

const connection: WebSocket = new WebSocket('ws://localhost:8000/ws/23')

export const setupSocket = (update: any, setWs: any) => {
      connection.onmessage = (event) => {
        const message: Message = JSON.parse(event.data)
        console.log(message)
        update(message)
      }

      connection.onopen = () => {
          setWs(true)
      }

      connection.onclose = () => {
        setWs(false)
      }
      console.log('WS Socket setup')

}

export const send = (message: string) => {
  connection.send(message)
}
