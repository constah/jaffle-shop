select
        id as order_id,
        user_id as customer_id,
        order_date::date,
        status
    from {{source('staging', 'raw_orders')}}