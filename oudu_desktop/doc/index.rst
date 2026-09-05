Oudu Desktop
============

Overview
--------

Oudu Desktop is the server-side companion for the free Oudu Desktop native
client. It publishes instance-wide desktop policies and lets the client provide
multi-instance workspaces, direct report printing, local files and local device
access without changing normal Odoo browser use.

Installation
------------

Install ``Oudu Desktop`` from the Apps page. Odoo installs ``Oudu Instance
Identity`` automatically as its shared dependency. Install the native client
from ``https://desktop.oudu.top`` to use the desktop capabilities. Windows users
may also install the free companion client from the Microsoft Store:
``https://apps.microsoft.com/detail/9NK0Z5PVPGJJ``.

Configuration
-------------

Open ``Settings`` and select ``Oudu Software``. The Oudu Desktop section appears
after Instance Identity so that shared identity remains in one predictable
place.

Report Print Policy
-------------------

Choose how the native client handles reports for this instance:

* **Desktop default** lets the client use its normal report workflow.
* **Do not intercept** keeps Odoo's native report download.
* **Silent print** sends the report to the client's default printer.

File Upload Policy
------------------

Choose whether the native client handles uploads or keeps Odoo's native file
picker. You can also hide individual desktop sources: local files, clipboard
files, screenshots, camera, microphone and scanner.

If every desktop source is hidden, the native picker remains available so an
administrator cannot accidentally remove every upload path.

Browser fallback and privacy
----------------------------

The module remains installable and configurable when the native client is not
present. An absent or incompatible client falls back without blocking normal
browser use. Policies are instance-wide and contain no Odoo business records or
user content.

Compatibility and support
-------------------------

The listing for each Odoo series declares its supported version. Community,
Enterprise, self-hosted and Odoo.sh installations are supported without
depending on or replacing an Enterprise module. For support, contact
``info@oudu.net`` or visit ``https://desktop.oudu.top``.
