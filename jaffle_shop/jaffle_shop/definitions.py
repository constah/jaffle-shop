from dagster import Definitions,job
from dagster_dbt import DbtCliResource,dbt_run_op ,dbt_cli_resource
from .assets import jaffle_shop_dbt_assets
from .project import jaffle_shop_project
from .schedules import schedules
from .load_exchange_rates import load_exchange_rates_api_op
from .dbt_connections import run_multiple_dbt_models_op,generate_dbt_docs_op

#define dbt resource
dbt_resource=dbt_cli_resource.configured({"project_dir":"/Users/constah/Documents/infolab/infolab/"})

#run entire dbt project by passing dbt run
@job(resource_defs={"dbt": dbt_resource})
def my_dbt_project_job():
    run_multiple_dbt_models_op()
    generate_dbt_docs_op()

defs = Definitions(
    assets=[jaffle_shop_dbt_assets], 
    schedules=schedules,
    jobs=[my_dbt_project_job],
    resources={
        "dbt": DbtCliResource(project_dir=jaffle_shop_project),
    },
)

