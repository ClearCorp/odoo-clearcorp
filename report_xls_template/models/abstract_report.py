# -*- coding: utf-8 -*-
# © 2014 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class AbstractReport(models.AbstractModel):

    _inherit = 'report.abstract_report'
    _report_render_type = None

    @api.model
    def render_html(self, docids, data=None):
        if self._report_render_type == 'qweb-xls':
            context = dict(self._context or {})

            if context and context.get('active_ids'):
                # Browse the selected objects via their reference in context
                model = context.get('active_model') or context.get('model')
                objects_model = self.env[model]
                objects = objects_model.with_context(context).browse(context['active_ids'])
            else:
                # If no context is set (for instance,
                # during test execution), build one
                model = self.env['report']._get_report_from_name(self._template).model
                objects_model = self.env[model]
                objects = objects_model.with_context(context).browse(docids)
                context['active_model'] = model
                context['active_ids'] = docids

            # Generate the old style report
            wrapped_report = self.with_context(context)._wrapped_report_class(self.env.cr, self.env.uid, '',
                                                                              context=self.env.context)
            wrapped_report.set_context(objects, data, context['active_ids'])

            # Rendering self._template with the wrapped report instance localcontext as
            # rendering environment
            docargs = dict(wrapped_report.localcontext)
            if not docargs.get('lang'):
                docargs.pop('lang', False)
            docargs['docs'] = docargs.get('objects')

            # Used in template translation (see translate_doc method from report model)
            docargs['doc_ids'] = context['active_ids']
            docargs['doc_model'] = model

            return self.env['report'].with_context(context).render(self._template, docargs)

        else:
            return super(AbstractReport, self).render_html(docids, data)
