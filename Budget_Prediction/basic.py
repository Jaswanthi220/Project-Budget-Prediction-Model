from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

# Your projects data
projects = [
{
      "Sector": "Agricultural credit",
      "Project Title": "Agricultural Refinance and Development Corporation Credit Project (05)",
      "Project ID": "P009828",
      "Project Status": "Closed",
      "Approval Year": "February 25, 1986",
      "Closing Year": "June 30, 1991",
      "Duration(in Months)": "65",
      "Year": "1986",
      "GDP in (Billion) $": "248.99",
      "Per Capita in rupees": "24800",
      "Growth%": "4.78",
      "Commitment Amount(in million)": "375.0"
    },
    {
      "Sector": "Agricultural credit",
      "Project Title": "National Cooperative Development Corporation Project (03)",
      "Project ID": "P009811",
      "Project Status": "Closed",
      "Approval Year": "June 19, 1984",
      "Closing Year": "June 30, 1992",
      "Duration(in Months)": "97",
      "Year": "1984",
      "GDP in (Billion) $": "212.16",
      "Per Capita in rupees": "22160",
      "Growth%": "3.82",
      "Commitment Amount(in million)": "220.0"
    },
    {
      "Sector": "Agricultural credit",
      "Project Title": "Agricultural Refinance and Development Corporation Credit Project (04)",
      "Project ID": "P009784",
      "Project Status": "Closed",
      "Approval Year": "February 23, 1982",
      "Closing Year": "June 30, 1984",
      "Duration(in Months)": "28",
      "Year": "1982",
      "GDP in (Billion) $": "200.72",
      "Per Capita in rupees": "21920",
      "Growth%": "3.48",
      "Commitment Amount(in million)": "350.0"
    }
]

class Projects(Resource):
    def get(self):
        return jsonify(projects)
#creating API with reference of project_id
class ProjectById(Resource):
    def get(self, project_id):
        project = next((p for p in projects if p["Project ID"] == project_id), None)
        if project:
            return jsonify({"project": project})
        else:
            return jsonify({"error": "Project Not Found"}), 404

#creating API with reference yearof
class ProjectsByYear(Resource):
    def get(self, year):
        # Convert the year parameter to a string
        year_str = str(year)

        # Filter projects by the converted year string
        projects_by_year = [p for p in projects if p["Year"] == year_str]

        return jsonify({"projects": projects_by_year})
#creating API with reference of duration

class ProjectsByDuration(Resource):
    def get(self, duration):
        # Convert the duration parameter to a string
        duration_str = str(duration)

        # Filter projects by duration
        projects_by_duration = [p for p in projects if p["Duration(in Months)"] == duration_str]
        return jsonify({"projects": projects_by_duration})
#creating API with reference of gdp
class ProjectsByGDP(Resource):
    def get(self, gdp):
        # Convert the GDP parameter to a float
        gdp_float = float(gdp)

        # Convert GDP values in the projects data to floats
        projects_float_gdp = [
            {**p, "GDP in (Billion) $": float(p["GDP in (Billion) $"])} for p in projects
        ]

        # Define a small range for GDP comparison
        gdp_range = 0.01  # You can adjust this based on your needs

        # Filter projects by GDP within the range
        projects_by_gdp = [p for p in projects_float_gdp if abs(p["GDP in (Billion) $"] - gdp_float) < gdp_range]
        return jsonify({"projects": projects_by_gdp})
#creating API with reference of gdp and year

class ProjectsByYearAndDuration(Resource):
    def get(self, year, duration):
        # Convert the year parameter to a string
        year_str = str(year)

        # Convert the duration parameter to an integer
        duration_int = int(duration)

        # Filter projects by year and duration
        projects_by_year_and_duration = [
            p for p in projects if p["Year"] == year_str and int(p["Duration(in Months)"]) == duration_int
        ]

        return jsonify({"projects": projects_by_year_and_duration})


api.add_resource(Projects, '/projects')
api.add_resource(ProjectById, '/projects/<string:project_id>')
api.add_resource(ProjectsByYear, '/projects/by_year/<int:year>')
api.add_resource(ProjectsByDuration, '/projects/by_duration/<int:duration>')
api.add_resource(ProjectsByGDP, '/projects/by_gdp/<float:gdp>')
api.add_resource(ProjectsByYearAndDuration, '/projects/by_year_and_duration/<int:year>/<int:duration>')


if __name__ == '__main__':
    app.run(debug=True)
