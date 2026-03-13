-- Nettoyage et standardisation des données étudiants
-- Gestion des valeurs manquantes dans GENDER

WITH source AS (
    SELECT * FROM {{ source('raw_data', 'ETUDIANTS') }}
),

cleaned AS (
    SELECT
        USER_ID,
        PATH_CATEGORY_NAME,
        AGE_GROUP,
        -- Gestion des valeurs manquantes
        CASE 
            WHEN GENDER IS NULL OR GENDER = '' THEN 'Non renseigné'
            ELSE GENDER 
        END AS GENDER,
        -- Harmonisation des noms de région pour jointure INSEE
        CASE 
            WHEN REGION = 'Centre-Val de Loire' THEN 'Centre-Val-de-Loire'
            ELSE REGION 
        END AS REGION,
        YEAR_PATH_STARTED
    FROM source
)

SELECT * FROM cleaned