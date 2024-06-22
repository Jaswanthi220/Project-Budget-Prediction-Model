from flask import Flask, jsonify,request
import requests
app = Flask(__name__)
projects = [
    {
      "Sector": "Agricultural credit",
      "Project Title": "Agricultural Refinance and Development Corporation Credit Project (05)",
      "Project ID": "P009828",
      "Project Status": "Closed",
      "Approval Year": "25-Feb-86",
      "Closing Year": "30-Jun-91",
      "Duration(in Months)": "65",
      "Year": "1986",
      "GDP in (Billion) $": "248.99",
      "Per Capita in rupees": "24800",
      "Growth%": "4.78",
      "Commitment Amount(in million)": "375"
    }
]

@app.route('/projects',methods=['GET'])
def get_projects():
    return jsonify(projects)
#Running on http://127.0.0.1:5000

@app.route('/projects/<string:project_id>',methods = ['GET'])
def get_projects_by_id(project_id):
    project = next((p for p in projects if p["Project ID"] == project_id),None)
    if project:
        return jsonify({"project":project})
    else:
        return jsonify({"error":" Project Not Found"}),404

@app.route('/projects', methods=['POST'])
def create_project():
    new_project = request.get_json()
    projects.append(new_project)
    return jsonify({"message": "Project created successfully"})

if __name__ == '__main__' :
    app.run(debug=True)