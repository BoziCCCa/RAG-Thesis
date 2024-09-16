import React, { useState, useEffect } from "react";
import LoadingDots from "./LoadingDots";

const BotMessage = ({ fetchMessage, question }) => {
  const [isLoading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const loadMessage = async () => {
      const msg = await fetchMessage(question);
      setLoading(false);
      setMessage(msg);
    };
    loadMessage();
  }, [fetchMessage]);

  return (
    <div className="message-container">
      <div className="bot-message">{isLoading ? <LoadingDots /> : message}</div>
    </div>
  );
};

export default BotMessage;
