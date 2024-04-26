from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb+srv://maksvin1111:6Ndfv4XtVYw9ax33@cluster0.cnm3lns.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['project_manager']
projects_collection = db['projects']

@app.route('/')
def index():
    projects = projects_collection.find()
    return render_template('index.html', projects=projects)

@app.route('/add_project', methods=['POST'])
def add_project():
    name = request.form['name']
    project = {'name': name, 'stages': []}
    projects_collection.insert_one(project)
    return redirect(url_for('index'))

@app.route('/add_stage/<project_id>', methods=['POST'])
def add_stage(project_id):
    stage_name = request.form['stage_name']
    projects_collection.update_one(
        {'_id': ObjectId(project_id)},
        {'$push': {'stages': {'name': stage_name, 'status': 'not completed'}}}
    )
    return redirect(url_for('index'))

@app.route('/delete_project/<project_id>')
def delete_project(project_id):
    projects_collection.delete_one({'_id': ObjectId(project_id)})
    return redirect(url_for('index'))

@app.route('/delete_stage/<project_id>/<stage_index>')
def delete_stage(project_id, stage_index):
    projects_collection.update_one(
        {'_id': ObjectId(project_id)},
        {'$unset': {f'stages.{stage_index}': 1}}
    )
    projects_collection.update_one(
        {'_id': ObjectId(project_id)},
        {'$pull': {'stages': None}}
    )
    return redirect(url_for('index'))

@app.route('/toggle_stage/<project_id>/<stage_index>')
def toggle_stage(project_id, stage_index):
    project = projects_collection.find_one({'_id': ObjectId(project_id)})
    current_status = project['stages'][int(stage_index)]['status']
    new_status = 'completed' if current_status == 'not completed' else 'not completed'
    projects_collection.update_one(
        {'_id': ObjectId(project_id)},
        {'$set': {f'stages.{stage_index}.status': new_status}}
    )
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)