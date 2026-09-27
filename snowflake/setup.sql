-- Example Snowflake bootstrap for the portfolio project.
create database if not exists CUSTOMER360;
create schema if not exists CUSTOMER360.RAW;
create schema if not exists CUSTOMER360.ANALYTICS;
create schema if not exists CUSTOMER360.SNAPSHOTS;

-- In a real environment, grant only the privileges required by the dbt role.
