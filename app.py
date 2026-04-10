from flask import Flask, render_template, request, session, redirect
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # needed for session

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_reply(property_info, question):
    prompt = f"""
    You are an Airbnb host assistant.

    Detect the language of the guest and reply in the same language.

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

    # If user submits property info
    if request.method == "POST" and "property_info" in request.form:
        session["property_info"] = request.form["property_info"]
        return redirect("/")

    # If user asks a question
    if request.method == "POST" and "question" in request.form:
        property_info = session.get("property_info", "")
        question = request.form["question"]

        if property_info:
            reply = generate_reply(property_info, question)

    return render_template("index.html", reply=reply, property_saved="property_info" in session)


@app.route("/reset")
def reset():
    session.pop("property_info", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
