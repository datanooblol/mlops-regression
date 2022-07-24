from dagster import pipeline, solid

@solid
def get_name() -> str:
    return "dagster"

@solid
def hello(context, name:str) -> None:
    context.log.info(f"Hello, {name}!")
    
@pipeline
def hello_pipeline():
    name = get_name()
    hello(name)