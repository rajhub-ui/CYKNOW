# 🛡️ CyberFit (CYKNOW) - Citizen Cyber Resilience Platform

CyberFit is an interactive, full-stack educational platform designed to protect Indian citizens from modern digital threats such as Phishing, Digital Arrest Scams, and Malicious Applications. 

Unlike traditional awareness programs that rely on reading static text, CyberFit uses **gamified simulations, adaptive learning paths, and accessible design** to ensure users actually retain what they learn.

## ✨ Key Features

- **📊 Adaptive Learning Paths**: A baseline survey assesses the user's knowledge and dynamically assigns them a *Beginner*, *Intermediate*, or *Advanced* learning path.
- **🃏 Swipeable Learning Cards**: Bite-sized, gamified learning modules with built-in **Text-to-Speech (TTS)** for accessibility.
- **🎣 Interactive Simulations**: 
  - *Phishing Inbox*: Spot the fake emails vs. real ones.
  - *Digital Arrest*: Navigate a high-pressure fake police video call.
  - *Malicious Apps*: Audit dangerous app permissions.
- **🇮🇳 Bilingual Support**: Full UI and learning content localization for **English and Hindi**.
- **📞 Emergency Directory**: One-tap dialing (`tel:` links) to official national helplines (1930, 1909, 112, etc.).
- **📝 1930 Report Generator**: Generates a pre-filled mock complaint for the National Cyber Crime portal.
- **👑 Admin Dashboard**: A secure analytics panel to track total users, total quizzes taken, and average scores per module.

## 🛠️ Tech Stack

- **Backend**: Python (Flask), SQLite (Self-healing schema)
- **Frontend**: HTML5, Vanilla JavaScript, CSS3
- **Libraries**: Chart.js (Analytics), Web Speech API (Audio), PyJWT & bcrypt (Authentication)
- **Architecture**: RESTful API with Session & JWT hybrid authentication

## 💻 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rajhub-ui/CYKNOW.git
   cd CYKNOW
