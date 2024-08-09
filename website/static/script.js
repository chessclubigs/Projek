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

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Sticky header on scroll
window.onscroll = function() {stickyHeader()};

var header = document.querySelector('header');
var sticky = header.offsetTop;

function stickyHeader() {
    if (window.pageYOffset > sticky) {
        header.classList.add('sticky');
    } else {
        header.classList.remove('sticky');
    }
}

// Back-to-top button
var backToTopButton = document.createElement('button');
backToTopButton.innerText = '↑';
backToTopButton.classList.add('back-to-top');
document.body.appendChild(backToTopButton);

backToTopButton.addEventListener('click', function() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

window.addEventListener('scroll', function() {
    if (window.scrollY > 300) {
        backToTopButton.classList.add('visible');
    } else {
        backToTopButton.classList.remove('visible');
    }
});

// Simple form validation
document.querySelector('form').addEventListener('submit', function(e) {
    var isValid = true;
    var inputs = this.querySelectorAll('input[type="text"], input[type="password"]');
    
    inputs.forEach(input => {
        if (input.value.trim() === "") {
            input.classList.add('error');
            isValid = false;
        } else {
            input.classList.remove('error');
        }
    });
    
    if (!isValid) {
        e.preventDefault();
        alert('Please fill out all fields.');
    }
});

// Mobile navigation toggle
var navToggle = document.createElement('button');
navToggle.innerText = '☰';
navToggle.classList.add('nav-toggle');
document.querySelector('header').appendChild(navToggle);

navToggle.addEventListener('click', function() {
    var menuList = document.querySelector('.menu-list');
    menuList.classList.toggle('open');
});

document.addEventListener('DOMContentLoaded', function() {
    var lazyImages = [].slice.call(document.querySelectorAll('img.lazy'));

    if ('IntersectionObserver' in window) {
        let lazyImageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    let lazyImage = entry.target;
                    lazyImage.src = lazyImage.dataset.src;
                    lazyImage.classList.remove('lazy');
                    lazyImageObserver.unobserve(lazyImage);
                }
            });
        });

        lazyImages.forEach(function(lazyImage) {
            lazyImageObserver.observe(lazyImage);
        });
    } else {
        // Fallback for older browsers
        lazyImages.forEach(function(image) {
            image.src = image.dataset.src;
        });
    }
});

// Animations on scroll
window.addEventListener('scroll', function() {
    var elements = document.querySelectorAll('.animate-on-scroll');
    var scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    elements.forEach(function(element) {
        var elementPosition = element.getBoundingClientRect().top + scrollTop;

        if (scrollTop + window.innerHeight >= elementPosition) {
            element.classList.add('animated');
        }
    });
});


// Currently Buggy
// document.addEventListener("DOMContentLoaded", function() {
//     const rows = document.querySelectorAll(".leaderboard-container tbody tr");
//     const winRates = [];

//     const podiumClasses = ["gold", "silver", "chocolate"];

//     rows.forEach((row) => {
//         const value = row.querySelector("td:nth-child(3)").innerHTML;
//         if (winRates.length === 0 || value !== winRates[winRates.length - 1]) {
//             winRates.push(value);
//         }
//         if (winRates.length > 3) {
//             return;
//         }
//         row.classList.add(podiumClasses[winRates.length - 1]);
//     });
// });