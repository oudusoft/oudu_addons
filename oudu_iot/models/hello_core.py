"""Oudu IoT hello 解码、结果分类与地址校验。

纯逻辑，不 import Odoo，仓根 unittest 直接加载。规则对齐 iot 仓 wire v1
hello-result.schema.json，钉版副本在仓根 tests/fixtures/iot-wire-v1/。
"""

import ipaddress
import json
import re

MAX_PAYLOAD_BYTES = 4096
MAX_STRING = 64
MAX_CHIP_REV = 0xFFFF

HELLO_REQUIRED = ("uuid", "name", "version", "chip", "mac", "compat_identifier")
HELLO_PATTERNS = {
    "uuid": r"[0-9a-f]{64}",
    "name": r"oudu-iot-[0-9a-f]{8}",
    "version": r"\d{4}\.\d{1,2}\.\d{1,2}",
    "mac": r"([0-9a-f]{2}:){5}[0-9a-f]{2}",
    "compat_identifier": r"[0-9a-f]{16}",
    "board": r"[a-z0-9]+(-[a-z0-9]+)*",
}
_COMPILED = {
    key: re.compile(pattern, re.ASCII) for key, pattern in HELLO_PATTERNS.items()
}
_CONTRACT_CODE = re.compile(r"[a-z_]{1,32}", re.ASCII)

CLIENT_KINDS = ("result", "error", "not_oudu", "unreachable", "blocked", "unsupported_browser")

_LABEL = re.compile(r"[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?", re.ASCII)
_IPV4 = re.compile(r"(0|[1-9][0-9]{0,2})(\.(0|[1-9][0-9]{0,2})){3}", re.ASCII)
_LOCAL_NETWORKS = tuple(
    ipaddress.ip_network(network)
    for network in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "169.254.0.0/16")
)

def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)

def _valid_string(key, value):
    if not isinstance(value, str) or not 0 < len(value) <= MAX_STRING:
        return False
    pattern = _COMPILED.get(key)
    return pattern is None or pattern.fullmatch(value) is not None

def _within_limit(payload):
    try:
        size = len(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
    except (TypeError, ValueError, RecursionError):
        return False
    return size <= MAX_PAYLOAD_BYTES

def decode_result(result):
    """设备 hello 的 result 对象 → ("ok", 快照) / ("not_oudu", None)。"""
    if not isinstance(result, dict) or not _within_limit(result):
        return "not_oudu", None
    snapshot = {}
    for key in HELLO_REQUIRED:
        if not _valid_string(key, result.get(key)):
            return "not_oudu", None
        snapshot[key] = result[key]
    if "chip_rev" in result:
        if not _is_int(result["chip_rev"]) or not 0 <= result["chip_rev"] <= MAX_CHIP_REV:
            return "not_oudu", None
        snapshot["chip_rev"] = result["chip_rev"]
    if "board" in result:
        if not _valid_string("board", result["board"]):
            return "not_oudu", None
        snapshot["board"] = result["board"]
    return "ok", snapshot

def decode_error(error):
    """设备 JSON-RPC 的 error 对象 → ("device_error", 码) / ("not_oudu", None)。"""
    if not isinstance(error, dict) or not _within_limit(error) or not _is_int(error.get("code")):
        return "not_oudu", None
    detail = str(error["code"])
    data = error.get("data")
    if isinstance(data, dict) and isinstance(data.get("code"), str):
        if _CONTRACT_CODE.fullmatch(data["code"]):
            detail = detail + " " + data["code"]
    return "device_error", detail

def classify(kind, payload=None):
    if kind not in CLIENT_KINDS:
        raise ValueError("unknown client kind")
    if kind == "result":
        return decode_result(payload)
    if kind == "error":
        return decode_error(payload)
    return kind, None

def normalize_address(value):
    """合法时返回小写规范形态，否则 None。不接受端口、路径、协议前缀与 IPv6。"""
    if not isinstance(value, str):
        return None
    address = value.strip().lower()
    if not address or len(address) > 253:
        return None
    if _IPV4.fullmatch(address):
        try:
            ip = ipaddress.IPv4Address(address)
        except ValueError:
            return None
        if any(ip in network for network in _LOCAL_NETWORKS):
            return address
        return None
    labels = address.split(".")
    if len(labels) < 2 or labels[-1] != "local":
        return None
    if all(_LABEL.fullmatch(label) for label in labels[:-1]):
        return address
    return None
