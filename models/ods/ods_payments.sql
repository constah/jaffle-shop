select * from 
{{ source('staging', 'raw_payments') }} 