install.packages(c('OnboardClient', 'lubridate'))          # install whatever libraries you don't already have
library(OnboardClient)
library(lubridate)                                      # for datetime handling

api.setup()                                             # will prompt for api key
query <- PointSelector()                                # create point selector
query$point_types       <- c('Zone Temperature')        # can list multiple points
query$equipment_types   <- c('fcu')                     # types, equipment types,
query$buildings         <- c('Laboratory')               # buildings, etc.
selection <- select_points(query)

start <- as_datetime("2022-03-29 00:00:00", tz = "UTC")
end <- as_datetime("2022-07-29 00:00:00", tz = "UTC")

sensor_data <- get_timeseries(start_time = start, end_time = end, point_ids = selection$points) #Queries timeseries data for the selection list we got above