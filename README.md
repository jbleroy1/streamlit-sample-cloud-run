# Streamlit app to visualize Uber pickups in NYC

This app uses the Streamlit framework to visualize data about Uber pickups in NYC. The data is loaded from a CSV file in Cloud Storage and then displayed in a variety of ways, including a map of all pickups and a histogram of the number of pickups by hour.

## Prerequisites

To run this app, you will need the following:

* A Google Cloud Platform project
* The Streamlit CLI installed
* A Python 3 environment

## Instructions

To run the app, follow these steps:

1. Clone the repository to your local machine:
````
git clone https://github.com/GoogleCloudPlatform/streamlit-cloud-run-app.git
````

2. Change directory to the directory that contains the app code:
````
cd streamlit-cloud-run-app
````
3. Install the dependencies:
````
pip install -r requirements.txt
````
4. Set the value for  audience, bucket name, and file


````
export IAP_EXPECTED_AUDIENCE=<YOUR IAP AUDIENCE>
export BUCKET=<GCS BUCKET NAME>
export FILE=<GCS file name>
````
5. Run the app:
````
streamlit run app.py
````

6. Open the app in your browser:
````
http://localhost:8501
````

## Usage

The app has two main features:

* A map of all Uber pickups in NYC
* A histogram of the number of pickups by hour

To use the app, simply select the hour you want to view from the slider and then click the "Filter" button. The map will be updated to show all pickups that occurred during the selected hour. The histogram will also be updated to show the number of pickups by hour.

## Contributing

If you would like to contribute to this app, please fork the repository and submit a pull request.

## License

This app is licensed under the Apache License, Version 2.0.
