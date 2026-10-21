{# Use the layer name as the schema (staging, marts) instead of dbt's default main_staging. #}
{% macro generate_schema_name(custom_schema_name, node) -%}
    {{ (custom_schema_name or target.schema) | trim }}
{%- endmacro %}
