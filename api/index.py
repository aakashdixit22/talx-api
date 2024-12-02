from flask import Flask, request, jsonify, Response
from groq import Groq
from dotenv import load_dotenv
import os
import logging
from flask_cors import CORS
import google.generativeai as genai
import io



load_dotenv()


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

AUTH_SECRET = os.getenv('AUTH_SECRET')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY is missing. Please check your .env file.")

GOOGLE_GEMINI_API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')

genai.configure(api_key=GOOGLE_GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

client = Groq(api_key=GROQ_API_KEY)


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    """Home route for health check."""
    return 'Hello, World!'

def generate_prompt(job_description=None):
    base_prompt = """
        You are an advanced AI model designed to analyze the compatibility between a CV and a job description. 
        Your task is to output a structured JSON format that includes the following:
        
        1. matching_analysis: Analyze the CV against the job description to identify key strengths and gaps.
        2. description: Summarize the relevance of the CV to the job description in a few concise sentences.
        3. score: Provide a numerical compatibility score (0-100) based on qualifications, skills, and experience.
        4. recommendation: Suggest actions for the candidate to improve their match or readiness for the role.
    """

    if job_description:
        prompt = f"""
        {base_prompt}
        Here is the Job Description: {job_description}
        The CV is attached for analysis. Analyze the CV against the job description and provide detailed insights.
        Your output must be in JSON format as follows:
        {{
          "matching_analysis": "Your detailed analysis here.",
          "description": "A brief summary here.",
          "score": 85,
          "recommendation": "Your suggestions here."
        }}
        """
    else:
        prompt = f"""
        {base_prompt}
         The CV is attached for analysis. Analyze the CV and provide detailed insights. 
        As no job description is provided, analyze the CV in general and suggest areas for improvement.
        Your output must be in JSON format as follows:
        {{
          "matching_analysis": "Your detailed analysis here.",
          "description": "A general summary here.",
          "score": 70,
          "skill_match_score": "The skill match score with the required skills in job description",
          "recommendation": "Your suggestions here."
        }}
        """
    return prompt


@app.route('/upload-resume', methods=['POST'])
def uploadResume():
    auth_secret_fetched = request.headers.get('Authorization') or request.headers.get('authorization') or request.json.get('authorization') or request.json.get('Authorization')
    if not auth_secret_fetched:
        return jsonify({'error': 'Authorization header is required.'}), 401
    
    if auth_secret_fetched != AUTH_SECRET:
        return jsonify({'error': 'Invalid authorization secret.'}), 401
    
    job_description = request.form.get('job_description')
    print(job_description)

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    print(file)

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.lower().endswith('.pdf'):
        try:
            pdf_bytes = file.read()
            pdf_stream = io.BytesIO(pdf_bytes)

            sample_file = {
                "mime_type": "application/pdf",
                "data": pdf_stream.getvalue()
            }

        except Exception as e:
            logging.error(f"Error reading in-memory file: {e}")
            return jsonify({"error": f"Error reading file: {e}"}), 500

        

        try:
            prompt = generate_prompt(job_description=job_description)
            response = model.generate_content([prompt, sample_file])
            summary = response.text
            print(summary)
            return jsonify({"summary": summary})
        except Exception as e:
            logging.error(f"Error generating summary: {e}")
            return jsonify({"error": f"Error generating summary: {e}"}), 500
        


@app.route('/genie', methods=['POST'])
def genie():
    chat_history = request.json.get('chat_history')
    auth_secret_fetched = request.headers.get('Authorization') or request.headers.get('authorization') or request.json.get('authorization') or request.json.get('Authorization')
    if not auth_secret_fetched:
        return jsonify({'error': 'Authorization header is required.'}), 401
    
    if auth_secret_fetched != AUTH_SECRET:
        return jsonify({'error': 'Invalid authorization secret.'}), 401
    
    try:
        user_query = request.json.get('query')
        print(user_query)
        if not user_query:
            return jsonify({'error': 'Query parameter is required.'}), 400

        logging.info(f"Processing query: {user_query}")

        temperature = 0.6
        max_tokens = 1500
        top_p = 0.9

                # Ensure chat_history is a list of dictionaries
        if not isinstance(chat_history, list):
            return jsonify({'error': 'chat_history must be a list of JSON objects.'}), 400
        print(chat_history)
        # Add the system message to the chat history
        system_message = {
            "role": "system",
            "content": (
                "You are Talx, an AI-powered assistant dedicated to the Talx job portal platform. "
                "Your role is to provide precise and contextual guidance related to the platform's features and functionality. "
                "Avoid answering irrelevant or unrelated questions and strictly focus on the Talx platform's context. "
                "If the user asks about topics outside the platform's scope, politely redirect them back to Talx-related features."
                "\n\nKey features to consider:\n"
                "1. Help job seekers find jobs, understand trends, and improve their job application materials.\n"
                "2. Assist job posters with actions like managing job postings, viewing applicants, and downloading application details.\n"
                "3. Support users in using the 'BulletinBuzz' news platform to stay informed about trends and keywords relevant to their industry.\n"
                "4. Analyze uploaded documents (e.g., resumes, cover letters, job descriptions) and provide actionable insights.\n"
                "5. Provide clear, concise, and professional answers while ensuring a conversational tone.\n"
                "6. Provide navigation assistance by directing users to the correct platform sections when needed using these links:\n"
                "   - **Home:** https://job-portal-frontend-swart.vercel.app/\n"
                "   - **Login:** https://job-portal-frontend-swart.vercel.app/login\n"
                "   - **Signup:** https://job-portal-frontend-swart.vercel.app/signup\n"
                "   - **Job Search:** https://job-portal-frontend-swart.vercel.app/search\n"
                "   - **My Posted Jobs:** https://job-portal-frontend-swart.vercel.app/my-job\n"
                "   - **Post a Job:** https://job-portal-frontend-swart.vercel.app/post-job\n"
                "   - **My Applications:** https://job-portal-frontend-swart.vercel.app/my-applications\n"
                "   - **BulletinBuzz (News Platform):** https://job-portal-frontend-swart.vercel.app/news\n"
                "If the user cannot find something or explicitly asks for navigation help, provide the relevant link from the list above."
            )
        }
        
        # Insert the system message at the beginning of the chat history
        chat_history.insert(0, system_message)
        
        # Append the user query to the chat history
        chat_history.append({"role": "user", "content": user_query})
        
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=chat_history,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=True,
        )
        
        def stream_response():
            response = ""
            for chunk in completion:
                delta = chunk.choices[0].delta.content or ""
                response += delta
                yield delta
            logging.info("Response fully generated.")
        
        return Response(stream_response(), content_type='text/plain')

    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        return jsonify({'error': 'An error occurred while processing the request.', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
