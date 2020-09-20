from flask import Flask, request, url_for,render_template,request, redirect,flash,session
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
app = Flask(__name__)
app.config.from_pyfile('config.cfg')
app.config['SECRET_KEY']='YourSecretKey'
mail = Mail(app)

urlSTS = URLSafeTimedSerializer(app.config['SECRET_KEY'])


@app.route('/',methods=["GET", "POST"])
def index():

	if request.method == 'POST':
		recipient=request.form.get('email')
		print('email:',recipient)
		sender='Your Email Username'
		token = urlSTS.dumps(recipient, salt='email-confirm')
		msg = Message('Confirm Email', sender=sender, recipients=[recipient])
		link = url_for('confirm_email', token=token, _external=True)
		msg.body = 'Your Email confirmation link {}'.format(link)
		mail.send(msg)
		flash(f'Email confirmation link sent your email', 'success')
		return redirect(url_for('index'))
	return render_template('index.html')



@app.route('/token/<token>', methods=["GET", "POST"])
def confirm_email(token):
    try:
        email = urlSTS.loads(token, salt="email-confirm", max_age=86400)
    except:
        abort(404)
    flash(f'Thanks for confirming your email', 'success')
    return redirect(url_for('index'))
    

if __name__ == '__main__':
    app.run(debug=True)
