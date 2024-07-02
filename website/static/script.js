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