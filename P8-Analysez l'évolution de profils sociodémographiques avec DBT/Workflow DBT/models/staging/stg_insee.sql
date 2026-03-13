-- Données de population INSEE par région, tranche d'âge et genre
-- Source : INSEE - Estimations de population 2022-2025
-- Harmonisation des catégories effectuée en amont (Python)

WITH source AS (
    SELECT * FROM {{ source('raw_data', 'INSEE_POPULATION') }}
)

SELECT
    *
FROM 
    source