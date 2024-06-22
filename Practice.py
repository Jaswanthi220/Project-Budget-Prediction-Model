import requests

api_url = "http://127.0.0.1:5000/projects"
data = {
    "Sector": "Agricultural credit",
    "Project Title": "Agricultural Refinance and Development Corporation Credit Project (04)",
    "Project ID": "P009784",
    "Project Status": "Closed",
    "Approval Year": "23-Feb-82",
    "Closing Year": "30-Jun-84",
    "Duration(in Months)": "28",
    "Year": "1982",
    "GDP in (Billion) $": "200.72",
    "Per Capita in rupees": "21920",
    "Growth%": "3.48",
    "Commitment Amount(in million)": "350"
}

try:
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        try:
            print(response.json())
        except requests.exceptions.JSONDecodeError as json_error:
            print(f"Error decoding JSON: {json_error}")
    else:
        print(f"Request failed with status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error making request: {e}")