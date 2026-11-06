from odoo.tools import SQL


def migrate(cr, version):
    # Preserve 1.0 evidence while allowing repeatable ready/resume operations with stable keys.
    cr.execute('ALTER TABLE arg_pyme_repair_event ADD COLUMN IF NOT EXISTS request_key varchar')
    cr.execute("UPDATE arg_pyme_repair_event SET request_key='legacy-' || id WHERE request_key IS NULL")
    cr.execute("SELECT conname FROM pg_constraint WHERE conrelid='arg_pyme_repair_event'::regclass "
               "AND contype='u' AND pg_get_constraintdef(oid)='UNIQUE (case_id, kind)'")
    for name, in cr.fetchall():
        cr.execute(SQL('ALTER TABLE arg_pyme_repair_event DROP CONSTRAINT %s', SQL.identifier(name)))
