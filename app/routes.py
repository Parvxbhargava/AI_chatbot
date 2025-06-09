from flask import Blueprint, render_template, request, redirect, url_for,jsonify
from flask_login import login_required, current_user
from app.api import call_api


main=Blueprint("main",__name__)

@main.route("/")
def home():
  if current_user.is_authenticated:
    return redirect(url_for("main.chat"))
  return redirect(url_for("auth.login"))

@main.route("/chat")
@login_required
def chat():
  return render_template("chat.html",user=current_user)

@main.route("/chat/message",methods=["POST"])
@login_required
def chat_message():
  user_input=request.json.get("message"," ")
  if not user_input:
    return jsonify({"error":"Message is required"}),400
  
  short_term_memory = [
    {"role": "system", "content": "You're a helpful assistant."},
  ]
  
  long_term_memory=[]
  
  reply=call_api(user_input,user_id=current_user.id,short_term_memory=short_term_memory,long_term_memory=long_term_memory)

  return jsonify({"reply":reply})


