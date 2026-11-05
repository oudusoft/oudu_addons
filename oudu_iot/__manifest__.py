{
    "name": "Oudu IoT",
    "summary": "Register and test Oudu IoT hosts on your local network",
    "version": "18.0.1.0",
    "sequence": -940,
    "category": "Extra Tools",
    "author": "Oudu Software",
    "website": "https://iot.oudu.top",
    "support": "iot@oudu.top",
    "license": "LGPL-3",
    "images": ["static/description/banner.png"],
    "depends": ["oudu_base", "web"],
    "data": [
        "views/oudu_host_views.xml",
        "views/oudu_host_form_states.xml",
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "oudu_iot/static/src/js/oudu_iot.js",
        ],
    },
    "installable": True,
    "application": True,
}
