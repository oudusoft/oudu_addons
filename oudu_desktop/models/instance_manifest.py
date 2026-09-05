from odoo import api, models

REPORT_POLICIES = ("default", "passthrough", "silent")
FILE_POLICIES = ("default", "passthrough")
FILE_SOURCES = (
    "local",
    "clipboard",
    "screenshot",
    "camera",
    "microphone",
    "scanner",
)

class OuduInstanceManifest(models.AbstractModel):
    _inherit = "oudu.instance.manifest"

    @api.model
    def _get_product_values(self):
        products = dict(super()._get_product_values())
        if "desktop" in products:
            raise ValueError("Oudu manifest product key already exists: desktop")

        params = self.env["ir.config_parameter"].sudo()
        report = params.get_param("oudu_desktop.report_policy")
        file_mode = params.get_param("oudu_desktop.file_policy")
        hidden = [
            source
            for source in FILE_SOURCES
            if params.get_param("oudu_desktop.hide_source_%s" % source)
        ]
        products["desktop"] = {
            "report": report if report in REPORT_POLICIES else "default",
            "file": {
                "mode": file_mode if file_mode in FILE_POLICIES else "default",
                "hidden": hidden,
            },
        }
        return products
