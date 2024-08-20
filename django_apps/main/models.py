from django.db import models, connection

from netfields import MACAddressField
import datetime

from users.models import User

class Ticket(models.Model):
    service_now = models.CharField(primary_key=True, max_length=32)
    service_now_sys_id = models.CharField(max_length=32)
    assigned_to = models.ForeignKey(
        "users.User", default=None, on_delete=models.SET_DEFAULT, null=True
    )
    requested_for = models.ForeignKey(
        "owners.Owner", default=None, on_delete=models.SET_DEFAULT, null=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    resolved_date = models.DateTimeField(default=None, null=True)
    resolved = models.BooleanField(default=False)

    def resolve(self):
        if not self.resolved:
            self.resolved_date = datetime.datetime.now()
            self.resolved = True
            # Add code to resolve in ServiceNow
            self.save()

    # Add function to get all devices on ticket


class Vulnerability(models.Model):
    plugin_id = models.CharField(primary_key=True, max_length=7)
    name = models.CharField(max_length=256)
    synopsis = models.CharField(max_length=400, null=True)
    description=models.CharField(max_length=2000, null=True)
    solution = models.CharField(max_length=2000, null=True)
    links = models.CharField(max_length=500, null=True)
    vpr = models.DecimalField(max_digits=3, decimal_places=1, default=None, null=True)
    suppressed = models.BooleanField(default=False)

    # Figure out how to get the synopsis, description, solution, and links for a vuln.
    # Not all vulns are listed in the "Priority" section of a scan Details report, and none of this info is in the vuln summaries elsewhere in the report.

    severityOptions = [
        (1, "Low"),
        (2, "Medium"),
        (3, "High"),
        (4, "Critical")
    ]

    severity = models.IntegerField(choices=severityOptions, default=1)

    # Add function to count how many devices currently have a given vulnerability
