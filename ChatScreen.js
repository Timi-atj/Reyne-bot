import React, { useState } from 'react';
import { View, TextInput, Button, Text, FlatList, StyleSheet } from 'react-native';
import axios from 'axios';
import { API_BASE_URL } from './config'; // 👈 import the base URL

const ChatScreen = () => {
  const [userMessage, setUserMessage] = useState('');
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!userMessage.trim()) return;

    const userMsg = {
      id: Math.random().toString(),
      text: userMessage,
      sender: 'user',
    };

    // Add user message
    setMessages(prev => [...prev, userMsg]);

    try {
   const response = await axios.post(`${API_BASE_URL}/chat`, { message: userMessage });

      const aiReply = response.data.reply || "Sorry, I couldn't get a response from the AI.";

      const aiMsg = {
        id: Math.random().toString(),
        text: aiReply,
        sender: 'ai',
      };

      setMessages(prev => [...prev, aiMsg]);
    } catch (error) {
      console.error('Error sending message:', error);

      const errorMsg = {
        id: Math.random().toString(),
        text: '❌ Error connecting to the server.',
        sender: 'ai',
      };

      setMessages(prev => [...prev, errorMsg]);
    }

    setUserMessage('');
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={messages}
        renderItem={({ item }) => (
          <View style={item.sender === 'user' ? styles.userMessage : styles.aiMessage}>
            <Text>{item.text}</Text>
          </View>
        )}
        keyExtractor={item => item.id}
        style={styles.messagesContainer}
      />
      <TextInput
        style={styles.input}
        value={userMessage}
        onChangeText={setUserMessage}
        placeholder="Ask me anything..."
      />
      <Button title="Send" onPress={sendMessage} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'flex-end',
    padding: 10,
  },
  messagesContainer: {
    flex: 1,
    marginBottom: 20,
  },
  userMessage: {
    alignSelf: 'flex-end',
    backgroundColor: '#e1ffc7',
    padding: 10,
    marginVertical: 5,
    borderRadius: 10,
  },
  aiMessage: {
    alignSelf: 'flex-start',
    backgroundColor: '#f0f0f0',
    padding: 10,
    marginVertical: 5,
    borderRadius: 10,
  },
  input: {
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
    padding: 10,
    marginBottom: 10,
  },
});

export default ChatScreen;