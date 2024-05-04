
from flask import Flask, render_template,url_for, request,redirect

import openai
import streamlit as st
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
import os
import json

app = Flask(__name__)


app.config["SECRET_KEY"] = "11_509"


@app.route('/', methods=['GET', 'POST'])
def home():
    youtube_id = request.form.get('Youtube_id')
    if 'next_button' in request.form and request.method == 'POST':
        print("val")

        #youtube_id = str(request.form.get('fname'))
        print("IDD",youtube_id)

        directory = ".."  # Root directory
        subdirectories = ["Quiz_Scrible_flask"]
        file_name = f"{youtube_id}.json"
        
        home.file_path = os.path.join(directory, *subdirectories, file_name)
        
        if os.path.exists(home.file_path):
            with open(home.file_path,'r') as f:
                home.quiz_Text = json.load(f)
        else:
            dictSubtitle = YouTubeTranscriptApi.get_transcript(youtube_id) 
            general_text = " ".join(i['text'] for i in dictSubtitle)
            for i in dictSubtitle:
                general_text += " " + i['text']
            client = OpenAI()
            completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": f"I am sending you a text.you MUST represent 10 quetion,the questions and  send answers as json file.  which qontainn keys and values like: \"qeuestion\",\"A\":answer,\"B\":answer,\"C\":answer,\"D\":answer, correct: same  answer which is correct: TEXT{general_text}"},
            #{"role": "user", "content": f"{generalText}"}
            ]
            )
            quizfile_json = json.loads(completion.choices[0].message.content)
            with open(home.file_path, "w") as json_file:
                json.dump(quizfile_json, json_file)
      
            with open(home.file_path, "r") as json_file:
                home.quiz_Text = json.load(json_file)

  
        print("id", youtube_id)
        return redirect('a')
        
    return render_template('home.html', title="youtube", handler='handler')
    
@app.route('/a', methods=['GET', 'POST'])
def quiz_form():
    answer_count = 0
    quiz_form.answers =["None","None","None","None","None","None","None","None","None","None",]
    for i in range(10):
        answer = request.form.get('group{}'.format(i))
        
        print('group{}'.format(i),"'group'.format(i)",answer)
        if  answer != None :
            quiz_form.answers[i] = answer
            answer_count +=1
           
    if 'next_button' in request.form and request.method == 'POST' and answer_count == 10:
        
        print("yess")
        return redirect('result_page')
    else: 
        return render_template('form.html', title='title', header='header2',quiz_text = home.quiz_Text,answers = quiz_form.answers)


@app.route('/result_page', methods=['GET', 'POST'])
def result_pagee():
    print("asdffggh")
    final_score = 0
    right_answers =[]
    for i in range(10):
     
      right_answers.append( home.quiz_Text["questions"][i]["correct"])
      if right_answers[i] ==  quiz_form.answers[i]:
          final_score +=1
      print(right_answers)
    if 'try_again' in request.form and request.method == 'POST':
        print("yess")
        return redirect(url_for("home"))
    return render_template('result.html', title="youtube", handler='handler',quiz_text = home.quiz_Text, r_answers=right_answers, answers= quiz_form.answers,final_score = final_score)




#return render_template('result.html', title="youtube", handler='handler')