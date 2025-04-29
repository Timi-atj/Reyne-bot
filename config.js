// config.js
import { Platform } from 'react-native';

const LOCAL_IP = "192.168.0.115"; // ⚡ your computer's IP without port
const USE_DEPLOYED_BACKEND = false; // ❗ Set to false for local testing

export const API_BASE_URL = USE_DEPLOYED_BACKEND
  ? "https://reyne-bot.onrender.com"
  : Platform.OS === 'web'
    ? "http://localhost:8000"
    : `http://${LOCAL_IP}:8000`;
