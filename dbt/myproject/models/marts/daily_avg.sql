{{
    config(
        materialized='table'
    )
}}

select 
 city,
 date(weather_time_local) as weather_date,
round(avg(temperature)::numeric,2) as avg_temperature,
round(avg(wind_speed)::numeric,2) as avg_wind_speed
from {{ ref('stg_weather_data') }}
group by 1, 2
order by 1,2