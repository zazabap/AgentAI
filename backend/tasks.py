from prefect import task, flow
import os
import shutil

# @task
# def process_file(file_path):
#     dest = os.path.join("/app/data/processed", os.path.basename(file_path))
#     os.makedirs(os.path.dirname(dest), exist_ok=True)
#     shutil.move(file_path, dest)
#     return dest

# def run_workflow(task_input, suggestion):
#     with Flow("automation") as flow:
#         if "file" in task_input.lower():
#             result = process_file("/app/data/input/sample.txt")
#     flow_state = flow.run()
#     return flow_state.result[result].result if "result" in locals() else "No action taken"


@task
def process_file(file_path):
    dest = os.path.join("data/processed", os.path.basename(file_path))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.move(file_path, dest)
    return dest

@flow
def run_workflow(task_input, suggestion):
    if "file" in task_input.lower():
        result = process_file("data/input/sample.txt")
        return result
    else:
        return "No action taken"