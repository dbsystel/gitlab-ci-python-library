import gcip


def test():
    pipeline = gcip.Pipeline()

    job = gcip.Job(name="print_date", script="date")
    job.set_image("docker/image:example")
    job.prepend_script("./before-script.sh")
    job.append_script("./after-script.sh")
    job.add_variables(USER="Max Power", URL="https://example.com")
    job.add_tags("test", "europe")
    job.add_rules(gcip.Rule(if_statement="$MY_VARIABLE_IS_PRESENT"))

    pipeline.add_jobs(job)

    pipeline.print_yaml()
