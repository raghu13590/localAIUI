<template>
  <div class="container">
    <h1>Qwen AI Assistant</h1>

    <div class="chat-container">
      <div class="messages" ref="messagesContainer">
        <div v-for="(message, index) in messages" :key="index"
             :class="['message', message.type]">
          <p>{{ message.text }}</p>
        </div>
      </div>
    </div>

    <div class="input-container">
      <textarea
        v-model="userInput"
        @keyup.enter="sendMessage"
        placeholder="Ask a question..."
        rows="3"
      ></textarea>
      <button @click="sendMessage" :disabled="isLoading">
        {{ isLoading ? 'Processing...' : 'Send' }}
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      userInput: '',
      messages: [],
      isLoading: false
    }
  },
  methods: {
    async sendMessage(event) {
      if (event.shiftKey && event.key === 'Enter') return
      if (event.key === 'Enter') event.preventDefault()

      const userMessage = this.userInput.trim()
      if (!userMessage || this.isLoading) return

      // Add user message to chat
      this.messages.push({
        type: 'user',
        text: userMessage
      })

      this.isLoading = true
      this.userInput = ''

      try {
        const response = await axios.post('http://localhost:8081/query', {
          question: userMessage
        })

        // Add AI response to chat
        this.messages.push({
          type: 'assistant',
          text: response.data.response
        })
      } catch (error) {
        this.messages.push({
          type: 'error',
          text: 'Sorry, there was an error processing your request.'
        })
        console.error('Error:', error)
      } finally {
        this.isLoading = false
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      }
    },
    scrollToBottom() {
      const container = this.$refs.messagesContainer
      container.scrollTop = container.scrollHeight
    }
  }
}
</script>

<style>
.container {
  max-width: 100%;
  margin: 10px;
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  text-align: center;
  color: #333;
}

.chat-container {
  height: calc(100vh - 200px);
  margin-bottom: 20px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.messages {
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px;
}

.message {
  margin-bottom: 15px;
  padding: 10px 15px;
  border-radius: 8px;
  max-width: 80%;
}

.message.user {
  background-color: #007bff;
  color: white;
  margin-left: auto;
}

.message.assistant {
  background-color: #f1f1f1;
  color: #333;
}

.message.error {
  background-color: #dc3545;
  color: white;
  margin-left: auto;
}

.input-container {
  display: flex;
  gap: 10px;
}

textarea {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: none;
  font-family: inherit;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  min-width: 100px;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}
</style>