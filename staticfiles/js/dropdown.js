(function () {
    const toggles = document.querySelectorAll("[data-dropdown-toggle]");

    function closeAll() {
        document.querySelectorAll("[data-dropdown-menu]").forEach(function (menu) {
            menu.hidden = true;
        });
    }

    toggles.forEach(function (toggle) {
        const target = toggle.getAttribute("data-dropdown-toggle");
        const menu = document.querySelector('[data-dropdown-menu="' + target + '"]');
        if (!menu) return;

        toggle.addEventListener("click", function (event) {
            event.stopPropagation();
            const isOpen = !menu.hidden;
            closeAll();
            menu.hidden = isOpen;
        });

        menu.addEventListener("click", function (event) {
            event.stopPropagation();
        });
    });

    document.addEventListener("click", closeAll);
})();
