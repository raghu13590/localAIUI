<template>
  <div class="container">
    <div class="header">
      <h1>Ollama AI Assistant</h1>
    </div>
    <div class="model-selector">
      <label for="model-select">Select Model:</label>
      <select v-model="selectedModel" id="model-select" :disabled="loadingModels">
        <option v-for="model in availableModels" :key="model" :value="model">{{ model }}</option>
      </select>
      <label for="query-type">Query Type:</label>
      <select v-model="queryType" id="query-type">
        <option value="langchain">LangChain</option>
        <option value="direct">Direct LLM</option>
      </select>
      <button v-if="modelError" @click="fetchModels" class="retry-button">
        Retry
      </button>
    </div>
    <div class="chat-container">
      <div class="messages" ref="messagesContainer">
        <div v-for="(message, index) in messages" :key="index" :class="['message', message.type]">
          <div v-if="message.type === 'assistant'" class="message-header">{{ message.model }}</div>
          {{ message.text }}
        </div>
      </div>
      <div class="input-container">
        <textarea v-model="userInput" @keydown="handleKeyDown" @input="adjustTextareaHeight" placeholder="Type your message..."></textarea>
        <button @click="sendMessage" :disabled="isLoading">Send</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      queryType: 'langchain',
      userInput: '',
      messages: [],
      isLoading: false,
      availableModels: [],
      selectedModel: '',
      loadingModels: true,
      modelError: false,
    }
  },
  created() {
    this.fetchModels()
  },
  methods: {
    async fetchModels() {
      this.loadingModels = true
      this.modelError = false
      try {
        console.log('Fetching models...')
        const response = await axios.get('/api/models')
        console.log('Models response:', response.data)
        this.availableModels = response.data.models
        if (this.availableModels.length > 0) {
          this.selectedModel = this.availableModels[0]
        }
      } catch (error) {
        console.error('Error fetching models:', error)
        this.modelError = true
      } finally {
        this.loadingModels = false
      }
    },
    handleKeyDown(event) {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault()
        this.sendMessage()
      }
    },
    async sendMessage() {
      const userMessage = this.userInput.trim()
      if (!userMessage || this.isLoading) return

      // Add user message to chat
      this.messages.push({
        type: 'user',
        text: userMessage
      })

      this.isLoading = true
      this.userInput = ''

      const endpoint = this.queryType === 'langchain' ? '/api/query' : '/api/direct_query'
      try {
        const response = await axios.post(endpoint, {
          question: userMessage,
          model: this.selectedModel
        })

        // Add AI response to chat
        this.messages.push({
          type: 'assistant',
          text: response.data.response,
          model: this.selectedModel
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
    },
    adjustTextareaHeight(event) {
      const textarea = event.target
      textarea.style.height = 'auto'
      textarea.style.height = `${textarea.scrollHeight}px`
    }
  }
}
</script>

<style>
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 100%;
  margin: 0;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h1 {
  color: #333;
  margin: 0;
}

.model-selector {
  display: flex;
  align-items: center;
  gap: 10px;
}

.chat-container {
  flex-grow: 1;
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
  white-space: pre-wrap; /* Preserve whitespace and formatting */
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
  padding: 10px 0;
  margin-top: auto; /* Ensure the input container is at the bottom */
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

.model-selector select {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
  min-width: 200px;
}

.model-selector select:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.retry-button {
  padding: 8px 16px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.retry-button:hover {
  background-color: #c82333;
}

.message-header {
  font-size: 0.8em;
  color: #666;
  margin-bottom: 5px;
}
</style>