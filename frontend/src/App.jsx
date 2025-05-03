import { Routes, Route } from "react-router-dom";
import About from "./pages/About";
import ChatbotPage from "./pages/ChatbotPage";
import SignIn from "./pages/SignIn";
import AceQuestionnaire from "./pages/AceQuestionnaire";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<About />} />
      <Route path="/chatbot" element={<ChatbotPage />} />
      <Route path="/signin" element={<SignIn />} />
      <Route path="/ace" element={<AceQuestionnaire />} />

    </Routes>
  );
}
