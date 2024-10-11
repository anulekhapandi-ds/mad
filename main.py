from flask import Flask, render_template,request, redirect, url_for, flash

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the provided credentials match
        if username == "1" and password == "1":
            return render_template('admin_dashboard.html')
        else:
            flash('Invalid username or password!') 
            return render_template('admin_login.html')
    return render_template('admin_login.html')

@app.route('/professional/login')
def professional_login():
    return render_template('professional_login.html')

@app.route('/customer/login')
def customer_login():
    return render_template('customer_login.html')

@app.route('/professional/register')
def professional_register():
    return render_template('professional_register.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
