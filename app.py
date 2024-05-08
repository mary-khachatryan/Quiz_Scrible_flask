
from flask import Flask, render_template,url_for, request,redirect

import openai
import streamlit as st
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi,TranscriptsDisabled
import os
import json
from dotenv import load_dotenv

app = Flask(__name__)
client = OpenAI()

load_dotenv()

# Retrieve API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
app.config["SECRET_KEY"] = "11_509"


@app.route('/', methods=['GET', 'POST'])
def home():
    


    
    if 'next_button' in request.form and request.method == 'POST':
        home.fav_num = request.form.get('fav_num')
        youtube_id = str(request.form.get('Youtube_id'))
        if(youtube_id != None):
            youtube_id = youtube_id[youtube_id.index('=') + 1 : youtube_id.index('=') + 12]
            print(youtube_id,"indexasdf")

        directory = ".."  # Root directory
        subdirectories = ["/opt/render/project/src/"]
        #subdirectories = ["Quiz_Scrible_flask"]
        file_name = f"{youtube_id}.json"
        
        home.file_path = os.path.join(directory, *subdirectories, file_name)
        print(home.file_path)
        if os.path.exists(home.file_path):
            with open(home.file_path,'r') as f:
                home.quiz_Text = json.load(f)
        else:
            dictSubtitle = None
            try:
                dictSubtitle = YouTubeTranscriptApi.get_transcript(youtube_id)
             
            except TranscriptsDisabled:
                    print("Transcripts are disabled for this video.")
            except Exception as e:
                    print("An error occurred:", e)
            
            if(dictSubtitle): 
                print("dictSubtitle",dictSubtitle)
                general_text = " ".join(i['text'] for i in dictSubtitle)
                for i in dictSubtitle:
                    general_text += " " + i['text']
                client = OpenAI()
                completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                {"role": "system", "content": f"I am sending you a text.you MUST represent 10 quetion,the questions and  send answers as json file.  which qontainn keys and values like that but dont include this example in json:\"questions\": [\"question\": \"What was the name of the ship mentioned in the text?\", \"A\": \"Nina\", \"B\": \"Pinta\", \"C\": \"Santa Maria\", \"D\": \"Annabel\", \"correct\": \"D\", correct: is same  letter  which is correct: TEXT{general_text}"},
            #{"role": "user", "content": f"{generalText}"}
                ]
                )
                quizfile_json = json.loads(completion.choices[0].message.content)
                with open(home.file_path, "w") as json_file:
                    json.dump(quizfile_json, json_file)
      
                with open(home.file_path, "r") as json_file:
                    home.quiz_Text = json.load(json_file)

  
                if home.fav_num =="509":
                    return redirect('Bayko')
                else:
                    return redirect('a')
            else:
                 print("noneeeeeeeeeee")
                 return render_template('home.html', title="restart", header  ="Transcripts are disabled for this video.")
    return render_template('home.html', title="Quiz Scrible" )
    
@app.route('/a', methods=['GET', 'POST'])
def quiz_form():
    answer_count = 0
    quiz_form.answers = ["None"] * 10
    for i in range(10):
        answer = request.form.get('group{}'.format(i))
        
        print('group{}'.format(i),"'group'.format(i)",answer)
        if  answer != None :
            quiz_form.answers[i] = answer
            answer_count +=1
           
    if 'next_button' in request.form and answer_count == 10:
        return redirect('result_page')
    else: 
        return render_template('form.html', title='title', header='Start Your Quiz Scrible',quiz_text = home.quiz_Text,answers = quiz_form.answers)


@app.route('/result_page', methods=['GET', 'POST'])
def result_pagee():
    
    final_score = 0
    right_answers =[]
    for i in range(10):
     
      right_answers.append( home.quiz_Text["questions"][i]["correct"])
      if right_answers[i] ==  quiz_form.answers[i]:
          final_score +=1
      
    if 'try_again' in request.form:
        
        return redirect(url_for("home"))
    return render_template('result.html', title="quiz-scrible", handler='handler',quiz_text = home.quiz_Text, r_answers=right_answers, answers= quiz_form.answers,final_score = final_score)


if __name__ == '__main__':
    app.run()