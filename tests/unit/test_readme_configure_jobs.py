import gcip

def test():
    pipeline = gcip.Pipeline()

    job = gcip.Job(name="print_date", script="date")
    job.prepend_script("./before-script.sh")
    job.prepend_script("./after-script.sh")
    job.add_variables(USER="Max Power", URL="https://example.com")
    job.add_tags("test", "europe")

    pipeline.add_job(job)

    pipeline.print_yaml()
