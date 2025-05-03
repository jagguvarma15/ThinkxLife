import { useState, useEffect } from "react";
import thinkLogo from "../assets/think-logo.png";
import { ChevronLeft, Menu } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function About() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
  const navigate = useNavigate();

  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth < 768);
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <div style={{ position: "relative", height: "100vh", width: "100vw", fontFamily: "Arial, sans-serif", backgroundColor: "#ffffff", overflow: "hidden" }}>
      {/* Sidebar */}
      <aside style={{
        position: "fixed",
        top: 0,
        left: 0,
        height: "100vh",
        width: "250px",
        backgroundColor: "#ffffff",
        boxShadow: "2px 0 5px rgba(0,0,0,0.1)",
        transform: sidebarOpen ? "translateX(0)" : "translateX(-100%)",
        transition: "transform 0.3s ease-in-out",
        zIndex: 1000,
        padding: "2rem 1.5rem"
      }}>
        <button
          onClick={() => setSidebarOpen(false)}
          style={{
            position: "absolute",
            top: "1rem",
            right: "1rem",
            background: "transparent",
            border: "none",
            cursor: "pointer"
          }}
        >
          <ChevronLeft size={20} />
        </button>

        <h2 style={{ fontSize: "1.5rem", fontWeight: "700", marginBottom: "2rem" }}>Explore</h2>
        <div style={{ marginBottom: "2rem" }}>
          <h4 style={{ marginBottom: "0.5rem" }}>🎨 Art</h4>
          <ul style={{ paddingLeft: 0, listStyle: "none", fontSize: "0.95rem" }}>
            <li>Gallery Exhibit</li>
            <li>Children's Mural</li>
            <li>Local Artist Collab</li>
          </ul>
        </div>
        <div style={{ marginBottom: "2rem" }}>
          <h4 style={{ marginBottom: "0.5rem" }}>🤝 Community</h4>
          <ul style={{ paddingLeft: 0, listStyle: "none", fontSize: "0.95rem" }}>
            <li>Neighborhood Talks</li>
            <li>Volunteer Drive</li>
            <li>Inclusive Design Forum</li>
          </ul>
        </div>
        <div style={{ marginBottom: "2rem" }}>
          <h4 style={{ marginBottom: "0.5rem" }}>📅 Events</h4>
          <ul style={{ paddingLeft: 0, listStyle: "none", fontSize: "0.95rem" }}>
            <li>ACE Workshop</li>
            <li>Community Garden Day</li>
            <li>Storytelling Circle</li>
          </ul>
        </div>
        <div>
          <h4 style={{ marginBottom: "0.5rem" }}>🚀 Projects</h4>
          <ul style={{ paddingLeft: 0, listStyle: "none", fontSize: "0.95rem" }}>
            <li>EarthCare Initiative</li>
            <li>Mindful Mondays</li>
            <li>Art for All</li>
          </ul>
        </div>
        <p style={{ fontSize: "0.8rem", color: "#999", marginTop: "2rem" }}>© 2025 Think Round, Inc.</p>
      </aside>

      {/* Top-right navigation */}
      <nav style={{ position: "fixed", top: "1rem", right: "1rem", zIndex: 1100, display: "flex", gap: "1rem" }}>
        <button onClick={() => navigate("/signin")} style={{ background: "transparent", border: "none", fontWeight: "600", cursor: "pointer" }}>Sign In</button>
        <button onClick={() => navigate("/")} style={{ background: "transparent", border: "none", fontWeight: "600", cursor: "pointer" }}>About Us</button>
        <button onClick={() => navigate("/chatbot")} style={{ background: "transparent", border: "none", fontWeight: "600", cursor: "pointer" }}>Chatbot</button>
      </nav>

      {!sidebarOpen && (
        <button
          onClick={() => setSidebarOpen(true)}
          style={{
            position: "fixed",
            top: "1rem",
            left: "1rem",
            zIndex: 1100,
            background: "#fff",
            border: "1px solid #ccc",
            borderRadius: "6px",
            padding: "0.5rem",
            boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
            cursor: "pointer"
          }}
        >
          <Menu size={20} />
        </button>
      )}

      {sidebarOpen && (
        <div
          onClick={() => setSidebarOpen(false)}
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            backgroundColor: "rgba(0, 0, 0, 0.3)",
            backdropFilter: "blur(3px)",
            zIndex: 900,
          }}
        />
      )}

      <main style={{
        padding: isMobile ? "1.5rem" : "3rem",
        width: "100%",
        maxWidth: "900px",
        margin: "0 auto",
        backgroundColor: "#ffffff",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center"
      }}>
        <div style={{
          display: "flex",
          flexDirection: isMobile ? "column" : "row",
          alignItems: "center",
          gap: "1rem",
          marginBottom: "2rem"
        }}>
          <img src={thinkLogo} alt="Think Round Logo" style={{ height: isMobile ? "80px" : "120px" }} />
          <div style={{ textAlign: isMobile ? "center" : "left" }}>
            <h1 style={{ fontSize: isMobile ? "2rem" : "2.5rem", fontWeight: "800", margin: 0 }}>Think Round, Inc.</h1>
            <p style={{ fontSize: isMobile ? "1rem" : "1.1rem", color: "#555" }}>Earth is home, Humans are family.</p>
          </div>
        </div>

        <div style={{ maxWidth: "700px", fontSize: "1rem", color: "#444", lineHeight: "1.6" }}>
          <p>
            Think Round, Inc. is a 501(c)(3) nonprofit organization founded in 2004 to promote the arts, the environment, and community health. Rooted in the belief that nurturing the whole person—body, mind, and spirit—requires a healthy planet and equitable community, Think Round advances this mission through art-centered programming, environmental advocacy, and inclusive education.
          </p>
          <p>
            Our work supports creative self-expression, healing, and resilience, with a focus on those affected by trauma or socio-economic barriers. Through partnerships, exhibitions, workshops, and public installations, we aim to transform lives by uniting artistic exploration with sustainability, empathy, and social justice.
          </p>
        </div>
      </main>
    </div>
  );
}
