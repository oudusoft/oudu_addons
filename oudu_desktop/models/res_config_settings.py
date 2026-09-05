from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    oudu_desktop_report_policy = fields.Selection(
        selection=[
            ("default", "Desktop default"),
            ("passthrough", "Do not intercept (native download)"),
            ("silent", "Silent to default printer"),
        ],
        string="Report Print Policy",
        default="default",
        config_parameter="oudu_desktop.report_policy",
    )

    oudu_desktop_file_policy = fields.Selection(
        selection=[
            ("default", "Desktop default"),
            ("passthrough", "Do not intercept (native picker)"),
        ],
        string="File Upload Policy",
        default="default",
        config_parameter="oudu_desktop.file_policy",
    )

    oudu_desktop_hide_source_local = fields.Boolean(
        string="Local files",
        config_parameter="oudu_desktop.hide_source_local",
    )
    oudu_desktop_hide_source_clipboard = fields.Boolean(
        string="Clipboard files",
        config_parameter="oudu_desktop.hide_source_clipboard",
    )
    oudu_desktop_hide_source_screenshot = fields.Boolean(
        string="Screenshot",
        config_parameter="oudu_desktop.hide_source_screenshot",
    )
    oudu_desktop_hide_source_camera = fields.Boolean(
        string="Camera",
        config_parameter="oudu_desktop.hide_source_camera",
    )
    oudu_desktop_hide_source_scanner = fields.Boolean(
        string="Scanner",
        config_parameter="oudu_desktop.hide_source_scanner",
    )
    oudu_desktop_hide_source_microphone = fields.Boolean(
        string="Microphone",
        config_parameter="oudu_desktop.hide_source_microphone",
    )
