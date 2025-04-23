window.addEventListener("load", function () {
    const el = document.getElementById("msg-end");
    if (el) {
        el.scrollIntoView({ behavior: "smooth", block: "end" });
    }
});
