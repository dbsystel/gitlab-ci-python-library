from gcip import Pipeline, Job

pipeline = Pipeline()
pipeline.add_children(Job(namespace="build", script="docker build ."))
pipeline.write_yaml()
