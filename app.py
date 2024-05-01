from radio_buttons import Quiz_Form,MyForm
from flask import Flask, render_template,url_for, request,redirect
app = Flask(__name__)


app.config["SECRET_KEY"] = "11_509"

# @app.route("/")
# def myredirect():
#     return redirect(url_for('quiz_form'))



@app.route('/', methods=['GET', 'POST'])
def home():
    form = MyForm()
    result = request.form
    if 'next_button' in request.form and request.method == 'POST':
        print("val")
        return redirect('a')
        #return render_template('form_handler.html', title="youtube", handler='handler', result=result)
        #return render_template('form.html')\
        #return render_template('form.html', title="kov", handler='handler')
    return render_template('home.html', title="youtube", handler='handler')
    # if form.validate_on_submit():
    #     print("val")
    #     return redirect(url_for('a'))
    # return render_template('home.html', title="youtube", handler='handler', form=form, result=result)

@app.route('/a', methods=['GET', 'POST'])
def quiz_form():
    form = Quiz_Form()
    if 'next_button' in request.form and request.method == 'POST':
        result = request.form
        return render_template('form_handler.html', title="youtube", handler='handler', result=result)
    return render_template('form.html', title='title', header='header2', form=form)

#  if request.method == 'POST':
#         if 'next_button' in request.form:
#             print("val")
#             return redirect(url_for('a'))
#     return render_template('home.html', title="youtube", handler='handler')