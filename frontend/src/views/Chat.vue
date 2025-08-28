<template>
  <div class="chat-container">
    <div class="sidebar">
      <h3>Tools</h3>
      <div class="tool-panel">
        <h4>VNC Viewer</h4>
        <div ref="vncScreen" class="vnc-screen"></div>
        <Button label="Connect VNC" @click="connectVnc" />
      </div>
    </div>
    <div class="main-content">
      <div class="chat-window">
        <div v-for="(message, index) in messages" :key="index" class="message" :class="message.role">
          <p><strong>{{ message.role }}:</strong> {{ message.content }}</p>
        </div>
      </div>
      <div class="chat-input">
        <form @submit.prevent="sendMessage">
          <InputText v-model="newMessage" placeholder="Type a message..." />
          <Button label="Send" type="submit" />
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import RFB from '@novnc/novnc/core/rfb';

const messages = ref([]);
const newMessage = ref('');
const authStore = useAuthStore();
let eventSource = null;
let sessionId = null;
const vncScreen = ref(null);
let rfb = null;

onMounted(async () => {
  // 1. Create a new session on component mount
  try {
    const response = await axios.post('/api/sessions/');
    sessionId = response.data.id;
    messages.value = response.data.conversation.messages;
    connectToSse();
  } catch (error) {
    console.error("Failed to create session:", error);
  }
});

const connectToSse = () => {
  if (!sessionId || !authStore.token) return;
  const url = `/api/sessions/${sessionId}/conversation?token=${authStore.token}`;
  eventSource = new EventSource(url);

  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    handleSseEvent(data);
  };

  eventSource.onerror = (error) => {
    console.error("SSE Error:", error);
    eventSource.close();
  };
};

const handleSseEvent = (event) => {
  switch (event.event) {
    case 'thought':
      messages.value.push({ role: 'assistant', content: `Thinking: ${event.data}` });
      break;
    case 'tool_call':
      messages.value.push({ role: 'assistant', content: `Using tool: ${event.data.tool}` });
      break;
    case 'message_chunk':
      const lastMessage = messages.value[messages.value.length - 1];
      if (lastMessage && lastMessage.role === 'assistant') {
        lastMessage.content += event.data;
      } else {
        messages.value.push({ role: 'assistant', content: event.data });
      }
      break;
    case 'end':
      eventSource.close();
      break;
  }
};

const sendMessage = async () => {
  if (!newMessage.value.trim() || !sessionId) return;

  const message = {
    role: 'user',
    content: newMessage.value,
  };
  messages.value.push(message);

  // Re-establish SSE connection for the new conversation turn
  connectToSse();

  try {
    await axios.post(`/api/sessions/${sessionId}/conversation`, message);
  } catch (error) {
    console.error("Failed to send message:", error);
  }

  newMessage.value = '';
};

const connectVnc = async () => {
  if (!sessionId) return;
  try {
    // 1. Get a new VNC ticket
    const response = await axios.get(`/vnc/${sessionId}/vnc-ticket`);
    const ticket = response.data.ticket;

    // 2. Construct the WebSocket URL
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    const url = `${protocol}//${host}/ws/vnc/${sessionId}?ticket=${ticket}`;

    // 3. Connect noVNC
    if (rfb) {
      rfb.disconnect();
    }
    rfb = new RFB(vncScreen.value, url, {
      credentials: { password: '' }, // We don't use VNC password, auth is handled by ticket
    });

  } catch (error) {
    console.error("Failed to connect to VNC:", error);
  }
};
</script>

<style scoped>
.vnc-screen {
  width: 100%;
  height: 200px; /* Adjust as needed */
  background-color: #000;
  border: 1px solid #ccc;
}
.chat-container {
  display: flex;
  height: 100vh;
}
.sidebar {
  width: 250px;
  background-color: #f0f0f0;
  padding: 1rem;
}
.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}
.chat-window {
  flex-grow: 1;
  padding: 1rem;
  overflow-y: auto;
}
.message {
  margin-bottom: 1rem;
}
.message.user {
  text-align: right;
}
.chat-input {
  padding: 1rem;
  border-top: 1px solid #ccc;
}
</style>
