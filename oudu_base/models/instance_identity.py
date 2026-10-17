import re

from odoo import api, models

from .attachment_binary import (
    attachment_content,
    attachment_storage_values,
    image_bytes,
)
from .config_parameter import get_string, set_string

INSTANCE_NAME_PARAM_KEY = "oudu_base.instance_name"
INSTANCE_COLOR_PARAM_KEY = "oudu_base.instance_color"
INSTANCE_ICON_PARAM_KEY = "oudu_base.instance_icon_attachment_id"
INSTANCE_ICON_ATTACHMENT_NAME = "oudu_instance_icon"

INSTANCE_NAME_MAX_LENGTH = 64
INSTANCE_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")

def _normalized_text(value):
    return value.strip() if isinstance(value, str) else ""

class OuduInstanceIdentity(models.AbstractModel):
    _name = "oudu.instance.identity"
    _description = "Oudu Instance Identity"

    @api.model
    def _get_icon_attachment(self):
        params = self.env["ir.config_parameter"].sudo()
        raw = get_string(params, INSTANCE_ICON_PARAM_KEY)
        try:
            attachment_id = int(raw) if raw else 0
        except (TypeError, ValueError):
            attachment_id = 0
        if not attachment_id:
            return self.env["ir.attachment"]
        return (
            self.env["ir.attachment"]
            .sudo()
            .search(
                [
                    ("id", "=", attachment_id),
                    ("name", "=", INSTANCE_ICON_ATTACHMENT_NAME),
                ],
                limit=1,
            )
        )

    @api.model
    def _set_icon(self, icon):
        params = self.env["ir.config_parameter"].sudo()
        attachment = self._get_icon_attachment()
        icon = image_bytes(icon)
        if icon:
            if attachment:
                if attachment_content(attachment) != icon:
                    values = {"public": True}
                    values.update(attachment_storage_values(attachment, icon))
                    attachment.write(values)
            else:
                values = {
                    "name": INSTANCE_ICON_ATTACHMENT_NAME,
                    "public": True,
                }
                values.update(attachment_storage_values(attachment, icon))
                attachment = self.env["ir.attachment"].sudo().create(
                    values
                )
            set_string(params, INSTANCE_ICON_PARAM_KEY, str(attachment.id))
        else:
            if attachment:
                attachment.unlink()
            set_string(params, INSTANCE_ICON_PARAM_KEY, False)

    @api.model
    def _get_public_values(self):
        params = self.env["ir.config_parameter"].sudo()
        name = _normalized_text(get_string(params, INSTANCE_NAME_PARAM_KEY))
        color = _normalized_text(get_string(params, INSTANCE_COLOR_PARAM_KEY))
        return {
            "name": name[:INSTANCE_NAME_MAX_LENGTH] if name else None,
            "color": color if INSTANCE_COLOR_RE.match(color) else None,
            "has_icon": bool(self._get_icon_attachment()),
        }
