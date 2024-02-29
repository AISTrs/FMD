// function to toggle dorp down arrow in nav
document.addEventListener('DOMContentLoaded', function () {
    var accordionButton = document.getElementById("nav-committee-accordion")

    accordionButton.addEventListener('click', function () {
        var arrowIcon = document.getElementById('collapse-arrow-icon');

        if (arrowIcon && this.getAttribute('aria-expanded') === 'true') {
            arrowIcon.classList.remove('bi-chevron-down');
            arrowIcon.classList.add('bi-chevron-up');
        } else if (arrowIcon) {
            arrowIcon.classList.remove('bi-chevron-up');
            arrowIcon.classList.add('bi-chevron-down');
        }

    });

});


// function to hide text in nav bar
document.addEventListener('DOMContentLoaded', function () {
    var nav = document.getElementById('base-nav-layout');

    var navTextElements = document.querySelectorAll('.nav-text');
    var contentDiv = document.getElementById('div-container-fluid-content')

    nav.addEventListener('mouseenter', function () {
        navTextElements.forEach(function (element) {
            element.style.opacity = '1';
        });
        contentDiv.style.left = '200px';
    });

    nav.addEventListener('mouseleave', function () {

        var accordion = document.getElementById('collapseCommittee');
        accordion.setAttribute('aria-expanded', 'false');
        accordion.classList.remove('show');

        navTextElements.forEach(function (element) {
            element.style.opacity = '0';
        });

        contentDiv.style.left = '90px';

        var arrowIcon = document.getElementById('collapse-arrow-icon');

        // reset arrow direction
        if (arrowIcon && this.getAttribute('aria-expanded') === 'true') {
            arrowIcon.classList.remove('bi-chevron-down');
            arrowIcon.classList.add('bi-chevron-up');
        } else if (arrowIcon) {
            arrowIcon.classList.remove('bi-chevron-up');
            arrowIcon.classList.add('bi-chevron-down');
        }
    });
});