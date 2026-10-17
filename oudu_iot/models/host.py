from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

from .hello_core import classify, normalize_address

TEST_STATUSES = [
    ("ok", "Connected"),
    ("duplicate", "Already registered as another host"),
    ("device_error", "Device reported an error"),
    ("not_oudu", "Not an Oudu IoT device"),
    ("unreachable", "No response: check the address and network; if a .local name fails, try the IP address"),
    ("blocked", "Blocked by the browser: allow local network access for this site"),
    ("unsupported_browser", "Browser not supported: use Chrome or Edge"),
]

class OuduHost(models.Model):
    _inherit = "oudu.host"

    iot_chip = fields.Char(string="Chip", readonly=True, copy=False)
    iot_chip_rev = fields.Char(string="Chip Revision", readonly=True, copy=False)
    iot_board = fields.Char(string="Board", readonly=True, copy=False)
    iot_compat_identifier = fields.Char(
        string="Compatibility Identifier", readonly=True, copy=False
    )
    iot_last_test_status = fields.Selection(
        TEST_STATUSES, string="Last Test Result", readonly=True, copy=False
    )
    iot_last_test_detail = fields.Char(
        string="Last Test Detail", readonly=True, copy=False
    )

    @api.constrains("product", "address")
    def _check_iot_address(self):
        for host in self:
            if host.product != "iot" or not host.address:
                continue
            if normalize_address(host.address) is None:
                raise ValidationError(
                    _("Use a .local host name or a private IPv4 address, without port or http://.")
                )

    def write(self, vals):
        changed = self.browse()
        if "address" in vals and "last_test_ok" not in vals:
            changed = self.filtered(lambda h: h.product == "iot" and h.address != vals["address"])
        result = super().write(vals)
        if changed:
            super(OuduHost, changed).write(
                {"last_test_ok": False, "iot_last_test_status": False, "iot_last_test_detail": False}
            )
        return result

    def action_iot_gateway(self):
        """备用：脚本未加载时由服务端打开设备网关页（根路径）。"""
        self.ensure_one()
        address = normalize_address(self.address) if self.address else None
        if self.product != "iot" or address is None:
            raise UserError(_("Enter a valid host address and save first."))
        return {"type": "ir.actions.act_url", "url": "http://%s/" % address, "target": "new"}

    def action_iot_test(self):
        """备用：连接测试必须在浏览器中执行，脚本未加载时只提示。"""
        raise UserError(_("Reload the page and try again: the connection test runs in your browser."))

    def action_iot_refresh(self):
        """表单隐藏按钮：脚本写回测试结果后点击，Odoo 先保存表单再原地重读记录。"""
        return True

    def iot_apply_hello(self, kind, payload=None):
        """浏览器回传一次 hello 结论；result/error 载荷由服务器严格校验，不信任前端。"""
        self.ensure_one()
        if self.product != "iot":
            raise UserError(_("Only IoT hosts can be tested."))
        try:
            status, data = classify(kind, payload)
        except ValueError:
            raise UserError(_("Unknown connection test result.")) from None
        values = {
            "last_test_at": fields.Datetime.now(),
            "last_test_ok": False,
            "iot_last_test_status": status,
            "iot_last_test_detail": False,
        }
        if status == "ok":
            other = self.search(
                [
                    ("product", "=", "iot"),
                    ("uuid", "=", data["uuid"]),
                    ("id", "!=", self.id),
                ],
                limit=1,
            )
            if other:
                values["iot_last_test_status"] = "duplicate"
                values["iot_last_test_detail"] = other.display_name
            else:
                values.update(
                    {
                        "last_test_ok": True,
                        "uuid": data["uuid"],
                        "version": data["version"],
                        "iot_chip": data["chip"],
                        "iot_chip_rev": str(data["chip_rev"]) if "chip_rev" in data else False,
                        "iot_board": data.get("board") or False,
                        "iot_compat_identifier": data["compat_identifier"],
                    }
                )
        elif status == "device_error":
            values["iot_last_test_detail"] = data
        self.write(values)
        return {"status": values["iot_last_test_status"]}
