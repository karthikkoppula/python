import dash
from dash import html
from dash.dependencies import Input, Output
import requests

# Assuming your Flask app is running on localhost and port 5000
flask_app_url = "http://10.61.93.223:5000"

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of your Dash app
app.layout = html.Div(
    [
        html.Button("Fetch Data", id="fetch-button"),
        html.Div(id="data-display"),
    ]
)

# Define a callback to fetch data when the button is clicked
@app.callback(
    Output("data-display", "children"),
    [Input("fetch-button", "n_clicks")]
)
def fetch_data(n_clicks):
    if n_clicks is None:
        return "Click the button to fetch data."

    try:
        # Make an HTTP GET request to the /fetch_dtdash endpoint
        response = requests.get(f"{flask_app_url}/fetch_dtdash")

        if response.status_code == 200:
            # Data is successfully fetched
            data = response.json()
            # Display the fetched data
            return f"Fetched Data: {data}"
            print(data)

        else:
            # If the request was unsuccessful, display an error message
            return f"Failed to fetch data. Status code: {response.status_code}"

    except Exception as e:
        # Handle any exceptions that may occur during the request
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run_server(debug=True)

