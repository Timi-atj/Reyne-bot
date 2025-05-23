import React from 'react';
import { SafeAreaView } from 'react-native';
import ChatScreen from './ChatScreen';  // Adjust if the file is in a different location

const App = () => {
  return (
    <SafeAreaView style={{ flex: 1 }}>
      <ChatScreen />
    </SafeAreaView>
  );
};

export default App;
