class MessageParser {
    constructor(actionProvider) {
      this.actionProvider = actionProvider;
    }
  
    parse(message) {
      const lowerCaseMessage = message.toLowerCase();
  
      if (lowerCaseMessage.includes("news")) {
        this.actionProvider.handleNews();
      } else {
        this.actionProvider.handleDefault();
      }
    }
  }
  
  export default MessageParser;
  