from flask import Flask,  render_template, request, escape, session
from vsearch import search4letters
from DBcm import UseDatabase
from checker import check_logged_in

app = Flask(__name__)

app.config['dbconfig'] = { 'host': '127.0.0.1',
                           'user': 'vsearch',
                           'password': 'vsearchpasswd',
                           'database': 'vsearchlogDB',
                         }


def log_request(req: 'flask_request', res: str) -> None:
    """ Log details of the web request and the results."""

    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into log
                  (phrase, letters, ip, browser_string, results)
                  values
                  (%s, %s, %s, %s, %s)"""

        cursor.execute(_SQL, (req.form['phrase'],
                          req.form['letters'],
                          req.remote_addr,
                          req.user_agent.browser,
                          res,
                          ))


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = "Here are your results: "
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                            the_title = title,
                            the_phrase = phrase,
                            the_letters = letters,
                            the_results = results,
                             )

@app.route('/')
@app.route('/entery')
def entery_page() -> 'html':
    return render_template('entery.html',
                            the_title = "Welcome to search4letters on the web!")


# For now this is in testing phase, the ide is to redirect to please_login
# but for now decorater check_logged_in is redirectiong to login page
@app.route('/please_login', methods = ['POST'])
def please_login() -> 'html':
    title = 'Please Login to view the logs'
    password = request.form['password']
    return render_template('please_login.html',
                            the_title = title,
                            the_password = password,
                            )

@app.route('/login')
def login() -> 'html':
    session['logged_in'] = True
    title = 'You are now loged in'
    return render_template('login.html',
                            the_title = title)
@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """ select phrase, letters, ip, browser_string, results
                   from log"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()

    titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')

    return render_template('viewlog.html',
                           the_title = 'View Log',
                           the_row_titles = titles,
                           the_data = contents,
                           )
@app.route('/logout')
def logout() -> 'html':
    session.pop('logged_in')
    title = 'You are now logged out'
    return  render_template('logout.html',
                             the_title = title)


app.secret_key = 'GuesMySecretKey'

if __name__ == '__main__':
    app.run(debug=True)
