import json

from odoo import http
from odoo.http import request

from odoo.addons.oudu_base.models.attachment_binary import attachment_content

class OuduBaseController(http.Controller):
    @http.route(
        "/oudu_base/manifest",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def manifest(self):
        payload = (
            request.env["oudu.instance.manifest"].sudo()._get_public_values()
        )
        return request.make_response(
            json.dumps(payload, separators=(",", ":")),
            [("Content-Type", "application/json")],
        )

    @http.route(
        "/oudu_base/icon",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def icon(self):
        attachment = (
            request.env["oudu.instance.identity"]
            .sudo()
            ._get_icon_attachment()
        )
        if not attachment:
            raise request.not_found()
        content = attachment_content(attachment)
        return request.make_response(
            content,
            [
                ("Content-Type", attachment.mimetype or "application/octet-stream"),
                ("Content-Length", str(len(content))),
            ],
        )
