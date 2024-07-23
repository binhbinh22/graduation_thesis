import { createChatBotMessage } from 'react-chatbot-kit';
import ChatbotAvatar from './ChatbotAvatar';
import ChatbotOptions from './ChatbotOptions';
import DialogflowHandler from './DialogflowHandler';

const config = {
  botName: "NewsBot",
  initialMessages: [createChatBotMessage("Hello! How can I help you today?")],
  customComponents: {
    botAvatar: (props) => <ChatbotAvatar {...props} />,
  },
  customStyles: {
    botMessageBox: {
      backgroundColor: "#376B7E",
    },
    chatButton: {
      backgroundColor: "#5ccc9d",
    },
  },
  state: {},
  widgets: [
    {
      widgetName: "dialogflowHandler",
      widgetFunc: (props) => <DialogflowHandler {...props} />,
    },
    {
      widgetName: "chatbotOptions",
      widgetFunc: (props) => <ChatbotOptions {...props} />,
    },
  ],
};

export default config;
