import React, { useState } from "react";
import "./App.css";

function App() {
  // Add state for user information
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [linkedin, setLinkedin] = useState("");
  const [github, setGithub] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // Here you would typically send the data to your Flask backend
    fetch("http://localhost:5000/contact", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, email, phone, linkedin, github }),
    })
      .then((response) => response.json())
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <div className="App">
      <h1>Resume Builder</h1>
      {/* User Information Section */}
      <form onSubmit={handleSubmit} className="userInfoSection">
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="tel"
          placeholder="Phone +1234567890"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
        />
        <input
          type="text"
          placeholder="LinkedIn URL"
          value={linkedin}
          onChange={(e) => setLinkedin(e.target.value)}
        />
        <input
          type="text"
          placeholder="GitHub URL"
          value={github}
          onChange={(e) => setGithub(e.target.value)}
        />
        <button type="submit">Save Contact Info</button>
      </form>
      {/* Remove message display */}
      {/* Display user info in resumeSection */}
      <div className="resumeSection">
        <div className="userInfoDisplay">
          <h2>{name}</h2>
          {(email || phone || linkedin || github) && (
            <p>
              {email && <span>{email}</span>}
              {phone && <span> | {phone}</span>}
              {linkedin && <span> | {linkedin}</span>}
              {github && <span> | {github}</span>}
            </p>
          )}
        </div>
      </div>
      <div className="resumeSection">
        <h2>Experience</h2>
        <p>Experience Placeholder</p>
        <button>Add Experience</button>
        <br />
      </div>
      <div className="resumeSection">
        <h2>Education</h2>
        <p>Education Placeholder</p>
        <button>Add Education</button>
        <br />
      </div>
      <div className="resumeSection">
        <h2>Skills</h2>
        <p>Skill Placeholder</p>
        <button>Add Skill</button>
        <br />
      </div>
      <br />
      <button>Export</button>
    </div>
  );
}

export default App;
