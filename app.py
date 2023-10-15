
from recommendation import get_course_recommendations
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

# @app.route('/search/<semester>')
# def search(semester):
#     recommended_courses = get_course_recommendations(semester)
#     return render_template('index.html', courses=recommended_courses)


@app.route('/')
def home():
    return render_template('form.html')

@app.route('/search', methods=['POST'])
def search():
    semester = request.form.get('semester')
    return redirect(url_for('recommendations', semester=semester))

@app.route('/recommendations/<semester>')
def recommendations(semester):
    recommended_courses = get_course_recommendations(semester)
    return render_template('index.html', courses=recommended_courses)

if __name__ == '__main__':
    app.run(debug=True)
