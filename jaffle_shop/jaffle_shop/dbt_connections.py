import os
import subprocess
from dagster import (Definitions,ScheduleDefinition ,job,AssetExecutionContext,op,asset,AssetKey,define_asset_job,AssetSelection,Out, In, Nothing)
from dagster_dbt import DbtCliResource  
#pip install dagster-dbt

#define dbt resource. point to the dbt project directory
dbt_resource=DbtCliResource(project_dir="/Users/constah/Documents/infolab/projectsv1.0/infolab/")

#run all models(dbt run)
@op(required_resource_keys={"dbt"},
    ins={"start": In(Nothing)})
def run_dbt_models(context):
    # Running dbt run without specifying models to run all models
    result = context.resources.dbt.cli(["run"])
    context.log.info(result)

#run select models(dbt run --select dim_branch sample_revenue_ssot)
@op(required_resource_keys={"dbt"},
    ins={"start": In(Nothing)})
def run_multiple_dbt_models_op(context):
    # Space-separated string of models
    models_to_run = "dim_branch sample_revenue_ssot"
    # Using cli command to run selected models
    result = context.resources.dbt.cli(["run", "--select", models_to_run])
    context.log.info(result) 

# Operation to run dbt docs generate(dbt docs generate)
@op
def generate_dbt_docs_op(context):
    # Manually invoke dbt docs generate using subprocess
    result = subprocess.run(["dbt", "docs", "generate"], cwd="/Users/constah/Documents/infolab/projectsv1.0/infolab/", capture_output=True, text=True)
    
    if result.returncode == 0:
        context.log.info("Successfully generated dbt docs.")
    else:
        context.log.error(f"Failed to generate dbt docs: {result.stderr}")
        raise Exception(f"dbt docs generate failed: {result.stderr}")

