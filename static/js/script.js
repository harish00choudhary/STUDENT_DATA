// Student Portal JS Enhancements

document.addEventListener("DOMContentLoaded", () => {
    const input = document.querySelector("input[name='enrollment']");
    const form = document.querySelector("form");

    // Press Enter to trigger search
    input.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            e.preventDefault();
            form.submit();
        }
    });

    // Small fade-in animation for flash messages
    const flash = document.querySelector(".flash-messages");
    if (flash) {
        flash.style.opacity = 0;
        setTimeout(() => {
            flash.style.transition = "opacity 0.8s ease-in-out";
            flash.style.opacity = 1;
        }, 200);
    }
});
