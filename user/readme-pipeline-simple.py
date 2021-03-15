from gcip import Job, Pipeline

pipeline = Pipeline()
pipeline.add_children(Job(namespace="build", script="docker build ."))
pipeline.write_yaml()
