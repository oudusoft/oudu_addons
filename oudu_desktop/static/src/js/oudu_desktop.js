(function () {
    "use strict";

    function isDesktop() {
        return !!document.querySelector("script[data-oudu-desktop-bridge]");
    }

    function renderGuide(guide) {
        if (guide.dataset.ouduRendered) {
            return;
        }
        guide.dataset.ouduRendered = "1";
        var detected = isDesktop();
        var on = guide.querySelector(".oudu_desktop_guide_detected");
        var off = guide.querySelector(".oudu_desktop_guide_not_detected");
        if (on) {
            on.hidden = !detected;
        }
        if (off) {
            off.hidden = detected;
        }
    }

    function scan() {
        var nodes = document.querySelectorAll(".oudu_desktop_guide");
        for (var i = 0; i < nodes.length; i++) {
            renderGuide(nodes[i]);
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", scan);
    } else {
        scan();
    }

    var scanTimer = null;
    function scheduleScan() {
        if (scanTimer) {
            return;
        }
        scanTimer = setTimeout(function () {
            scanTimer = null;
            scan();
        }, 250);
    }

    new MutationObserver(scheduleScan).observe(document.documentElement, {
        childList: true,
        subtree: true,
    });
})();
