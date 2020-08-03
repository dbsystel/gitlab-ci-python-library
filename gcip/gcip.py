import yaml
import copy


class Job():
    def __init__(
        self,
        *args,
        name: str,
        script: [str],
    ):
        self._name = name
        self._namespace = None
        self._variables = {}

        if type(script) == str:
            self._script = [script]
        elif type(script) == list:
            self._script = script
        else:
            raise AttributeError(
                "script parameter must be of type string or list of strings")

    @property
    def fqdn(self):
        return self._name + (f"_{self._namespace}"
                             if self._namespace is not None else "")

    def prepend_script(self, script: str):
        self._script.insert(0, script)

    def append_script(self, script: str):
        self._script.append(script)

    def add_variables(self, variables: dict):
        self._variables = {**self._variables, **variables}

    def add_namespace(self, namespace: str):
        if namespace is None:
            return
        if self._namespace is None:
            self._namespace = namespace
        else:
            self._namespace += "_" + namespace

    def copy(self):
        job_copy = Job(
            name=self._name,
            script=copy.deepcopy(self._script),
        )
        job_copy.add_variables(copy.deepcopy(self._variables))
        job_copy.add_namespace(self._namespace)
        return job_copy

    def render(self):
        return {
            "script": self._script,
            "variables": self._variables,
        }


class JobSequence():
    def __init__(self, namespace: str = None):
        self._jobs = []
        self._namespace = namespace
        self._prepend_scripts = []
        self._append_scripts = []

    def add_job(self, job: Job, *args, namespace: str = None):
        job.add_namespace(namespace)
        self._jobs.append(job)

    def add_sequence(self, job_sequence, *args, namespace: str = None):
        job_sequence.add_namespace(namespace)
        self._jobs.append(job_sequence)

    def prepend_script(self, script: str):
        self._prepend_scripts.insert(0, script)

    def append_script(self, script: str):
        self._append_scripts.append(script)

    def add_namespace(self, namespace: str):
        if namespace is None:
            return
        if self._namespace is None:
            self._namespace = namespace
        else:
            self._namespace += namespace

    @property
    def populated_jobs(self) -> list:
        all_jobs = []
        for job in self._jobs:
            if type(job) == JobSequence:
                all_jobs += job.populated_jobs
            elif type(job) == Job:
                all_jobs.append(job.copy())

        for job in all_jobs:
            job.add_namespace(self._namespace)
            for script in self._prepend_scripts:
                job.prepend_script(script)
            for script in self._append_scripts:
                job.append_script(script)

        return all_jobs


class Pipeline(JobSequence):
    def __init__(
        self,
        *args,
        namespace: str = None,
    ):
        super().__init__(namespace)
        self._pipeline = {}

    def render(self):
        stages = {}
        job_copies = self.populated_jobs
        for job in job_copies:
            # use the keys of dictionary as ordered set
            stages[job.fqdn] = None
        pipe_copy = copy.deepcopy(self._pipeline)
        pipe_copy["stages"] = list(stages.keys())
        for job in job_copies:
            rendered_job = job.render()
            rendered_job["stage"] = job.fqdn
            pipe_copy[job.fqdn] = rendered_job
        return pipe_copy

    def print_yaml(self):
        print(
            yaml.dump(self.render(), default_flow_style=False,
                      sort_keys=False))
