from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_reply(property_info, question):
    prompt = f"""
You are an Airbnb host assistant.

Detect the language of the guest question and reply in the SAME language.

Property Info:
{property_info}

Guest Question:
{question}

Rules:
- Be polite and natural
- Keep it short
- If info is missing, say you will confirm
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


@app.route("/", methods=["GET", "POST"])
def index():
    reply = ""

    if request.method == "POST":
        property_info = request.form["property_info"]
        question = request.form["question"]

        reply = generate_reply(property_info, question)

    return render_template("index.html", reply=reply)


if __name__ == "__main__":
    app.run(debug=True)