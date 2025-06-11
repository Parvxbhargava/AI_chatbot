from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from flask_login import login_required, current_user
from app.api import call_api
from app.models import LongTermMemory  # make sure this matches your model name
from app import db

main = Blueprint("main", __name__)


@main.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("main.chat"))
    return redirect(url_for("auth.login"))


@main.route("/chat")
@login_required
def chat():
    return render_template("chat.html", user=current_user)


@main.route("/chat/message", methods=["POST"])
@login_required
def chat_message():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"error": "Message is required"}), 400

    # Load session-based short-term memory (STM)
    conversation = session.get("conversation", [])
    conversation.append({"role": "user", "content": user_input})
    short_term_memory = conversation[-5:]  # Only last 10 messages

    # Fetch long-term memory (LTM) from database
    user_memories = LongTermMemory.query.filter_by(user_id=current_user.id).all()
    long_term_memory = [{"role": "user", "content": m.content} for m in user_memories]

    # Call the chatbot API
    reply = call_api(user_input, user_id=current_user.id,
                     short_term_memory=short_term_memory,
                     long_term_memory=long_term_memory)

    # Save assistant reply in conversation
    conversation.append({"role": "assistant", "content": reply})
    session["conversation"] = conversation[-10:]  # Keep session small

    return jsonify({"reply": reply})


@main.route("/ltm")
@login_required
def ltm():
     user_memories = LongTermMemory.query.filter_by(user_id=current_user.id).all()
     return render_template("ltm.html", memories=user_memories)


@main.route("/clear_session")
@login_required
def clear_session():
    session.clear()
    return "Session cleared. Try chatting again."

@main.route("/ltm/delete/<int:memory_id>", methods=["POST"])
@login_required
def delete_memory(memory_id):
    memory = LongTermMemory.query.get_or_404(memory_id)
    if memory.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(memory)
    db.session.commit()
    return jsonify({"success": True})


