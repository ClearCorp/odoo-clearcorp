# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from datetime import datetime
import openerp.tools as tools

# Debe cambiarse TODO el módulo -> etiqueta que cambia a rojo si se pasa de tiempo
# Se agrega un tag a de task tag_ids


class Task(models.Model):
    _inherit = 'project.task'

    @api.one
    @api.depends('date_deadline', 'date_start')
    def _get_color_code(self):
        """Calculate the current color code for the task depending on the state
        Colors:
        0 -> White          5 -> Aqua
        1 -> Dark Gray      6 -> Light Aqua
        2 -> Red            7 -> Blue
        3 -> Orange         8 -> Purple
        4 -> Green          9 -> Pink
        @param self: The object pointer.
        @param date_deadline: The string deadline
        @param planned_hours: Total planned hours for the task
        @param state: The current task state
        @param progress: The current task progress
        @return: An integer that represents the current task state as a color
        """
        if self.date_deadline:
            deadline = datetime.strptime(self.date_deadline,
                                     tools.DEFAULT_SERVER_DATE_FORMAT)
            date_start = datetime.strptime(self.date_start,
                                       tools.DEFAULT_SERVER_DATETIME_FORMAT)
            today = datetime.now()
            time_diff = deadline - date_start

            # If the time difference is in seconds, there is still 1 work
            # day to go.
            if time_diff.seconds:
                total_days = time_diff.days + 1
            else:
                total_days = time_diff.days

            time_diff = deadline - today

            if time_diff.seconds:
                days_until_deadline = time_diff.days + 1
            else:
                days_until_deadline = time_diff.days

            try:
                time_ratio = float(days_until_deadline) / float(total_days)
            except ZeroDivisionError:
                time_ratio = 0.0

            # If the task is not done and it hasn't been cancelled, it's
            # necessary to call the user's attention.
            if self.state != 'done' or self.state != 'cancel':
                # Checks if the time ratio is less than 0.2 to alert the task
                # needs attention.
                if time_ratio <= 0.2:

                    # Gets res_id to relate the impending deadline tag to
                    # the task.
                    _model, res_id = self.env[
                        'ir.model.data'].get_object_reference(
                            'project_deadline_color',
                            'project_deadline_tag_data')
                    self.tag_ids = [(4, res_id)]




    color = fields.Integer(compute='_get_color_code', string='Color Index',
                           store=True)
