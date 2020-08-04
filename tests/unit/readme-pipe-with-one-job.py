import gcip

pipeline = gcip.Pipeline()
pipeline.add_job(gcip.Job(name="print_date", script="date"))
pipeline.print_yaml()
