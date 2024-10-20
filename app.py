import os  # Add this line

import webbrowser
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///checklist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    checked = db.Column(db.Boolean, default=False)

@app.route('/')
def checklist():
    rules = Rule.query.all()
    return render_template('checklist.html', rules=rules)

@app.route('/add_rule', methods=['POST'])
def add_rule():
    new_rule = request.form['new_rule']
    rule = Rule(text=new_rule)
    db.session.add(rule)
    db.session.commit()
    return redirect('/')

@app.route('/toggle_rule/<int:rule_id>', methods=['POST'])
def toggle_rule(rule_id):
    rule = Rule.query.get(rule_id)
    if rule:
        data = request.get_json()
        rule.checked = data['checked']
        db.session.commit()
    return jsonify(success=True)

@app.route('/delete_rule/<int:rule_id>', methods=['POST'])
def delete_rule(rule_id):
    rule = Rule.query.get(rule_id)
    if rule:
        db.session.delete(rule)
        db.session.commit()
    return redirect('/')

@app.route('/reset_rules', methods=['POST'])
def reset_rules():
    rules = Rule.query.all()
    for rule in rules:
        rule.checked = False
    db.session.commit()
    return redirect('/')

@app.route('/delete_all', methods=['POST'])
def delete_all():
    db.session.query(Rule).delete()  # Deletes all rules from the database
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")  # This line will open the browser
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
