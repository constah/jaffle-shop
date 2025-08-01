
with customers as (
    select * from
        {{ ref('ods_customer') }}
),
customer_orders as ( 
    select
        * from
        {{ ref('ods_customer_orders') }}  

),
final as (
    select
        c.customer_id,
        c.first_name,
        c.last_name,
        co.first_order_date,
        co.most_recent_order_date,
        coalesce(co.number_of_orders, 0) as number_of_orders
    from customers c
    left join customer_orders co on c.customer_id=co.customer_id
)
{{
  config(
    materialized='table'
  )
}}
select * from final