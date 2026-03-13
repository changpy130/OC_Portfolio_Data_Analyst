-- Jointure complète entre les étudiants OC et la population INSEE
-- FULL OUTER JOIN pour conserver :
--   - les étudiants "Non renseigné" (présents dans OC uniquement)
--   - les régions sans étudiants OC comme la Corse (présentes dans INSEE uniquement)


{{ config(materialized='view') }} 

WITH etudiants AS (
    SELECT * FROM {{ ref('stg_etudiants') }}
),

insee AS (
    SELECT * FROM {{ ref('stg_insee') }}
),

etudiants_agg AS (
    SELECT
        YEAR_PATH_STARTED AS YEAR,
        REGION,
        AGE_GROUP,
        GENDER,
        COUNT(USER_ID) AS NB_ETUDIANTS
    FROM
       etudiants 
    GROUP BY 1, 2, 3 , 4
)

SELECT
    COALESCE(e.YEAR, i.YEAR) AS YEAR,
    COALESCE(e.REGION, i.REGION) AS REGION,
    COALESCE(e.AGE_GROUP, i.AGE_GROUP) AS AGE_GROUP,
    COALESCE(e.GENDER, i.GENDER) AS GENDER,
    e.NB_ETUDIANTS,
    i.POPULATION AS POPULATION_INSEE
FROM 
    etudiants_agg e
FULL OUTER JOIN
    insee i
    ON
        e.YEAR = i.YEAR
    AND
        e.REGION = i.REGION
    AND
        e.AGE_GROUP = i.AGE_GROUP
    AND
        e.GENDER = i.GENDER
ORDER BY YEAR, REGION, AGE_GROUP, GENDER