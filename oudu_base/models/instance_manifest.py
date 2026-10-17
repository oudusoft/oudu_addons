from odoo import api, models

MANIFEST_CONTRACT_VERSION = 1
MANIFEST_RESERVED_KEYS = frozenset(("version", "identity"))

class OuduInstanceManifest(models.AbstractModel):
    _name = "oudu.instance.manifest"
    _description = "Oudu Instance Capability Manifest"

    @api.model
    def _get_product_values(self):
        """Installed product modules extend this mapping through ``super()``."""
        return {}

    @api.model
    def _get_public_values(self):
        identity = self.env["oudu.instance.identity"].sudo()._get_public_values()
        products = self._get_product_values()
        if not isinstance(products, dict):
            raise TypeError("Oudu manifest product values must be a mapping")
        collisions = MANIFEST_RESERVED_KEYS.intersection(products)
        if collisions:
            raise ValueError(
                "Oudu manifest product keys collide with reserved keys: %s"
                % ", ".join(sorted(collisions))
            )

        payload = {
            "version": MANIFEST_CONTRACT_VERSION,
            "identity": {
                "name": identity["name"],
                "color": identity["color"],
                "icon": "/oudu_base/icon" if identity["has_icon"] else None,
            },
        }
        payload.update(products)
        return payload
