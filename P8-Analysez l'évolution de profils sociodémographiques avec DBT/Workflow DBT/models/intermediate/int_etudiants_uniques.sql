-- Choisir des étudiants(USER_ID) distincts
-- Avec la première inscription(YEAR_PATH_STARTED)

{{ config(materialized='view') }} 

with stg AS (
    SELECT * FROM {{ ref('stg_etudiants') }}
),

ranked AS (
    SELECT *,
    row_number() OVER (
        PARTITION BY USER_ID
        ORDER BY YEAR_PATH_STARTED ASC
    ) AS rank_num
    FROM stg
)

SELECT * 
FROM ranked
WHERE rank_num = 1