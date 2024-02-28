import streamlit as st
import pandas as pd
import numpy as np
import google.auth.transport.requests
import google.oauth2.id_token
from google.cloud import storage
import io
import os

from streamlit.web.server.websocket_headers import _get_websocket_headers
from streamlit.web.server.server import Server
from streamlit.runtime import get_instance
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx

DATE_COLUMN = 'date/time'

iap_jwt_expected_audience = os.getenv('IAP_EXPECTED_AUDIENCE')
assert iap_jwt_expected_audience, "⚠️ No IAP expected audience set for JWT validation"

def get_streamlit_session():
    runtime = get_instance()
    session_id = get_script_run_ctx().session_id
    session_info = runtime._session_mgr.get_session_info(session_id)
    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    
    return session_info

def validate_iap_jwt(iap_jwt, expected_audience):
    print(f'Validating JWT: {iap_jwt}')
    #https://cloud.google.com/iap/docs/query-parameters-and-headers-howto#testing_jwt_verification
    try:
        decoded_jwt = google.oauth2.id_token.verify_token(
            iap_jwt, google.auth.transport.requests.Request(), audience=expected_audience,
            certs_url='https://www.gstatic.com/iap/verify/public_key')
        print (f'Decoded JWT: {decoded_jwt}')
        return (decoded_jwt['sub'], decoded_jwt['email'], '')
    except Exception as e:
        return (None, None, '**ERROR: JWT validation error {}**'.format(e))


@st.cache_data
def load_data(nrows):
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(os.getenv('BUCKET'))
    # Construct a client-side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` in that it doesn't
    # retrieve metadata from Google Cloud Storage. As we don't use metadata in
    # this example, using `Bucket.blob` is preferred here.
    file_obj = io.BytesIO()
   
    blob = bucket.blob(os.getenv('FILE'))  
    blob.download_to_file(file_obj)
    file_obj.seek(0)
    
    data = pd.read_csv(file_obj, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


def main():

  st.title('Streamlit Demo -- Uber pickups in NYC')

  streamlit_session = get_streamlit_session()
  headers = _get_websocket_headers()
  iap_jwt_assertion_header_value = headers.get("X-Goog-Iap-Jwt-Assertion")
  iap_authenticated_userid_header_value = headers.get("X-Goog-Authenticated-User-Id")
  iap_authenticated_useremail_header_value = headers.get("X-Goog-Authenticated-User-Email")
  iap_jwt_assertion_header_user_id, iap_jwt_assertion_header_user_email, iap_jwt_verification_error_str = validate_iap_jwt(iap_jwt_assertion_header_value, iap_jwt_expected_audience)
  


  if iap_jwt_verification_error_str is not None:
      print(iap_jwt_verification_error_str)

  data_load_state = st.text('Loading data...')
  data = load_data(10000)
  data_load_state.text("Done! (using st.cache_data)")

  if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

  st.subheader('Number of pickups by hour')
  hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
  st.bar_chart(hist_values)

  # Some number in the range 0-23
  hour_to_filter = st.slider('hour', 0, 23, 17)
  filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

  st.subheader('Map of all pickups at %s:00' % hour_to_filter)
  st.map(filtered_data)

if __name__ == "__main__":
  main()
