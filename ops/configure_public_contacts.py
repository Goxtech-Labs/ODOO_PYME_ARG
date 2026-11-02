"""Apply an explicitly selected public contact profile inside odoo shell.

Run with ARG_PUBLIC_CONTACTS_JSON pointing to the operator's chosen JSON file.
This changes only the five listed public parameters, never messaging providers.
"""
import json
import os
from pathlib import Path

profile = json.loads(Path(os.environ['ARG_PUBLIC_CONTACTS_JSON']).read_text())
values = {
    'arg_project_website': profile['website'],
    'arg_youtube_channel': profile['youtube_channel'],
    'arg_support_channel': profile['support_channel'],
    'arg_support_whatsapp': profile['support_whatsapp'],
    'arg_support_email': profile['support_email'],
}
# Validate through the installed settings model. Do not call set_values(), which
# could apply defaults for unrelated settings from this transient record.
settings = env['res.config.settings'].create(values)
parameters = env['ir.config_parameter'].sudo()
for field, value in values.items():
    parameter = settings._fields[field].config_parameter
    parameters.set_str(parameter, value or '')
env.cr.commit()
print(json.dumps({'configured_public_parameters': len(values), 'messages_sent': 0}))
