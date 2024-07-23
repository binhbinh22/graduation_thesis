import React, { useEffect, useState } from 'react';
import axios from 'axios';

const DialogflowHandler = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  useEffect(() => {
    sendMessageToDialogflow('Hello!');
  }, []);

  const sendMessageToDialogflow = async (text) => {
    const projectId = 'YOUR_PROJECT_ID'; // Thay thế bằng ID dự án của bạn
    const sessionId = '1234567890'; // Để mỗi lần tạo session mới, bạn có thể sử dụng một session ID ngẫu nhiên hoặc theo logic của bạn
    const languageCode = 'en'; // Ngôn ngữ của bạn, ví dụ: en, vi, ...

    try {
      const response = await axios.post(
        `https://dialogflow.googleapis.com/v2/projects/${projectId}/agent/sessions/${sessionId}:detectIntent`,
        {
          queryInput: {
            text: {
              text: text,
              languageCode: languageCode,
            },
          },
        },
        {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${process.env.REACT_APP_DIALOGFLOW_ACCESS_TOKEN}`, // Thay thế bằng access token của bạn
          },
        }
      );

      const { fulfillmentText } = response.data.queryResult;

      if (fulfillmentText) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: fulfillmentText, sender: 'bot' },
        ]);
      }
    } catch (error) {
      console.error('Error querying Dialogflow:', error);
    }
  };

  const handleUserMessage = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setMessages((prevMessages) => [...prevMessages, { text: input, sender: 'user' }]);
    sendMessageToDialogflow(input);
    setInput('');
  };

  return (
    <div>
      <div>
        {messages.map((message, index) => (
          <div key={index}>
            <span>{message.sender === 'bot' ? 'Bot: ' : 'You: '}</span>
            <span>{message.text}</span>
          </div>
        ))}
      </div>
      <form onSubmit={handleUserMessage}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default DialogflowHandler;

// import React, { useEffect, useState } from 'react';
// import Chatbot from 'react-chatbot-kit';
// import 'react-chatbot-kit/build/main.css';
// import { ApiAiClient } from 'api-ai-javascript';
// import config from './chatbotConfig'; // Import config from chatbotConfig.js
// import MessageParser from './MessageParser'; // Assuming MessageParser is correctly defined
// import ActionProvider from './ActionProvider'; // Assuming ActionProvider is correctly defined
// import { createChatBotMessage } from 'react-chatbot-kit'; // Import createChatBotMessage

// const DialogflowHandler = () => {
//   const [client, setClient] = useState(null);
//   const [state, setState] = useState({ messages: [] }); // Initialize state for messages

//   useEffect(() => {
//     const apiAiClient = new ApiAiClient({ accessToken: 'ya29.c.c0ASRK0GbpYqwS16ICFBvVz2lhk9SisH6A04sInges0t9kWyJPxWhcssgtmNHkrM8CflrdVvaXUSA4ogPVGRntFGnwG5zWce0uiGO7-pOwn9CdZbz1c80KxHVrSgkjFn_EvdrFgMCpo4xUq2zXOuen7-wAoxvqEDJpwCc9tp8YRKddEj8FonIFNjQ4JNJSanZAK08vMuE8rOvpXX397gUurpTwCV26EK7aOFi8le1HPYlxdX3VntdleZVuv6PmRFuBMEtTfo3witRI4XnD2Kjf-uqltl6z6bGIc0PRTHPNzVzRWMT8xu9YxlyL1wlQzcsZL2zSzW-Z3VOV_zNdGzp0y8FmErcHbtqrYEXF0uzuHMUtMXV1R4T3tgVXjE2_2oXQoWo1KAL399Phv17BMXdMb3k7YblRzS8JJ6xJwg5Y_W-iYmz9yd1qV9Yqxbi9ftMaqMF4F08WhcycS5duza3ilM-if8kj6eMZ4xucjjOdhZcycw04wicewp0idMijtWOXQQfaI-6eXfBmxkUZZevSJRxqBtjeUa6eedrYWvmnrkhexlB_Z6pd69r-JpMYx9k1QMUWM0X8-fgmz18ed4VoRQe0owsVs80WhqQWQQb2b0OgwW37Scf_fk8XBi_YV3a8WWiid6S4xqwboZsiFp-hmgpbkqcdh4OpiilomY-qqqYc6MUMBc_0FgyQYVrmIJspypm0jk_oe9Z9jlZ7Rbmho8o5f_oF98--xbXl0kI4rqa7YQ39p1XJ0bJivFIRbFbbzm7ythFQ46rygQe0X2vm92-ddZn6tFoQu37dlsyoMIj4b-IhwsjgJZ86dXrdsujp7UxoujyooeFS2_ptS-SYRbIcm376vrZf6b50smFFX43aQWzp-7nFJpfFgQ5e7OM9qiyhc2pb-YttyB3YSY15zORtUaUxure4oVuyX9lmodtJqit1BRtnfO93r_eWn55nXjW-0puadIh7I4cYbwi9Q7b6bY6nbq4fvl5M2cdQ1ytruowIq2sfj-r' });
//     setClient(apiAiClient);
//   }, []);

//   const handleUserMessage = async (message) => {
//     if (client) {
//       const response = await client.textRequest(message);
//       const botMessage = {
//         type: 'bot',
//         message: response.result.fulfillment.speech,
//       };
//       return botMessage;
//     }
//   };

//   return (
//     <div>
//       <Chatbot
//         config={config} // Pass config from chatbotConfig.js
//         messageParser={MessageParser} // Assuming MessageParser is correctly defined
//         actionProvider={new ActionProvider(createChatBotMessage, setState)} // Assuming setState is defined
//       />
//     </div>
//   );
// };

// export default DialogflowHandler;


// // const apiAiClient = new ApiAiClient({ accessToken: 'ya29.c.c0ASRK0GbpYqwS16ICFBvVz2lhk9SisH6A04sInges0t9kWyJPxWhcssgtmNHkrM8CflrdVvaXUSA4ogPVGRntFGnwG5zWce0uiGO7-pOwn9CdZbz1c80KxHVrSgkjFn_EvdrFgMCpo4xUq2zXOuen7-wAoxvqEDJpwCc9tp8YRKddEj8FonIFNjQ4JNJSanZAK08vMuE8rOvpXX397gUurpTwCV26EK7aOFi8le1HPYlxdX3VntdleZVuv6PmRFuBMEtTfo3witRI4XnD2Kjf-uqltl6z6bGIc0PRTHPNzVzRWMT8xu9YxlyL1wlQzcsZL2zSzW-Z3VOV_zNdGzp0y8FmErcHbtqrYEXF0uzuHMUtMXV1R4T3tgVXjE2_2oXQoWo1KAL399Phv17BMXdMb3k7YblRzS8JJ6xJwg5Y_W-iYmz9yd1qV9Yqxbi9ftMaqMF4F08WhcycS5duza3ilM-if8kj6eMZ4xucjjOdhZcycw04wicewp0idMijtWOXQQfaI-6eXfBmxkUZZevSJRxqBtjeUa6eedrYWvmnrkhexlB_Z6pd69r-JpMYx9k1QMUWM0X8-fgmz18ed4VoRQe0owsVs80WhqQWQQb2b0OgwW37Scf_fk8XBi_YV3a8WWiid6S4xqwboZsiFp-hmgpbkqcdh4OpiilomY-qqqYc6MUMBc_0FgyQYVrmIJspypm0jk_oe9Z9jlZ7Rbmho8o5f_oF98--xbXl0kI4rqa7YQ39p1XJ0bJivFIRbFbbzm7ythFQ46rygQe0X2vm92-ddZn6tFoQu37dlsyoMIj4b-IhwsjgJZ86dXrdsujp7UxoujyooeFS2_ptS-SYRbIcm376vrZf6b50smFFX43aQWzp-7nFJpfFgQ5e7OM9qiyhc2pb-YttyB3YSY15zORtUaUxure4oVuyX9lmodtJqit1BRtnfO93r_eWn55nXjW-0puadIh7I4cYbwi9Q7b6bY6nbq4fvl5M2cdQ1ytruowIq2sfj-r' });


// // import React, { useEffect, useState } from 'react';
// // import { useChatbot } from 'react-chatbot-kit';
// // import { ApiAiClient } from 'api-ai-javascript';

// // const DialogflowHandler = () => {
// //   const [client, setClient] = useState(null);
// //   const { createChatBotMessage, addMessageToBotState } = useChatbot();

// //   useEffect(() => {
// //     const apiAiClient = new ApiAiClient({ accessToken: 'ya29.c.c0ASRK0GbpYqwS16ICFBvVz2lhk9SisH6A04sInges0t9kWyJPxWhcssgtmNHkrM8CflrdVvaXUSA4ogPVGRntFGnwG5zWce0uiGO7-pOwn9CdZbz1c80KxHVrSgkjFn_EvdrFgMCpo4xUq2zXOuen7-wAoxvqEDJpwCc9tp8YRKddEj8FonIFNjQ4JNJSanZAK08vMuE8rOvpXX397gUurpTwCV26EK7aOFi8le1HPYlxdX3VntdleZVuv6PmRFuBMEtTfo3witRI4XnD2Kjf-uqltl6z6bGIc0PRTHPNzVzRWMT8xu9YxlyL1wlQzcsZL2zSzW-Z3VOV_zNdGzp0y8FmErcHbtqrYEXF0uzuHMUtMXV1R4T3tgVXjE2_2oXQoWo1KAL399Phv17BMXdMb3k7YblRzS8JJ6xJwg5Y_W-iYmz9yd1qV9Yqxbi9ftMaqMF4F08WhcycS5duza3ilM-if8kj6eMZ4xucjjOdhZcycw04wicewp0idMijtWOXQQfaI-6eXfBmxkUZZevSJRxqBtjeUa6eedrYWvmnrkhexlB_Z6pd69r-JpMYx9k1QMUWM0X8-fgmz18ed4VoRQe0owsVs80WhqQWQQb2b0OgwW37Scf_fk8XBi_YV3a8WWiid6S4xqwboZsiFp-hmgpbkqcdh4OpiilomY-qqqYc6MUMBc_0FgyQYVrmIJspypm0jk_oe9Z9jlZ7Rbmho8o5f_oF98--xbXl0kI4rqa7YQ39p1XJ0bJivFIRbFbbzm7ythFQ46rygQe0X2vm92-ddZn6tFoQu37dlsyoMIj4b-IhwsjgJZ86dXrdsujp7UxoujyooeFS2_ptS-SYRbIcm376vrZf6b50smFFX43aQWzp-7nFJpfFgQ5e7OM9qiyhc2pb-YttyB3YSY15zORtUaUxure4oVuyX9lmodtJqit1BRtnfO93r_eWn55nXjW-0puadIh7I4cYbwi9Q7b6bY6nbq4fvl5M2cdQ1ytruowIq2sfj-r'});
// //     setClient(apiAiClient);
// //   }, []);

// //   const handleUserMessage = async (message) => {
// //     if (client) {
// //       const response = await client.textRequest(message);
// //       const botMessage = createChatBotMessage(response.result.fulfillment.speech);
// //       addMessageToBotState(botMessage);
// //     }
// //   };

// //   return (
// //     <div>
// //       <input type="text" placeholder="Ask something..." onKeyDown={(e) => {
// //         if (e.key === 'Enter') {
// //           handleUserMessage(e.target.value);
// //           e.target.value = '';
// //         }
// //       }} />
// //     </div>
// //   );
// // };

// // export default DialogflowHandler;
// // import React from 'react';
// // import Chatbot from 'react-chatbot-kit';
// // import 'react-chatbot-kit/build/main.css';

// // import config from './config';
// // import MessageParser from './MessageParser';
// // import ActionProvider from './ActionProvider';

// // const DialogflowHandler = () => {
// //   return (
// //     <div>
// //       <Chatbot
// //         config={config}
// //         messageParser={MessageParser}
// //         actionProvider={ActionProvider}
// //       />
// //     </div>
// //   );
// // };

// // export default DialogflowHandler;
