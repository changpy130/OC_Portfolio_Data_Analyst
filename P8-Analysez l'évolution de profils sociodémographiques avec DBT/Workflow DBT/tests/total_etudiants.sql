-- Vérifier que le nombre total d'étudiants uniques est bien 4010 après la jointure

WITH source AS (
    SELECT * FROM {{ ref('fct_profil_sociodem') }}
),

total_etudiants AS (
    SELECT
        SUM(NB_ETUDIANTS) AS total
    FROM
        source
)

SELECT
    *
FROM
    total_etudiants
WHERE total != 4010