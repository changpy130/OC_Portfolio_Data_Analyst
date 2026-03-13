-- Table finale d'analyse

{{ config(materialized='table') }}

WITH source AS (
    SELECT * FROM {{ ref('int_etudiants_insee_joined') }}
),

-- CTE : gender par année
gender AS (
    SELECT
        YEAR,
        SUM(NB_ETUDIANTS) AS NB_ETUDIANTS,
        ROUND(
            SUM(CASE WHEN GENDER = 'F' THEN NB_ETUDIANTS ELSE 0 END) * 100.0
            / SUM(NB_ETUDIANTS),
            3
        ) AS PCT_FEMMES_OC,
        ROUND(
            SUM(CASE WHEN GENDER = 'F' THEN POPULATION_INSEE ELSE 0 END) * 100.0
            / SUM(POPULATION_INSEE),
            3
        ) AS PCT_FEMMES_INSEE,
        ROUND(
            SUM(CASE WHEN GENDER = 'M' THEN NB_ETUDIANTS ELSE 0 END) * 100.0
            / SUM(NB_ETUDIANTS),
            3
        ) AS PCT_HOMMES_OC,
        ROUND(
            SUM(CASE WHEN GENDER = 'M' THEN POPULATION_INSEE ELSE 0 END) * 100.0
            / SUM(POPULATION_INSEE),
            3
        ) AS PCT_HOMMES_INSEE,
        ROUND(
            SUM(CASE WHEN GENDER = 'Non renseigné' THEN NB_ETUDIANTS ELSE 0 END) * 100.0
            / SUM(NB_ETUDIANTS),
            3
        ) AS PCT_NON_RENSEIGNE
        FROM
            source
        GROUP BY YEAR
),

-- CTE : age group
age_by_year AS (
    SELECT
        YEAR,
        AGE_GROUP,
        SUM(NB_ETUDIANTS) AS NB_ETUDIANTS
    FROM 
        source
    GROUP BY YEAR, AGE_GROUP
),
age_final AS (
    SELECT DISTINCT
        YEAR,
        FIRST_VALUE(AGE_GROUP) OVER (
            PARTITION BY YEAR
            ORDER BY NB_ETUDIANTS DESC
        ) AS AGE_GROUP_MAJORITAIRE,
        FIRST_VALUE(NB_ETUDIANTS) OVER (
            PARTITION BY YEAR
            ORDER BY NB_ETUDIANTS DESC
        ) AS NB_AGE_MAJORITAIRE
    FROM 
        age_by_year
),

-- CTE : région
region_by_year AS (
    SELECT
        YEAR,
        REGION,
        SUM(NB_ETUDIANTS) AS NB_ETUDIANTS
    FROM
        source
    GROUP BY YEAR, REGION
),
region_final AS (
    SELECT DISTINCT
        YEAR,
        FIRST_VALUE(REGION) OVER (
            PARTITION BY YEAR
            ORDER BY NB_ETUDIANTS DESC
        ) AS REGION_MAJORITAIRE,
        FIRST_VALUE(NB_ETUDIANTS) OVER (
            PARTITION BY YEAR
            ORDER BY NB_ETUDIANTS DESC
        ) AS NB_REGION_MAJORITAIRE
    FROM
        region_by_year
    WHERE NB_ETUDIANTS IS NOT NULL
)

-- table finale
SELECT  
    g.YEAR,
    g.NB_ETUDIANTS,
    g.PCT_FEMMES_OC,
    g.PCT_FEMMES_INSEE,
    g.PCT_HOMMES_OC,
    g.PCT_HOMMES_INSEE,
    g.PCT_NON_RENSEIGNE,
    a.AGE_GROUP_MAJORITAIRE,
    ROUND(
        a.NB_AGE_MAJORITAIRE * 100.0
        / g.NB_ETUDIANTS,
        3
    ) AS PCT_AGE_GROUP_MAJORITAIRE,
    r.REGION_MAJORITAIRE,
    ROUND(
        r.NB_REGION_MAJORITAIRE * 100.0
        / g.NB_ETUDIANTS,
        3
    ) AS PCT_REGION_MAJORITAIRE
FROM
    gender g
LEFT JOIN age_final a
    ON g.YEAR = a.YEAR
LEFT JOIN region_final r
    ON g.YEAR = r.YEAR
ORDER BY YEAR