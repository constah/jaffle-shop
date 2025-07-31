from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import jaffle_shop_dbt_assets
from .project import jaffle_shop_project
from .schedules import schedules
from .load_exchange_rates import load_exchange_rates_api_op

defs = Definitions(
    assets=[jaffle_shop_dbt_assets],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=jaffle_shop_project),
    },
)

