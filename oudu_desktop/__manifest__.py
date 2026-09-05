{
    "name": "Oudu Desktop",
    "summary": "Native desktop capabilities for Odoo with the Oudu Desktop client",
    "version": "18.0.1.2",
    "sequence": -980,
    "category": "Extra Tools",
    "author": "Oudu Software",
    "website": "https://desktop.oudu.top",
    "support": "info@oudu.net",
    "license": "LGPL-3",
    "depends": ["oudu_base", "web"],
    "data": [
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "oudu_desktop/static/src/js/oudu_desktop.js",
        ],
    },
    "images": ["static/description/banner.png"],
    "installable": True,
    "application": True,
}
