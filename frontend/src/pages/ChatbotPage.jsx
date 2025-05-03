import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import luffyImage from "../assets/luffy.png";

export default function ChatbotPage() {
  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
  const navigate = useNavigate();

  const isValid = name.trim() && age.trim();

  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth < 768);
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

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
      navigate("/ace", { state: { name, age } });
    }
  };

  return (
    <div style={{
      position: "relative",
      height: "100vh",
      width: "100vw",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      overflow: "hidden",
      fontFamily: "Calibri, sans-serif",
      backgroundColor: "#ffffff"
    }}>
      {/* Bubble Background */}
      <div className="bubble-background"></div>
      {Array.from({ length: 20 }).map((_, i) => (
        <div
          key={i}
          className="bubble"
          style={{
            position: "absolute",
            bottom: 0,
            width: "20px",
            height: "20px",
            backgroundColor: "rgba(173, 216, 230, 0.6)",
            borderRadius: "50%",
            left: `${Math.random() * 100}vw`,
            animation: `rise ${6 + Math.random() * 4}s linear infinite`,
            animationDelay: `${Math.random() * 5}s`,
            zIndex: 0,
          }}
        />
      ))}

      <main style={{
        zIndex: 1,
        width: "100%",
        maxWidth: "500px",
        padding: "2rem",
        borderRadius: "12px",
        backgroundColor: "rgba(255, 255, 255, 0.95)",
        boxShadow: "0 0 10px rgba(0, 0, 0, 0.05)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center"
      }}>
        <div style={{ marginBottom: "1rem" }}>
          <img
            src={luffyImage}
            alt="Zoe Assistant"
            style={{ width: "160px", height: "160px" }}
          />
        </div>
        <h1 style={{ fontSize: isMobile ? "1.5rem" : "2rem", marginBottom: "0.5rem" }}>
          Hey there! I'm Zoe 👋
        </h1>
        <h2 style={{ fontSize: isMobile ? "1rem" : "1.2rem", marginBottom: "1.5rem", color: "#555" }}>
          Tell me a bit about yourself and let's get started!
        </h2>

        <form
          onSubmit={handleSubmit}
          style={{
            width: "100%",
            display: "flex",
            flexDirection: "column",
            gap: "1.25rem",
            alignItems: "center"
          }}
        >
          <div style={{ width: "100%" }}>
            <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "600" }}>
              Name
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              placeholder="Enter your name"
              style={{
                width: "100%",
                padding: "0.75rem",
                borderRadius: "6px",
                border: "1px solid #ccc",
                fontFamily: "inherit"
              }}
            />
          </div>
          <div style={{ width: "100%" }}>
            <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "600" }}>
              Age
            </label>
            <input
              type="number"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              required
              placeholder="Enter your age"
              style={{
                width: "100%",
                padding: "0.75rem",
                borderRadius: "6px",
                border: "1px solid #ccc",
                fontFamily: "inherit"
              }}
            />
          </div>
          <button
            type="submit"
            style={{
              padding: "0.50rem",
              width: "60%",
              backgroundColor: isValid ? "#2ecc71" : "#e74c3c",
              color: "#fff",
              border: "none",
              borderRadius: "6px",
              fontWeight: "600",
              fontSize: "1rem",
              cursor: "pointer"
            }}
          >
            Proceed to Questionnaire
          </button>
        </form>
      </main>
    </div>
  );
}
