
import os

from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

SYSTEM_PROMPT = """
You are IdeaForge AI, a helpful college project idea assistant.

Generate practical, creative, beginner-friendly project ideas.
Use clear, simple English and well-organized headings.
Avoid unrealistic budgets and expensive hardware.
Give enough details for a college student to start building.
"""


def generate_with_groq(prompt):
    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Set it in your terminal."
        )

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.7,
        max_tokens=4000,
    )

    content = response.choices[0].message.content

    if not content or not content.strip():
        raise RuntimeError(
            "The AI returned an empty response. Please try again."
        )

    return content.strip()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}

    fields = {
        "domain": (data.get("domain") or "Artificial Intelligence").strip(),
        "skills": (data.get("skills") or "Beginner programming").strip(),
        "difficulty": (data.get("difficulty") or "Beginner").strip(),
        "project_type": (
            data.get("project_type") or "College mini project"
        ).strip(),
        "budget": (data.get("budget") or "Low / free tools").strip(),
        "focus": (data.get("focus") or "None specified").strip(),
    }

    prompt = f"""
Create 3 meaningfully different and feasible college project ideas.

Student details:
- Domain: {fields['domain']}
- Current skills: {fields['skills']}
- Difficulty: {fields['difficulty']}
- Project type: {fields['project_type']}
- Budget/resources: {fields['budget']}
- Extra interests or constraints: {fields['focus']}

For EACH of the 3 ideas, include:

1. Project title
2. Problem statement
3. Proposed solution
4. Four to six key features
5. Suggested technology stack
6. Development roadmap with four to six steps
7. What makes the idea distinctive
8. Difficulty level
9. First milestone to complete

Use clear headings and simple English.
Keep the projects feasible for a college student.
Avoid expensive hardware or paid services unless requested.

End with a reminder to research similar projects and validate
originality before submitting the project.
"""

    try:
        result = generate_with_groq(prompt)
        return jsonify({"result": result}), 200

    except RuntimeError as exc:
        app.logger.error("Idea generation setup error: %s", exc)
        return jsonify({"error": str(exc)}), 503

    except Exception as exc:
        app.logger.exception("Groq request failed")
        return jsonify({
            "error": f"{type(exc).__name__}: {str(exc)}"
        }), 502


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.environ.get("PORT", 5000)),
        debug=False,
    )

