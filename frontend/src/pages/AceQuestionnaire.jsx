import { useLocation } from "react-router-dom";
import { useState } from "react";

export default function ACEQuestionnaire() {
  const location = useLocation();
  const { name, age } = location.state || {};
  const questions = [
    "Did a parent or other adult in the household often swear at you, insult you, or humiliate you?",
    "Did a parent or other adult in the household often push, grab, slap, or throw something at you?",
    "Did you often feel that no one in your family loved you or thought you were important or special?",
    "Did you often feel that you didn't have enough to eat, had to wear dirty clothes, or had no one to protect you?",
    "Were your parents ever separated or divorced?",
    "Was your mother or stepmother often pushed, grabbed, slapped, or had something thrown at her?",
    "Did you live with anyone who was a problem drinker or alcoholic or who used street drugs?",
    "Was a household member depressed or mentally ill or did a household member attempt suicide?",
    "Did a household member go to prison?",
    "Did you often feel alone or unsupported as a child?"
  ];

  const [currentIndex, setCurrentIndex] = useState(0);
  const [score, setScore] = useState(0);
  const [responses, setResponses] = useState([]);
  const [submitted, setSubmitted] = useState(false);

  const handleResponse = (value) => {
    const updatedResponses = [...responses, value];
    const updatedScore = score + value;
    setResponses(updatedResponses);
    setScore(updatedScore);
  
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      setSubmitted(true);
      
      // Log to backend after last question
      fetch("http://localhost:5001/ace-results", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          age,
          responses: updatedResponses,
          score: updatedScore.toFixed(2),
        }),
      })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to log ACE data.");
        return res.json();
      })
      .then((data) => console.log("Logged ACE data:", data))
      .catch((err) => console.error(err));
    }
  };
  

  const neumorphicCard = {
    padding: "2rem",
    borderRadius: "20px",
    background: "#e0e0e0",
    boxShadow: "8px 8px 16px #bebebe, -8px -8px 16px #ffffff",
    maxWidth: "700px",
    width: "90%",
    textAlign: "center",
  };

  const buttonStyle = {
    padding: "0.75rem 1.5rem",
    fontSize: "1rem",
    borderRadius: "10px",
    border: "none",
    margin: "0 0.5rem",
    backgroundColor: "#f0f0f0",
    boxShadow: "4px 4px 10px #bebebe, -4px -4px 10px #ffffff",
    cursor: "pointer",
    transition: "all 0.2s ease-in-out",
  };

  return (
    <div style={{
      height: "100vh",
      width: "100vw",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      fontFamily: "Calibri, sans-serif",
      backgroundColor: "#e0e0e0",
    }}>
      <main style={neumorphicCard}>
        {submitted ? (
          <>
            <h1>Thank you, {name}!</h1>
            <p>Your ACE Questionnaire is complete.</p>
            <h2>Your ACE Score is <strong>{score.toFixed(2)} / 10</strong></h2>
          </>
        ) : (
          <>
            <h1>ACE Questionnaire</h1>
            <p><strong>Question {currentIndex + 1} of {questions.length}</strong></p>
            <p style={{ margin: "1.5rem 0" }}>{questions[currentIndex]}</p>
            <div style={{ display: "flex", justifyContent: "center", flexWrap: "wrap" }}>
              <button onClick={() => handleResponse(1)} style={buttonStyle}>Yes</button>
              <button onClick={() => handleResponse(0)} style={buttonStyle}>No</button>
              <button onClick={() => handleResponse(0.25)} style={buttonStyle}>Skip</button>
            </div>
          </>
        )}
      </main>
    </div>
  );
}
