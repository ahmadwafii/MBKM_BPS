from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
import re


app = Flask(__name__)
app.secret_key = 'ppp1234321'

hostname = 'localhost'
database = 'Db_pstdigital'
username = 'postgres'
pwd = 'Fathur27!!..))'
port = '5432'

conn = psycopg2.connect(dbname = database, user = username, password = pwd, host = hostname, port = port)

@app.route('/')
def main():
    return render_template('index.html')

#@app.route('/home', methods=['GET', 'POST'])
#def home():
    # Check if user is loggedin
    #if 'loggedin' in session:
        #User is loggedin show them the home page
        #return render_template('dashboard_users.html', nama_lengkap=session['nama_lengkap'])
    #User is not loggedin redirect to login page
    #return redirect(url_for('login_user'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('dashboard_users.html')

@app.route('/buku_tamu', methods=['GET', 'POST'])
def buku_tamu(): 
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'nama_lengkap' in request.form and 'nomor_hp' in request.form and 'jenis_kelamin' in request.form and 'tanggal_masuk' in request.form:
        # Create variables for easy access
        nama_lengkap = request.form['nama_lengkap']
        nomor_hp = request.form['nomor_hp']
        jenis_kelamin = request.form['jenis_kelamin']
        tanggal_masuk = request.form['tanggal_masuk']

        if not nama_lengkap or not nomor_hp or not jenis_kelamin or not tanggal_masuk:
            flash('Silakan isi semua kolom.')
        else:
            cursor.execute("INSERT INTO tamu (nama_lengkap, nomor_handphone, jeniskelamin, tanggal_input) VALUES (%s, %s, %s, %s)", (nama_lengkap, nomor_hp, jenis_kelamin, tanggal_masuk))
            conn.commit()
            flash('Data berhasil disimpan.')
            return redirect(url_for('home'))
    # Show registration form with message (if any)
    return render_template('buku.html')

@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'nama_lengkap' in request.form and 'password' in request.form:
        nama_lengkap = request.form['nama_lengkap']
        password = request.form['password']
        print(password)
 
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE nama_lengkap = %s', (nama_lengkap, ))
        # Fetch one record and return result
        account = cursor.fetchone()
        
 
        if account:
            password_rs = account['password']
            print(password_rs)
            # If account exists in users table in out database
            if check_password_hash(password_rs, password):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['nama_lengkap'] = account['nama_lengkap']
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Nama Lengkap / Password terdapat kesalahan!')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Nama Lengkap / Password terdapat kesalahan!')
    return render_template('login_user.html')

@app.route('/registrasi', methods=['GET', 'POST'])
def registrasi():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'nama_lengkap' in request.form and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        nama_lengkap = request.form['nama_lengkap']
        email = request.form['email']
        password = request.form['password']
    
        _hashed_password = generate_password_hash(password)
 
        #Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE nama_lengkap = %s AND email = %s', (nama_lengkap, email, ))
        account = cursor.fetchone()
        print(account)

        # If account exists show error and validation checks
        if account:
            flash('Akun tersesbut telah aktif!')
        elif not re.match(r'[A-Za-z0-9]+', nama_lengkap):
            flash('Nama Lengkap hanya boleh berisi karakter dan angka!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Isikan kolom email dengan benar!')
        elif not nama_lengkap or not email or not password:
            flash('Silakan isi formulirnya!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            cursor.execute("INSERT INTO users (nama_lengkap, email, password) VALUES (%s,%s,%s)", (nama_lengkap, email, _hashed_password))
            conn.commit()
            flash('Akun Anda berhasil dibuat!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Silakan isi form tersebut!')

    # Show registration form with message (if any)
    return render_template('registrasi.html')

@app.route('/perpustakaan')
def perpustakaan():
    return render_template('perpustakaan.html')

@app.route('/pembelian_data')
def pembelian_data():
    return render_template('pembelian_data.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('nama_lengkap', None)
   # Redirect to login page
   return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)