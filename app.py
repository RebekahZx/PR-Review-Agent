from flask import Flask, request, render_template

from review_engine.pr_fetcher import PRFetcher

from review_engine.ai_reviewer import AIReviewer

import os

from dotenv import load_dotenv



# Load environment variables from .env

load_dotenv()



app = Flask(__name__)



# Initialize AI reviewer with API key from .env

ai = AIReviewer(api_key=os.environ.get("GEMINI_API_KEY"))



@app.route("/", methods=["GET", "POST"])

def index():

    feedback = []



    if request.method == "POST":

        repo_url = request.form.get("repo_url")

        pr_number = request.form.get("pr_number")



        if not repo_url or not pr_number:

            return render_template("index.html", feedback=[], error="Please provide both repo URL and PR number.")



        try:

            pr_number = int(pr_number)

        except ValueError:

            return render_template("index.html", feedback=[], error="PR number must be an integer.")



        # Fetch PR changes

        fetcher = PRFetcher(repo_url)

        changes = fetcher.get_pr_diff(pr_number)



        # Review each file patch

        for c in changes:

            patch = c.get("patch", "")

            if patch.strip():

                review_text = ai.review_patch(c["filename"], patch)

                feedback.append({

                    "filename": c["filename"],

                    "review_text": review_text

                })



    return render_template("index.html", feedback=feedback)



if __name__ == "__main__":

    app.run(debug=True)

