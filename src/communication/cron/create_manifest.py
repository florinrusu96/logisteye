from django_cron import CronJobBase, Schedule
import requests
from backend import settings
from communication import models


class CreateManifest(CronJobBase):
    RUN_EVERY_MINS = 120  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'  # a unique code

    def awesome_algorithm_to_get_routes(self, aggregated_data, instances):
        if aggregated_data is None:
            return
        if instances is None:
            return
        # awesome algorithm to get routes tbd
        return [{}]

    @staticmethod
    def get_instance_url(instance_url: str):
        append = 'communicate/packages'
        if instance_url.endswith('/'):
            return instance_url
        return instance_url + '/' + append

    # we should use async stuff, but for now it will work like this
    def create_manifest(self):
        # should get all data from the database
        instances = models.Instance.objects.filter(is_active=True)
        aggregated_data = {}
        for instance in instances:
            instance_url = self.get_instance_url(instance.instance_url)
            aggregated_data[instance.company.name] = requests.get(instance_url).json()
        self.awesome_algorithm_to_get_routes(aggregated_data, instances)

    def do(self):
        if settings.IS_MASTER_INSTANCE:
            self.create_manifest()
        return
