import requests
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from .settings  import postgresql_connection_string,exchange_rates_api_key
from dagster import asset,op,job,ScheduleDefinition,AssetExecutionContext,In,Nothing

def load_exchange_rates_to_postgres(api_key, db_connection_string):
    try:
        # Fetch exchange rates from the API
        base_currency = "KES"
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
        
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            rates = data["conversion_rates"]
            current_date = datetime.now().date()  # Use local current date
            benchmark_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Use local current date and time

            # Prepare the data, each currency as a row with currency code and exchange rate
            exchange_data = [
                {"benchmark_date": current_date, "currency": "KES", "rate": rates["KES"], "cur_code": 81, "exchange_rate": 1 / rates["KES"], "etl_date": benchmark_date},
                {"benchmark_date": current_date, "currency": "USD", "rate": rates["USD"], "cur_code": 82, "exchange_rate": 1 / rates["USD"], "etl_date": benchmark_date},
                {"benchmark_date": current_date, "currency": "TZS", "rate": rates["TZS"], "cur_code": 83, "exchange_rate": 1 / rates["TZS"], "etl_date": benchmark_date},
                {"benchmark_date": current_date, "currency": "UGX", "rate": rates["UGX"], "cur_code": 84, "exchange_rate": 1 / rates["UGX"], "etl_date": benchmark_date},
                {"benchmark_date": current_date, "currency": "EUR", "rate": rates["EUR"], "cur_code": 101, "exchange_rate": 1 / rates["EUR"], "etl_date": benchmark_date},
                {"benchmark_date": current_date, "currency": "GBP", "rate": rates["GBP"], "cur_code": 85, "exchange_rate": 1 / rates["GBP"], "etl_date": benchmark_date},
            ]

            # Convert the list of dictionaries to a DataFrame
            df = pd.DataFrame(exchange_data)

            # Connect to PostgreSQL
            conn = create_engine(db_connection_string)
            with conn.begin() as connection:
                # Delete existing records for the current date to ensure idempotency
                delete_query = f"DELETE FROM staging.stg_exchange_rates WHERE benchmark_date = '{current_date}';"
                connection.execute(delete_query)
                
                # Insert new data
                df.to_sql(schema='staging', name='stg_exchange_rates', con=connection, if_exists='append', index=False, method='multi')

            print("Exchange rates inserted successfully.")

        else:
            print(f"Error fetching exchange rates: {data.get('error-type', 'Unknown error')}")
            return

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to ExchangeRate-API: {e}")
    
    except SQLAlchemyError as e:
        print(f"Error inserting data into PostgreSQL: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Usage
@op(ins={"start": In(Nothing)},
    name="load_exchange_rates",description="Pulls current/latest exchange rates from the exchange rates API into the warehouse")
def load_exchange_rates_api_op():
    api_key = exchange_rates_api_key
    db_connection_string = postgresql_connection_string
    load_exchange_rates_to_postgres(api_key, db_connection_string)
