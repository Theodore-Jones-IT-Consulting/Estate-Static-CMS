from flask import Flask, jsonify, request, render_template, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"agents": [], "listings": []}
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', agents=data['agents'], listings=data['listings'])

@app.route('/add/agent', methods=['GET', 'POST'])
def add_agent():
    if request.method == 'POST':
        new_agent = request.form.to_dict()
        new_agent['homepage'] = 'homepage' in request.form
        data = load_data()
        data['agents'].append(new_agent)
        save_data(data)
        return redirect(url_for('index'))
    return render_template('add_agent.html')

@app.route('/add/listing', methods=['GET', 'POST'])
def add_listing():
    if request.method == 'POST':
        new_listing = request.form.to_dict()
        data = load_data()
        data['listings'].append(new_listing)
        save_data(data)
        return redirect(url_for('index'))
    return render_template('add_listing.html')

@app.route('/edit/agent/<int:agent_index>', methods=['GET', 'POST'])
def edit_agent(agent_index):
    data = load_data()
    agent = data['agents'][agent_index]
    if request.method == 'POST':
        updated_agent = request.form.to_dict()
        updated_agent['homepage'] = 'homepage' in request.form
        data['agents'][agent_index] = updated_agent
        save_data(data)
        return redirect(url_for('index'))
    return render_template('edit_agent.html', agent=agent, agent_index=agent_index)

@app.route('/edit/listing/<int:listing_index>', methods=['GET', 'POST'])
def edit_listing(listing_index):
    data = load_data()
    listing = data['listings'][listing_index]
    if request.method == 'POST':
        updated_listing = request.form.to_dict()
        updated_listing['agent'] = data['agents'][int(request.form['agent'])]  # Associate agent with the listing
        data['listings'][listing_index] = updated_listing
        save_data(data)
        return redirect(url_for('index'))
    return render_template('edit_listing.html', listing=listing, listing_index=listing_index, agents=data['agents'])

@app.route('/listings')
def listings():
    data = load_data()
    return render_template('listings.html', listings=data['listings'], agents=data['agents'])

@app.route('/agents')
def agents():
    data = load_data()
    return render_template('agents.html', agents=data['agents'])

if __name__ == '__main__':
    app.run(debug=True)
