import React, { useState } from "react";
import Messages from "../components/Messages";
import MessageInput from "../components/MessageInput";
import UserMessage from "../components/UserMessage";
import ChatbotMessage from "../components/ChatbotMessage";
import axios from "axios";

const MainPage = () => {
  const [messages, setMessages] = useState([]);

  const handleSend = async (messageText) => {
    // Add the user's message to the messages list
    const userMessage = (
      <UserMessage key={messages.length} text={messageText} />
    );
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);

    // Add the bot's message to the messages list
    const botMessage = (
      <ChatbotMessage
        key={updatedMessages.length}
        fetchMessage={fetchMessage}
        question={messageText}
      />
    );
    setMessages([...updatedMessages, botMessage]);
  };

  const fetchMessage = async (question) => {
    const response = await axios.post("http://localhost:5000/ask-question", {
      question: question,
    });

    return response.data.answer;
  };

  return (
    <div className="chatbot">
      <Messages messages={messages} />
      <MessageInput handleSend={handleSend} />
    </div>
  );
};

export default MainPage;
