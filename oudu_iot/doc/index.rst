Oudu IoT
========

Overview
--------

Oudu IoT hosts work with standard Odoo without any Oudu module: enter a host
address in Point of Sale under Configuration > Settings > Connected Devices:
enable **IoT Box** and enter it as the **IP Address**, or enable **ePos Printer**
and enter it as the **Epson Printer IP** (receipts only).

This optional module adds:

* an **Oudu IoT** block in Settings > Oudu Software with firmware and flashing links;
* **Oudu > IoT > Hosts**, a list of hosts on your local network;
* a **Test connection** button, shown once the host is saved with an address,
  that checks the host from your browser and records its identity, firmware
  version, chip and board;
* an **Open gateway** button, shown after a successful test, that opens the
  host's own gateway page (the device's root address) in a new tab. Changing the
  address clears the result until the host is tested again.

Installation
------------

Install ``Oudu IoT`` from the Apps page. Odoo installs ``Oudu Instance
Identity`` automatically as its shared dependency. Get the firmware and flash an
ESP32 board online at ``https://iot.oudu.top``.

Configuration
-------------

Open ``Oudu > IoT > Hosts``, create a host with its ``.local`` host name or
private IPv4 address and save it, then click **Test connection**. Connection
tests need Google Chrome or Microsoft Edge. Only administrators can see and
edit hosts. The Oudu IoT block in ``Settings > Oudu Software`` links to the
firmware and the online flasher.

Support
-------

For support, contact ``iot@oudu.top`` or visit ``https://iot.oudu.top``.
