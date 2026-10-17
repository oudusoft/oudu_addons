(function () {
    "use strict";

    var MODEL = "oudu.host";
    var TIMEOUT_MS = 20000;
    var MAX_ENVELOPE_CHARS = 4096;
    var busy = false;

    function rpc(method, args, root) {
        return fetch("/web/dataset/call_kw/" + MODEL + "/" + method, {
            method: "POST",
            credentials: "same-origin",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                jsonrpc: "2.0",
                method: "call",
                id: Date.now(),
                params: { model: MODEL, method: method, args: args, kwargs: {} },
            }),
        })
            .then(function (response) {
                var type = response.headers.get("Content-Type") || "";
                if (!response.ok || type.indexOf("application/json") === -1) {
                    throw new Error(text(root, "rpc_error"));
                }
                return response.json();
            })
            .then(function (payload) {
                if (payload.error) {
                    var data = payload.error.data || {};
                    throw new Error(data.message || payload.error.message);
                }
                return payload.result;
            });
    }

    function currentRecordId() {
        var parts = window.location.hash.replace(/^#/, "").split("&");
        var model = null;
        var id = null;
        for (var i = 0; i < parts.length; i++) {
            var pair = parts[i].split("=");
            if (pair[0] === "model") {
                model = decodeURIComponent(pair[1] || "");
            } else if (pair[0] === "id") {
                id = pair[1] || "";
            }
        }
        if (model === MODEL && /^[0-9]+$/.test(id || "")) {
            return parseInt(id, 10);
        }
        if (model) {
            return null;
        }
        var match = window.location.pathname.match(/\/([0-9]+)\/?$/);
        return match ? parseInt(match[1], 10) : null;
    }

    function text(root, key) {
        var node = root.querySelector('[data-oudu-iot-text="' + key + '"]');
        return node ? node.textContent.trim() : "";
    }

    function isChromium() {
        var data = navigator.userAgentData;
        var brands = data && data.brands;
        if (!brands) {
            return false;
        }
        for (var i = 0; i < brands.length; i++) {
            if (brands[i].brand === "Chromium") {
                return true;
            }
        }
        return false;
    }

    function queryPermission(name) {
        return navigator.permissions.query({ name: name });
    }

    function failureKind() {
        if (!isChromium()) {
            return Promise.resolve(
                window.location.protocol === "https:" ? "unsupported_browser" : "unreachable"
            );
        }
        if (!navigator.permissions || !navigator.permissions.query) {
            return Promise.resolve("unreachable");
        }
        return queryPermission("local-network-access")
            .then(null, function () {
                return queryPermission("local-network");
            })
            .then(
                function (state) {
                    return state.state === "denied" ? "blocked" : "unreachable";
                },
                function () {
                    return "unreachable";
                }
            );
    }

    function probeHello(address) {
        var requestId = Math.floor(Math.random() * 1000000000) + 1;
        var controller = new AbortController();
        var timer = setTimeout(function () {
            controller.abort();
        }, TIMEOUT_MS);

        function done(kind, payload) {
            clearTimeout(timer);
            return { kind: kind, payload: payload === undefined ? null : payload };
        }

        function failed() {
            return failureKind().then(function (kind) {
                return done(kind);
            });
        }

        function unwrap(envelope) {
            if (!envelope || typeof envelope !== "object" || envelope.id !== requestId) {
                return done("not_oudu");
            }
            if (Object.prototype.hasOwnProperty.call(envelope, "error")) {
                return done("error", envelope.error);
            }
            if (Object.prototype.hasOwnProperty.call(envelope, "result")) {
                return done("result", envelope.result);
            }
            return done("not_oudu");
        }

        var request;
        try {
            request = fetch("http://" + address + "/iot/hello", {
                method: "POST",
                mode: "cors",
                credentials: "omit",
                cache: "no-store",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ jsonrpc: "2.0", method: "call", id: requestId, params: {} }),
                targetAddressSpace: "local",
                signal: controller.signal,
            });
        } catch (error) {
            request = Promise.reject(error);
        }
        return request
            .then(function (response) {
                var length = parseInt(response.headers.get("Content-Length"), 10);
                if (length > MAX_ENVELOPE_CHARS) {
                    return done("not_oudu");
                }
                return response.text().then(function (body) {
                    var envelope = null;
                    if (body.length <= MAX_ENVELOPE_CHARS) {
                        try {
                            envelope = JSON.parse(body);
                        } catch (error) {
                            envelope = null;
                        }
                    }
                    return unwrap(envelope);
                });
            })
            .then(null, failed);
    }

    function localAddress(value) {
        if (typeof value !== "string") {
            return null;
        }
        var host = value.trim().toLowerCase();
        if (!host || host.length > 253) {
            return null;
        }
        var parts = host.split(".");
        var i;
        if (parts.length >= 2 && parts[parts.length - 1] === "local") {
            for (i = 0; i < parts.length - 1; i++) {
                if (!/^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$/.test(parts[i])) {
                    return null;
                }
            }
            return host;
        }
        if (parts.length !== 4) {
            return null;
        }
        var octets = [];
        for (i = 0; i < 4; i++) {
            if (!/^(0|[1-9][0-9]{0,2})$/.test(parts[i]) || parseInt(parts[i], 10) > 255) {
                return null;
            }
            octets.push(parseInt(parts[i], 10));
        }
        var first = octets[0];
        var second = octets[1];
        var isPrivate =
            first === 10 ||
            (first === 172 && second >= 16 && second <= 31) ||
            (first === 192 && second === 168) ||
            (first === 169 && second === 254);
        return isPrivate ? host : null;
    }

    function readAddress(id, root) {
        return rpc("read", [[id], ["address", "product"]], root).then(function (rows) {
            var row = rows && rows[0];
            return row && row.product === "iot" ? localAddress(row.address) : null;
        });
    }

    function runTest(root, id, address) {
        return probeHello(address).then(function (outcome) {
            return rpc("iot_apply_hello", [[id], outcome.kind, outcome.payload], root);
        });
    }

    function formAddress() {
        var field = document.querySelector('.o_form_view [name="address"]');
        if (!field) {
            return null;
        }
        var input = field.tagName === "INPUT" ? field : field.querySelector("input");
        return (input ? input.value : field.textContent).trim().toLowerCase();
    }

    function refreshForm() {
        var button = document.querySelector('button[name="action_iot_refresh"]');
        if (button) {
            button.click();
        } else {
            window.location.reload();
        }
    }

    var ACTIONS = {
        action_iot_test: "test",
        action_iot_gateway: "gateway",
    };
    var SELECTOR =
        'button[name="action_iot_test"], button[name="action_iot_gateway"]';

    function onAction(event) {
        var trigger = event.target.closest ? event.target.closest(SELECTOR) : null;
        if (!trigger) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
        var root = document.querySelector(".oudu_iot_host_texts") || document;
        var action = ACTIONS[trigger.getAttribute("name")];
        var id = currentRecordId();
        if (!id) {
            window.alert(text(root, "unsaved"));
            return;
        }
        if (busy) {
            return;
        }
        var popup = null;
        if (action === "gateway") {
            popup = window.open("", "_blank");
            if (!popup) {
                return;
            }
        }
        busy = true;
        trigger.disabled = true;
        readAddress(id, root)
            .then(function (address) {
                if (!address) {
                    if (popup) {
                        popup.close();
                    }
                    window.alert(text(root, "no_address"));
                    return null;
                }
                if (popup) {
                    popup.opener = null;
                    popup.location.href = "http://" + address + "/";
                    return null;
                }
                var shown = formAddress();
                if (shown !== null && shown !== address) {
                    window.alert(text(root, "unsaved"));
                    return null;
                }
                return runTest(root, id, address).then(refreshForm);
            })
            .then(null, function (error) {
                if (popup) {
                    popup.close();
                }
                var message = error && error.message ? error.message : "" + error;
                if (message) {
                    window.alert(message);
                }
            })
            .then(function () {
                busy = false;
                trigger.disabled = false;
            });
    }

    document.addEventListener("click", onAction, true);
})();
