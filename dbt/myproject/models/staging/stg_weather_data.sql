{{ config(
    materialized='table',
    unique_key='id'
) }}

with source as(
select * from {{ source('dev', 'raw_weather_data') }}
),

dedupe as (
    select *,
    row_number() over (partition by time order by inserted_at) as row_num 
    from source
)

select 
    id,
    city,
    temperature,
    wind_speed,
    weather_description,
    time as weather_time_local,
    (inserted_at + (utc_offset || ' hours')::interval) as inserted_at_local
from dedupe
where row_num = 1