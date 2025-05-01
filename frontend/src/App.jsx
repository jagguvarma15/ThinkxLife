import { useState } from "react";
import Chatbot from "./components/Chatbot";
import thinkLogo from "./assets/think-logo.png";

export default function App() {
  const [showChat, setShowChat] = useState(false);
  const [name, setName] = useState("");
  const [age, setAge] = useState("");

  const isValid = name.trim() && age.trim();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isValid) {
      try {
        await fetch("http://localhost:5001/user", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name, age }),
        });
      } catch (error) {
        console.error("Failed to register user:", error);
      }
      setShowChat(true);
    }
  };

  if (showChat) {
    return <Chatbot name={name} age={age} />;
  }

  return (
    <div style={{ display: 'flex', height: '100vh', width: '100vw', overflow: 'hidden' }}>
      {/* Left Sidebar */}
      <div style={{ width: "15%", backgroundColor: '#f79d51', padding: "1rem", color: "#000" }}>
        <h3>🎨 Art</h3>
        <ul style={{ fontSize: "0.9rem" }}>
          <li>Gallery Exhibit</li>
          <li>Children's Mural</li>
          <li>Local Artist Collab</li>
        </ul>
      </div>

      {/* Main Content */}
      <div
        style={{
          flex: 1,
          padding: "2rem",
          fontFamily: "Arial, sans-serif",
          backgroundColor: "#fff",
          boxSizing: "border-box",
          display: "flex",
          flexDirection: "column",
          justifyContent: "flex-start",
          alignItems: "center",
        }}
      >
        {/* Logo and Brand Name */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "1rem",
            marginBottom: "2rem",
            width: "150%",
            justifyContent: "center",
          }}
        >
          <img src={thinkLogo} alt="Think Round Logo" style={{ height: "150px" }} />
          <div style={{ display: "flex", flexDirection: "column" }}>
            <h1 style={{ fontSize: "3.5rem", fontWeight: "900", margin: 0 }}>
              Think Round, Inc.
            </h1>
            <p style={{ fontSize: "1.5rem", color: "#6c5ce7", margin: 0 }}>
              Earth is home, Humans are family.
            </p>
          </div>
        </div>

        {/* Welcome Heading */}
        <h2 style={{ fontWeight: "600", fontSize: "1.2rem", marginBottom: "1.5rem" }}>
          Let's get to know you!
        </h2>

        {/* Form */}
        <form
          onSubmit={handleSubmit}
          style={{
            width: "100%",
            maxWidth: "400px",
            display: "flex",
            flexDirection: "column",
            gap: "1.5rem",
            alignItems: "center",
          }}
        >
          <div style={{ width: "100%" }}>
            <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "500" }}>
              What is your name?
            </label>
            <input
              type="text"
              placeholder="Enter your First Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              style={{
                width: "100%",
                padding: "0.75rem",
                borderRadius: "8px",
                border: "1px solid #ccc",
                backgroundColor: "#f5f7fa",
                fontSize: "1rem",
              }}
            />
          </div>

          <div style={{ width: "100%" }}>
            <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "500" }}>
              What is your age?
            </label>
            <input
              type="number"
              placeholder="Enter your age"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              required
              style={{
                width: "100%",
                padding: "0.75rem",
                borderRadius: "8px",
                border: "1px solid #ccc",
                backgroundColor: "#f5f7fa",
                fontSize: "1rem",
              }}
            />
          </div>

          <button
            type="submit"
            style={{
              width: "100%",
              padding: "0.75rem",
              backgroundColor: isValid ? "#2ecc71" : "#e74c3c",
              color: "white",
              border: "none",
              borderRadius: "8px",
              fontWeight: "600",
              fontSize: "1rem",
              cursor: "pointer",
            }}
          >
            Submit
          </button>
        </form>
      </div>

      {/* Right Sidebar */}
      <div style={{ width: "15%", backgroundColor: '#67c1f5', padding: "1rem", color: "#000" }}>
        <h3>📅 Events</h3>
        <ul style={{ fontSize: "0.9rem" }}>
          <li>ACE Workshop</li>
          <li>Community Garden Day</li>
          <li>Storytelling Circle</li>
        </ul>

        <h3 style={{ marginTop: "2rem" }}>🚀 Projects</h3>
        <ul style={{ fontSize: "0.9rem" }}>
          <li>EarthCare Initiative</li>
          <li>Mindful Mondays</li>
          <li>Art for All</li>
        </ul>
      </div>
    </div>
  );
}
