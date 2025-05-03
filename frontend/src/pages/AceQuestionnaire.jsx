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
    const newScore = score + value;
    setResponses([...responses, value]);
    setScore(newScore);

    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      setSubmitted(true);
    }
  };

  if (submitted) {
    return (
      <main style={{ padding: "2rem", fontFamily: "Calibri, sans-serif", textAlign: "center" }}>
        <h1>Thank you, {name}!</h1>
        <p>Your ACE Questionnaire is complete.</p>
        <h2>Your ACE Score is <strong>{score.toFixed(2)} / 10</strong></h2>
      </main>
    );
  }

  return (
    <main style={{ padding: "2rem", fontFamily: "Calibri, sans-serif", textAlign: "center" }}>
      <h1>ACE Questionnaire</h1>
      <p><strong>Question {currentIndex + 1} of {questions.length}</strong></p>
      <p style={{ margin: "1.5rem 0" }}>{questions[currentIndex]}</p>
      <div style={{ display: "flex", justifyContent: "center", gap: "1.5rem" }}>
        <button onClick={() => handleResponse(1)} style={buttonStyle}>Yes</button>
        <button onClick={() => handleResponse(0)} style={buttonStyle}>No</button>
        <button onClick={() => handleResponse(0.25)} style={buttonStyle}>Skip</button>
      </div>
    </main>
  );
}

const buttonStyle = {
  padding: "0.75rem 1.5rem",
  fontSize: "1rem",
  borderRadius: "6px",
  border: "none",
  backgroundColor: "#3498db",
  color: "white",
  cursor: "pointer"
};
