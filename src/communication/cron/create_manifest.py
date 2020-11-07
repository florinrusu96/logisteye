from django_cron import CronJobBase, Schedule
from src.communication import models


class CreateManifest(CronJobBase):
    RUN_EVERY_MINS = 120  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'  # a unique code

    def awesome_algorithm_to_get_routes(self):
        return [{}]

    def create_manifest(self):
        # should get all data from the database
        instances = models.Instance.objects.filter(is_active=True)
        aggregated_data = {}
        for instance in instances:
            aggregated_data[instance] = []
            aggregated_data[instance] = (self.awesome_algorithm_to_get_routes(instance))

    def do(self):
        self.create_manifest()
