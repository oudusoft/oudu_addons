from odoo import api, fields, models

from .instance_identity import (
    INSTANCE_COLOR_PARAM_KEY,
    INSTANCE_NAME_PARAM_KEY,
)

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    oudu_instance_name = fields.Char(
        string="Instance Name",
        config_parameter=INSTANCE_NAME_PARAM_KEY,
    )

    oudu_instance_icon = fields.Image(
        string="Instance Icon", max_width=128, max_height=128
    )

    oudu_instance_color = fields.Char(
        string="Instance Color",
        config_parameter=INSTANCE_COLOR_PARAM_KEY,
    )

    oudu_instance_color_clear = fields.Boolean(
        string="Clear instance color",
        help="Select to clear the configured instance color, then save.",
    )

    @api.onchange("oudu_instance_color_clear")
    def _onchange_oudu_instance_color_clear(self):
        if self.oudu_instance_color_clear:
            self.oudu_instance_color = False
            self.oudu_instance_color_clear = False

    @api.model
    def get_values(self):
        values = super().get_values()
        attachment = self.env["oudu.instance.identity"]._get_icon_attachment()
        values["oudu_instance_icon"] = (
            attachment.datas if attachment else False
        )
        return values

    def set_values(self):
        super().set_values()
        self.env["oudu.instance.identity"]._set_icon(self.oudu_instance_icon)
