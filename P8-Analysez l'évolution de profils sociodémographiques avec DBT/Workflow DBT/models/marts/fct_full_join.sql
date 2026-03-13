-- Table complète après la jointure

{{ config(materialized='table') }}

WITH source AS (
    SELECT * FROM {{ ref('int_etudiants_insee_joined') }}
)

SELECT
    *
FROM
    source