import {Message} from './src/interfaces'

const connection: WebSocket = new WebSocket('ws://localhost:8000/ws/23')

export const setupSocket = (update: any) => {
      connection.onmessage = (event) => {
        const message: Message = JSON.parse(event.data)
        console.log(message)
        update(message)

      }
      console.log('socket setup')

}

export const send = (message: string) => {
  connection.send(message)
}
