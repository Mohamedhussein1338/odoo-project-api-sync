from odoo import models, api, fields
from datetime import date, datetime, time
from odoo.exceptions import ValidationError
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class ProjectApi(models.Model):
    _name = "project.api"
    _description = "Project Api"

    name = fields.Char(string="Name")
    description = fields.Text()
    postcode = fields.Integer()
    date_availability = fields.Date()


    @api.model
    def create(self, vals):

        _logger.info("Data before sending to endpoint: %s", vals)

        # Create the record in Odoo 15
        new_record = super(ProjectApi, self).create(vals)

        # Prepare data to be sent to Odoo 16
        data_save = {
            'name': vals.get('name'),
            'description': vals.get('description'),
            'postcode': vals.get('postcode'),
            'date_availability': vals.get('date_availability')
        }

        # Send POST request to the endpoint in Odoo 16
        try:
            response = requests.post('http://localhost:8025/create_project', data=json.dumps(data_save))
            if response.status_code == 200:
                print("Record created successfully in Odoo 16 with ID:", response.text)
            else:
                print("Failed to create record in Odoo 16. Status code:", response.status_code)
        except Exception as e:
            print("Error occurred while sending request to Odoo 16:", str(e))

        return new_record
