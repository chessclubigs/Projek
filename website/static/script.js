"use strict";

const timezoneOffset = new Date().getTimezoneOffset();

fetch("/set_timezone_offset", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({ timezoneOffset })
}).catch(error => {
    console.error("Error:", error);
});

document.addEventListener("DOMContentLoaded", function() {
    const rows = document.querySelectorAll(".leaderboard-container tbody tr");
    const winRates = [];

    const podiumClasses = ["gold", "silver", "chocolate"];

    rows.forEach((row) => {
        const value = row.querySelector("td:nth-child(3)").innerHTML;
        if (winRates.length === 0 || value !== winRates[winRates.length - 1]) {
            winRates.push(value);
        }
        if (winRates.length > 3) {
            return;
        }
        row.classList.add(podiumClasses[winRates.length - 1]);
    });
});
