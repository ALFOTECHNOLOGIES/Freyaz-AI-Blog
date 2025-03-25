import os
import openai
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
BLOG_DIR = "my_ai_blog"
POSTS_DIR = os.path.join(BLOG_DIR, "_posts")
GITHUB_REPO = "ALFOTECHNOLOGIES/Freyaz-AI-Blog"
ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

def install_dependencies():
    """Install required dependencies."""
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

def setup_blog():
    """Setup Jekyll blog structure if not already existing."""
    if not os.path.exists(BLOG_DIR):
        subprocess.run(["jekyll", "new", BLOG_DIR], check=True)
    if not os.path.exists(POSTS_DIR):
        os.makedirs(POSTS_DIR)

def generate_article(topic):
    """Use OpenAI to generate an article."""
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Fetch API key from environment variable
    if not openai.api_key:
        raise ValueError("API key not set. Please set the OPENAI_API_KEY environment variable.")
    
    prompt = f"Write an SEO-optimized blog post about {topic}. Include an introduction, key points, and conclusion."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

def save_article(content, topic):
    """Save the AI-generated article as a markdown post."""
    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date}-{topic.replace(' ', '-')}.md"
    filepath = os.path.join(POSTS_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"---\n")
        f.write(f"title: {topic}\n")
        f.write(f"date: {date}\n")
        f.write(f"---\n\n")
        f.write(content)
    return filename

def deploy_to_github():
    """Push new posts to GitHub Pages."""
    os.chdir(BLOG_DIR)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Auto-generated blog post"], check=True)
    subprocess.run(["git", "push", f"https://{ACCESS_TOKEN}@github.com/{GITHUB_REPO}.git", "main"], check=True)
    os.chdir("..")

def main():
    install_dependencies()
    setup_blog()
    topic = "Latest AI Trends in 2025"
    article = generate_article(topic)
    save_article(article, topic)
    deploy_to_github()

if __name__ == "__main__":
    main()