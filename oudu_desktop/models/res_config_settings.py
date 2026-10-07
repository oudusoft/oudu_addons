from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from .instance_manifest import (
    VIDEO_RECORDING_DURATION_SECONDS_DEFAULT,
    VIDEO_RECORDING_DURATION_SECONDS_MAX,
    VIDEO_RECORDING_SIZE_MB_DEFAULT,
    VIDEO_RECORDING_SIZE_MB_MAX,
)

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

    oudu_desktop_video_max_duration_seconds = fields.Integer(
        string="Maximum Video Recording Duration (seconds)",
        default=VIDEO_RECORDING_DURATION_SECONDS_DEFAULT,
        config_parameter="oudu_desktop.video_max_duration_seconds",
    )
    oudu_desktop_video_max_size_mb = fields.Integer(
        string="Maximum Video Recording Size (MB)",
        default=VIDEO_RECORDING_SIZE_MB_DEFAULT,
        config_parameter="oudu_desktop.video_max_size_mb",
    )

    oudu_desktop_hide_source_local = fields.Boolean(
        string="Local files",
        config_parameter="oudu_desktop.hide_source_local",
    )
    oudu_desktop_hide_source_clipboard = fields.Boolean(
        string="Paste files",
        config_parameter="oudu_desktop.hide_source_clipboard",
    )
    oudu_desktop_hide_source_screenshot = fields.Boolean(
        string="Screenshot",
        config_parameter="oudu_desktop.hide_source_screenshot",
    )
    oudu_desktop_hide_source_screen = fields.Boolean(
        string="Screen",
        config_parameter="oudu_desktop.hide_source_screen",
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

    @api.constrains(
        "oudu_desktop_video_max_duration_seconds",
        "oudu_desktop_video_max_size_mb",
    )
    def _check_video_recording_limits(self):
        for record in self:
            if not (
                1
                <= record.oudu_desktop_video_max_duration_seconds
                <= VIDEO_RECORDING_DURATION_SECONDS_MAX
            ):
                raise ValidationError(
                    _(
                        "Maximum video recording duration must be between 1 and "
                        "%s seconds.",
                        VIDEO_RECORDING_DURATION_SECONDS_MAX,
                    )
                )
            if not (
                1
                <= record.oudu_desktop_video_max_size_mb
                <= VIDEO_RECORDING_SIZE_MB_MAX
            ):
                raise ValidationError(
                    _(
                        "Maximum video recording size must be between 1 and %s MB.",
                        VIDEO_RECORDING_SIZE_MB_MAX,
                    )
                )
