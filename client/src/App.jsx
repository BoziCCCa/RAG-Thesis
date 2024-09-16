import "./App.css";
import MainPage from "./pages/MainPage";
import { Route, Routes } from "react-router-dom";
import Layout from "./pages/Layout";
import "./index.css";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<MainPage />} />
      </Route>
    </Routes>
  );
}

export default App;
