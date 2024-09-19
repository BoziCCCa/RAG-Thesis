import React from "react";

const UserMessage = ({ text }) => {
  return (
    <div className="flex flex-row ml-16">
      <div className="message-container">
        <div className="user-message">{text}</div>
      </div>
      <div className="flex flex-col-reverse pr-2 pl-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="40"
          width="40"
          viewBox="0 0 448 512"
        >
          {/* <!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.-->*/}
          <path
            fill="#ffffff"
            d="M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512l388.6 0c16.4 0 29.7-13.3 29.7-29.7C448 383.8 368.2 304 269.7 304l-91.4 0z"
          />
        </svg>
      </div>
    </div>
  );
};

export default UserMessage;
