# 🤖 Talx API - AI Backend  

**Visit Talx**: [https://talx.vercel.app/](https://talx.vercel.app/)  

**Talx API** powers the AI-driven functionalities of the **Talx** platform, providing intelligent features like **ResumeAI** and **Chat Assistant AI**. This backend is built with Flask and leverages advanced AI models, ensuring seamless integration of AI capabilities into the Talx ecosystem.  

---

## 📖 Table of Contents  

- [About Talx API](#about-talx-api)  
- [Key Features](#key-features)  
- [Related Repositories](#related-repositories)  
- [API Routes](#api-routes)  
- [Tech Stack](#tech-stack)  
- [Installation](#installation)  

---

## 📝 About Talx API  

Talx API is the core AI backend for the Talx job portal, handling functionalities such as:  
1. **Resume Analysis**:  
   - Analyzes resumes and job descriptions, providing compatibility scores and actionable recommendations using **Google Gemini 2.0 Flash**.  
2. **Chat Assistant**:  
   - Powered by **Llama 3.3 Versatile** for career guidance and platform support.  
3. **Streaming Responses**:  
   - Real-time responses enhance user interaction, ensuring a smooth experience.  

---

## ✨ Key Features  

- **ResumeAI**:  
  Analyze resumes against job descriptions or general criteria to provide insights and recommendations.  
- **Chat Assistant AI**:  
  An intelligent assistant offering platform navigation help and career guidance.  
- **Real-time Streaming**:  
  Supports real-time AI responses for better interactivity.  
- **Secure API**:  
  Ensures protected access via authorization headers and environment variables.  

---

## 🔗 Related Repositories  

1. **Talx Frontend (Main Platform)**  
   - [talx-frontend](https://github.com/aakashdixit22/talx-frontend)  

2. **Talx Backend (Job Portal Backend)**  
   - [talx-backend](https://github.com/aakashdixit22/talx-backend)  

---

## 📡 API Routes  

### 1. **Home**  
- **`GET /`**  
  - **Description**: Health check endpoint.  

---

### 2. **Resume Analysis**  
- **`POST /upload-resume`**  
  - **Description**: Analyze a resume and optionally compare it with a job description.  
  - **Headers**:  
    - `Authorization`: Bearer token for API access.  
  - **Form Data**:  
    - `file`: PDF file of the resume.  
    - `job_description`: (Optional) Text of the job description.  
  - **Response**:  
    ```json
    {
      "summary": {
        "matching_analysis": "Detailed analysis here.",
        "description": "Summary of relevance.",
        "score": 85,
        "skill_match_score": 90,
        "recommendation": "Suggestions for improvement."
      }
    }
    ```
    - **Note**: The `skill_match_score` will only be included in the response if a `job_description` is provided.

---

### 3. **Chat Assistant**  
- **`POST /genie`**  
  - **Description**: Provides interactive career guidance and platform navigation help.  
  - **Headers**:  
    - `Authorization`: Bearer token for API access.  
  - **Body Parameters**:  
    ```json
    {
      "query": "User query here",
      "chat_history": [
        {"role": "user", "content": "Previous query"},
        {"role": "assistant", "content": "Previous response"}
      ]
    }
    ```  
  - **Response**: Real-time streaming of AI-generated content.  

---

## 🛠️ Tech Stack  

1. **Framework**: Flask  
2. **AI Models**:  
   - Llama 3.3 Versatile by Meta (via Groq)  
   - Google Gemini 2.0 Flash Via Gemini AI Studio 
3. **Utilities**:  
   - Flask-CORS for Cross-Origin Resource Sharing  
   - Python libraries: `google.generativeai`, `dotenv`, `io`  
4. **Authorization**: Secure endpoints with `Authorization` headers.  
5. **Streaming**: Flask-SSE for real-time AI responses.  

---

## 🚀 Installation  

### Prerequisites  

- Python 3.8+  
- Environment variables set up in a `.env` file:  
  ```env
  AUTH_SECRET=your_secret_key
  GROQ_API_KEY=your_groq_api_key
  GOOGLE_GEMINI_API_KEY=your_google_gemini_key
  ```

### Steps  

1. Clone the repository:  
   ```bash
   git clone https://github.com/aakashdixit22/talx-api.git
   cd talx-api
   ```  

2. Create a virtual environment:  
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```  

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  

4. Run the API:  
   ```bash
   python api/index.py
   ```  

5. The API will be available at `http://127.0.0.1:5000`.  

---

## 🧪 Testing  

### **Resume Analysis**  
Use Postman or cURL to test:  
```bash
curl -X POST http://127.0.0.1:5000/upload-resume \
-H "Authorization: Bearer your_secret_key" \
-F "file=@resume.pdf" \
-F "job_description=Software Engineer role."
```

### **Chat Assistant**  
```bash
curl -X POST http://127.0.0.1:5000/genie \
-H "Authorization: Bearer your_secret_key" \
-H "Content-Type: application/json" \
-d '{"query": "How can I improve my resume?", "chat_history": []}'
```

---

## 📜 License  

This project is licensed under the [MIT License](https://github.com/aakashdixit22/talx-api/blob/main/LICENSE).  

