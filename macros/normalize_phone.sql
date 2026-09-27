{% macro normalize_phone(column_name) %}
    regexp_replace({{ column_name }}, '[^0-9+]', '')
{% endmacro %}
