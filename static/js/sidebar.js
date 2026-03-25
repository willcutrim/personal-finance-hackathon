(function () {
    const shell = document.querySelector(".app-shell");
    const toggle = document.querySelector("[data-sidebar-toggle]");
    const overlay = document.querySelector("[data-sidebar-overlay]");

    if (!shell || !toggle) return;

    function openSidebar() {
        shell.classList.add("is-sidebar-open");
    }

    function closeSidebar() {
        shell.classList.remove("is-sidebar-open");
    }

    toggle.addEventListener("click", function () {
        if (shell.classList.contains("is-sidebar-open")) {
            closeSidebar();
        } else {
            openSidebar();
        }
    });

    if (overlay) {
        overlay.addEventListener("click", closeSidebar);
    }
})();
