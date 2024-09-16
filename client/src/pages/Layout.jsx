{
  /* <div className="min-h-screen flex items-center justify-center">
      <header className="App-header">
        <h1>My Chatbot App</h1>
      </header>
      <MainPage className="MainPage" />
    </div> */
}
import React from "react";
import { Outlet } from "react-router-dom";
import Header from "./Header";

const Layout = () => {
  return (
    <div style={{ height: "100%" }} className="flex flex-col items-center">
      <Header />
      <Outlet />
    </div>
  );
};

export default Layout;
