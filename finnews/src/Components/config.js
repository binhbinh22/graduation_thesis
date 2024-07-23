import { createChatBotMessage } from 'react-chatbot-kit';

const config = {
  botName: "FinnewsBot",
  initialMessages: [createChatBotMessage("Hi! How can I help you with the latest news?")],
};

export default config;
