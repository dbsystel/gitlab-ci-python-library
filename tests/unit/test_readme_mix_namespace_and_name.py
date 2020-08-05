import gcip


def job_for(service: str) -> gcip.Job:
    return gcip.Job(name="update_service", script=f"./update-service.sh {service}")


def test():
    pipeline = gcip.Pipeline()
    for env in ["development", "test"]:
        pipeline.add_job(job_for(env), namespace=env, name="service1")
        pipeline.add_job(job_for(env), namespace=env, name="service2")

    pipeline.print_yaml()
