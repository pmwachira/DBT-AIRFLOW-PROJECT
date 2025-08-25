{{config(
    materialized='table',
    unique_key='id'
)}}


select 
city,
temperature,
wind_speed,
weather_description,
weather_time_local
from 
{{ ref('stg_weather_data')}}