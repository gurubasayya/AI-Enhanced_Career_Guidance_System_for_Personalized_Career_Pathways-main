import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from typing import List, Dict, Any, Optional
from flask import Flask, request, jsonify

# Load environment variables from .env file
load_dotenv()

# Configuration
endpoint = "https://models.github.ai/inference"
model = "deepseek/DeepSeek-V3-0324"

# Get token from environment variables
token = os.getenv("GITHUB_PAT")
if not token:
    raise ValueError("GITHUB_PAT environment variable is not set. Please create a .env file with your GitHub PAT.")

def get_ai_client() -> ChatCompletionsClient:
    """Initialize and return the Azure AI client."""
    try:
        return ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
        )
    except Exception as e:
        raise Exception(f"Failed to initialize AI client: {str(e)}")

# Career-specific learning paths and guidance
CAREER_GUIDANCE = {
    'Software Engineer': {
        'overview': 'Software engineering is about designing, developing, and maintaining software systems.',
        'skills_needed': [
            'Data Structures & Algorithms',
            'System Design',
            'Version Control (Git)',
            'Testing & Debugging',
            'Cloud Platforms (AWS/Azure/GCP)'
        ],
        'learning_path': [
            'Master a programming language (Python, Java, or JavaScript)',
            'Learn data structures and algorithms',
            'Understand databases (SQL and NoSQL)',
            'Learn about APIs and web services',
            'Explore cloud computing fundamentals'
        ],
        'resources': [
            'LeetCode for coding practice',
            'Designing Data-Intensive Applications (book)',
            'FreeCodeCamp or The Odin Project',
            'AWS/Azure/GCP free tier for hands-on practice'
        ]
    },
    'Data Scientist': {
        'overview': 'Data science involves extracting insights from structured and unstructured data.',
        'skills_needed': [
            'Python/R Programming',
            'Statistics & Mathematics',
            'Machine Learning',
            'Data Visualization',
            'SQL & Database Management'
        ],
        'learning_path': [
            'Learn Python for data analysis (pandas, numpy)',
            'Study statistics and probability',
            'Master data visualization (matplotlib, seaborn)',
            'Learn machine learning fundamentals',
            'Work on real-world datasets'
        ],
        'resources': [
            'Kaggle for datasets and competitions',
            'Fast.ai for practical ML',
            'Towards Data Science publication',
            'Coursera\'s Machine Learning by Andrew Ng'
        ]
    },
    'Product Manager': {
        'overview': 'Product management focuses on developing and managing products throughout their lifecycle.',
        'skills_needed': [
            'Market Research',
            'Product Strategy',
            'Agile Methodologies',
            'User Experience (UX) Principles',
            'Data-Driven Decision Making'
        ],
        'learning_path': [
            'Learn product development lifecycle',
            'Study agile and scrum methodologies',
            'Understand UX/UI fundamentals',
            'Develop business and market analysis skills',
            'Practice stakeholder management'
        ],
        'resources': [
            'Inspired: How to Create Products Customers Love (book)',
            'Product School courses',
            'Marty Cagan\'s blog',
            'Lenny\'s Newsletter'
        ]
    },
    'default': {
        'overview': 'This career path shows good potential based on your skills.',
        'skills_needed': [
            'Industry-specific technical skills',
            'Communication & Collaboration',
            'Problem Solving',
            'Continuous Learning',
            'Project Management'
        ],
        'learning_path': [
            'Research industry requirements',
            'Identify key skills gap',
            'Take relevant courses/certifications',
            'Build a portfolio of projects',
            'Network with professionals in the field'
        ],
        'resources': [
            'LinkedIn Learning',
            'Industry-specific forums and communities',
            'Professional networking events',
            'Mentorship programs'
        ]
    }
}

def generate_career_guidance(career_title: str, match_percentage: int, growth: str, user_skills: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate comprehensive career guidance with learning path.
    
    Args:
        career_title: The title of the career
        match_percentage: The match percentage for this career
        growth: Growth potential (High/Medium/Low)
        user_skills: Dictionary containing user's skills and information
        
    Returns:
        Dictionary containing structured guidance and learning path
    """
    import time
    
    # Small delay for better UX
    time.sleep(0.3)
    
    # Get career guidance or default
    career_info = CAREER_GUIDANCE.get(career_title, CAREER_GUIDANCE['default'])
    
    # Return structured data instead of HTML
    return {
        'title': career_title,
        'match': match_percentage,
        'growth': growth,
        'overview': career_info['overview'],
        'skills': career_info['skills_needed'],
        'learning_path': career_info['learning_path'],
        'resources': career_info['resources']
    }

app = Flask(__name__)

@app.route('/api/guidance', methods=['POST'])
def api_guidance():
    data = request.get_json()
    career_title = data.get('title')
    match_percentage = data.get('match')
    growth = data.get('growth')
    user_skills = data.get('skills', {})
    if not career_title or match_percentage is None or not growth:
        return jsonify({'error': 'Missing required fields'}), 400
    guidance = generate_career_guidance(
        career_title=career_title,
        match_percentage=match_percentage,
        growth=growth,
        user_skills=user_skills
    )
    return jsonify(guidance)

def main():
    """Example usage of the career guidance generator."""
    # Example data - this would come from your application
    example_results = [
        {"title": "Software Engineer", "match": 92, "growth": "High"},
        {"title": "Data Scientist", "match": 88, "growth": "Very High"},
        {"title": "Product Manager", "match": 85, "growth": "High"}
    ]
    
    example_skills = {
        "technical_skills": ["Python", "Web Development", "Databases"],
        "programming_languages": ["Python", "JavaScript", "SQL"],
        "soft_skills": ["Communication", "Teamwork", "Problem Solving"],
        "experience_level": "Intermediate",
        "certifications": "AWS Certified Cloud Practitioner"
    }
    
    # Loop through each career and get specific guidance
    for result in example_results:
        guidance = generate_career_guidance(
            career_title=result["title"],
            match_percentage=result["match"],
            growth=result["growth"],
            user_skills=example_skills
        )
        print(f"\n{'='*50}")
        print(f"CAREER: {guidance['title']} ({guidance['match']}% Match, {guidance['growth']} Growth)")
        print("-" * 50)
        print(f"Overview: {guidance['overview']}\n")
        print("What to learn:")
        for item in guidance['learning_path']:
            print(f"  - {item}")
        print("\nHow to learn (Resources):")
        for resource in guidance['resources']:
            print(f"  - {resource}")
        print("="*50)

if __name__ == "__main__":
    app.run(debug=True)
