import pandas as pd
from onboard.client import OnboardClient
from onboard.client.dataframes import points_df_from_streaming_timeseries
from onboard.client.models import PointSelector, TimeseriesQuery, PointData
from datetime import datetime, timezone, timedelta
from typing import List
import pytz
from key import api_key

client = OnboardClient(api_key=api_key)

print(list(pd.DataFrame(client.get_all_buildings())['name'])) # returns list of buildings that you have access to (you may not have 'Laboratory' in your set)

query = PointSelector()
query.point_types     = ['Zone Temperature'] # can list multiple point
query.equipment_types = ['fcu']              # types, equipment types,
query.buildings       = ['Laboratory']       # buildings, etc.
selection = client.select_points(query)

start = pd.Timestamp("2022-03-29 00:00:00", tz="utc")
end = pd.Timestamp("2022-07-29 00:00:00", tz="utc")

timeseries_query = TimeseriesQuery(point_ids = selection['points'], start = start, end = end)
sensor_data = points_df_from_streaming_timeseries(client.stream_point_timeseries(timeseries_query))