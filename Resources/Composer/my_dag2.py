from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
from random import randint
def _choosing_best_model(**kwargs):
    ti = kwargs['ti']
    accuracies = ti.xcom_pull(task_ids=[
        'training_model_A',
        'training_model_B',
        'training_model_C'
    ])
    if max(accuracies) > 8:
        return 'accurate'
    return 'inaccurate'

def _training_model(model):
    return randint(1, 10)

with DAG("my_dag2", start_date=datetime(2021, 11 , 26),
    schedule_interval='@daily', catchup=False) as dag:
    #training_model_tasks = [ PythonOperator( task_id=f"training_model_{model_id}", python_callable=_training_model, op_kwargs={ "model": model_id } ) for model_id in ['A', 'B', 'C'] ]
    training_model_A = PythonOperator(
        task_id="training_model_A",
        python_callable=_training_model,
        op_kwargs={"model": "A"}
    )
    training_model_B = PythonOperator(
        task_id="training_model_B",
        python_callable=_training_model,
        op_kwargs={"model": "B"}
    )
    training_model_C = PythonOperator(
        task_id="training_model_C",
        python_callable=_training_model,
        op_kwargs={"model": "C"}
    )

    choosing_best_model = BranchPythonOperator(
        task_id="choosing_best_model",
        python_callable=_choosing_best_model,
        #xcom_push=True,
        dag=dag,
        provide_context=True
    )
    accurate = BashOperator(
        task_id="accurate",
        bash_command="echo 'accurate'"
    )
    inaccurate = BashOperator(
        task_id="inaccurate",
        bash_command=" echo 'inaccurate'"
    )

    [training_model_A, training_model_B, training_model_C] >> choosing_best_model >> [accurate, inaccurate]
