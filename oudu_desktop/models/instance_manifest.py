from odoo import api, models

from odoo.addons.oudu_base.models.config_parameter import (
    get_boolean,
    get_integer,
    get_string,
)

REPORT_POLICIES = ("default", "passthrough", "silent")
FILE_POLICIES = ("default", "passthrough")
FILE_SOURCES = (
    "local",
    "clipboard",
    "screenshot",
    "screen",
    "camera",
    "microphone",
    "scanner",
)
VIDEO_RECORDING_DURATION_SECONDS_DEFAULT = 180
VIDEO_RECORDING_DURATION_SECONDS_MAX = 1_800
VIDEO_RECORDING_SIZE_MB_DEFAULT = 150
VIDEO_RECORDING_SIZE_MB_MAX = 256

def bounded_positive_integer(params, key, default, maximum):
    value = get_integer(params, key, default)
    try:
        value = int(value)
    except (TypeError, ValueError):
        return default
    if not 1 <= value <= maximum:
        return default
    return value

class OuduInstanceManifest(models.AbstractModel):
    _inherit = "oudu.instance.manifest"

    @api.model
    def _get_product_values(self):
        products = dict(super()._get_product_values())
        if "desktop" in products:
            raise ValueError("Oudu manifest product key already exists: desktop")

        params = self.env["ir.config_parameter"].sudo()
        report = get_string(params, "oudu_desktop.report_policy")
        file_mode = get_string(params, "oudu_desktop.file_policy")
        video_duration = bounded_positive_integer(
            params,
            "oudu_desktop.video_max_duration_seconds",
            VIDEO_RECORDING_DURATION_SECONDS_DEFAULT,
            VIDEO_RECORDING_DURATION_SECONDS_MAX,
        )
        video_size = bounded_positive_integer(
            params,
            "oudu_desktop.video_max_size_mb",
            VIDEO_RECORDING_SIZE_MB_DEFAULT,
            VIDEO_RECORDING_SIZE_MB_MAX,
        )
        hidden = [
            source
            for source in FILE_SOURCES
            if get_boolean(params, "oudu_desktop.hide_source_%s" % source)
        ]
        products["desktop"] = {
            "report": report if report in REPORT_POLICIES else "default",
            "file": {
                "mode": file_mode if file_mode in FILE_POLICIES else "default",
                "hidden": hidden,
            },
            "capture": {
                "video": {
                    "max_duration_seconds": video_duration,
                    "max_size_mb": video_size,
                },
            },
        }
        return products
