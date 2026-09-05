Oudu Instance Identity
======================

Overview
--------

Oudu Instance Identity is the shared settings and capability foundation for
Oudu Software modules. It lets an administrator identify an Odoo instance once
and lets installed Oudu products reuse that identity without duplicating the
same controls.

Installation
------------

Install ``Oudu Instance Identity`` from the Apps page. Odoo installs it
automatically when another Oudu module declares it as a dependency.

Configuration
-------------

Open ``Settings`` and select ``Oudu Software``. The Instance Identity section
is always the first Oudu settings section.

* **Instance Name** is the friendly name shown by compatible Oudu products.
* **Instance Color** helps distinguish this instance from other workspaces.
* **Instance Icon** is a small square image used by compatible Oudu products.

Any field may be left empty. Each product then keeps its own default for that
value. Settings apply to the instance and should be managed by an administrator.

Capability contract
-------------------

The module publishes a machine-readable description of the instance identity
and installed Oudu integrations. Compatible clients can use this contract to
discover available capabilities and degrade safely when a capability is absent.
The contract contains configuration and capability metadata, not Odoo business
records or user content.

Safe defaults
-------------

Installing the module does not replace an Odoo Community or Enterprise module
and does not change normal browser access. Leaving identity values empty keeps
the product defaults.

Compatibility and support
-------------------------

Generated and tested for Odoo 13 through 19, Community and Enterprise. For
support, contact ``info@oudu.net`` or visit ``https://www.oudu.net``.
