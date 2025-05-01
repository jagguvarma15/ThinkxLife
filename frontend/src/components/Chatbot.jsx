import { useState } from "react";

export default function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages([...messages, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:5001/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();
      const botMessage = { sender: "zoe", text: data.response };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: "zoe", text: "Error: Could not reach backend." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div style={{ border: "1px solid #ccc", padding: "1rem", borderRadius: "8px" }}>
      <div style={{ height: "300px", overflowY: "auto", marginBottom: "1rem" }}>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              textAlign: msg.sender === "user" ? "right" : "left",
              marginBottom: "8px",
            }}
          >
            <span
              style={{
                display: "inline-block",
                background: msg.sender === "user" ? "#d1e7ff" : "#f1f1f1",
                padding: "8px 12px",
                borderRadius: "12px",
              }}
            >
              {msg.text}
            </span>
          </div>
        ))}
        {loading && <div style={{ fontSize: "0.9rem", color: "#888" }}>Zoe is thinking...</div>}
      </div>
      <div style={{ display: "flex" }}>
        <input
          style={{ flex: 1, padding: "0.5rem", marginRight: "0.5rem" }}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}
