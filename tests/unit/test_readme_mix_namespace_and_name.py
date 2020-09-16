import gcip
from tests import conftest


def job_for(service: str) -> gcip.Job:
    return gcip.Job(name="update_service", script=f"./update-service.sh {service}")


def test():
    pipeline = gcip.Pipeline()
    for env in ["development", "test"]:
        pipeline.add_jobs(job_for(env), namespace=env, name="service1")
        pipeline.add_jobs(job_for(env), namespace=env, name="service2")

    output = pipeline.render()
    # print(output)
    assert conftest.dict_a_contains_b(
        a=output,
        b={
            'stages': ['update_service_development', 'update_service_test'],
            'update-service-development-service1': {
                'script': ['./update-service.sh development'],
                'stage': 'update_service_development'
            },
            'update-service-development-service2': {
                'script': ['./update-service.sh development'],
                'stage': 'update_service_development'
            },
            'update-service-test-service1': {
                'script': ['./update-service.sh test'],
                'stage': 'update_service_test'
            },
            'update-service-test-service2': {
                'script': ['./update-service.sh test'],
                'stage': 'update_service_test'
            }
        },
    )
