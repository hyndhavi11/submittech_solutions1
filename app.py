from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from datetime import datetime
import config

app = Flask(__name__)
app.config.from_object(config.Config)
mysql = MySQL(app)

# Helper function to get user ID from session
def get_user_id():
    return session.get('user_id')

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('medications'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        
        if user:
            session['user_id'] = user[0]
            flash('Login successful!', 'success')
            return redirect(url_for('medications'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/medications')
def medications():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = get_user_id()
    filter_status = request.args.get('status', '')
    sort_by = request.args.get('sort', 'name')
    
    cur = mysql.connection.cursor()
    
    # Base query
    query = "SELECT * FROM medications WHERE user_id = %s"
    params = [user_id]
    
    # Apply filter
    if filter_status in ['Active', 'Discontinued']:
        query += " AND status = %s"
        params.append(filter_status)
    
    # Apply sorting
    if sort_by == 'name':
        query += " ORDER BY name"
    elif sort_by == 'date':
        query += " ORDER BY start_date DESC"
    
    cur.execute(query, tuple(params))
    medications = cur.fetchall()
    
    # Get summary counts
    cur.execute("SELECT COUNT(*) FROM medications WHERE user_id = %s AND status = 'Active'", (user_id,))
    active_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM medications WHERE user_id = %s AND status = 'Discontinued'", (user_id,))
    discontinued_count = cur.fetchone()[0]
    
    cur.close()
    
    return render_template('medications.html', 
                         medications=medications,
                         active_count=active_count,
                         discontinued_count=discontinued_count,
                         filter_status=filter_status,
                         sort_by=sort_by)

@app.route('/add_medication', methods=['GET', 'POST'])
def add_medication():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        dosage = request.form['dosage']
        frequency = request.form['frequency']
        start_date = request.form['start_date']
        notes = request.form['notes']
        status = request.form['status']
        
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO medications 
            (user_id, name, dosage, frequency, start_date, notes, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (get_user_id(), name, dosage, frequency, start_date, notes, status))
        mysql.connection.commit()
        cur.close()
        
        flash('Medication added successfully!', 'success')
        return redirect(url_for('medications'))
    
    return render_template('add_medication.html')

@app.route('/edit_medication/<int:id>', methods=['GET', 'POST'])
def edit_medication(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        dosage = request.form['dosage']
        frequency = request.form['frequency']
        start_date = request.form['start_date']
        notes = request.form['notes']
        status = request.form['status']
        
        cur.execute("""
            UPDATE medications SET
            name = %s, dosage = %s, frequency = %s, 
            start_date = %s, notes = %s, status = %s
            WHERE id = %s AND user_id = %s
        """, (name, dosage, frequency, start_date, notes, status, id, get_user_id()))
        mysql.connection.commit()
        cur.close()
        
        flash('Medication updated successfully!', 'success')
        return redirect(url_for('medications'))
    
    # GET request - load existing data
    cur.execute("SELECT * FROM medications WHERE id = %s AND user_id = %s", (id, get_user_id()))
    medication = cur.fetchone()
    cur.close()
    
    if not medication:
        flash('Medication not found or access denied.', 'danger')
        return redirect(url_for('medications'))
    
    return render_template('edit_medication.html', medication=medication)

@app.route('/delete_medication/<int:id>')
def delete_medication(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM medications WHERE id = %s AND user_id = %s", (id, get_user_id()))
    mysql.connection.commit()
    cur.close()
    
    flash('Medication deleted successfully!', 'success')
    return redirect(url_for('medications'))

if __name__ == '__main__':
    app.secret_key = config.Config.SECRET_KEY
    app.run(debug=True)