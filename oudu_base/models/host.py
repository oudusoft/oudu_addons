import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

HOST_PRODUCTS = ("iot", "desktop", "app")
_UUID = re.compile(r"[0-9a-f]{64}", re.ASCII)

class OuduHost(models.Model):
    """家族主机：一个 Oudu 受管端一条记录。产品专属字段由产品模块 _inherit。"""

    _name = "oudu.host"
    _description = "Oudu Host"
    _order = "name, id"

    name = fields.Char(string="Name", required=True)
    product = fields.Char(string="Product", required=True, index=True)
    uuid = fields.Char(string="UUID", readonly=True, copy=False, index=True)
    address = fields.Char(string="Address")
    note = fields.Text(string="Note")
    version = fields.Char(string="Firmware Version", readonly=True, copy=False)
    last_test_at = fields.Datetime(string="Last Test", readonly=True, copy=False)
    last_test_ok = fields.Boolean(
        string="Last Test Succeeded", readonly=True, copy=False
    )

    @api.constrains("product")
    def _check_product(self):
        for host in self:
            if host.product not in HOST_PRODUCTS:
                raise ValidationError(_("Unknown Oudu product: %s") % host.product)

    @api.constrains("product", "uuid")
    def _check_uuid(self):
        for host in self.filtered("uuid"):
            if not _UUID.fullmatch(host.uuid):
                raise ValidationError(
                    _("Host UUID must be 64 lowercase hexadecimal characters.")
                )
            duplicate = self.search_count(
                [
                    ("product", "=", host.product),
                    ("uuid", "=", host.uuid),
                    ("id", "!=", host.id),
                ]
            )
            if duplicate:
                raise ValidationError(_("This host is already registered."))
