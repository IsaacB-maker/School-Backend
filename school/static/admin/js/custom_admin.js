document.addEventListener("DOMContentLoaded", function () {
/*
* =====================================================
* PARACLETE CLASSICAL INTERNATIONAL SCHOOL
* SAFE DJANGO ADMIN JAVASCRIPT
* =====================================================
*
* This script only adds visual enhancements.
* It does NOT modify Django forms, buttons, saving,
* deleting, authentication, or admin actions.
*/


/* -----------------------------------------------------
   1. Confirm that our custom admin JavaScript loaded
   ----------------------------------------------------- */

document.body.classList.add("paraclete-admin-ready");


/* -----------------------------------------------------
   2. Add a class to dashboard modules when hovered
   ----------------------------------------------------- */

const modules = document.querySelectorAll(
    "#content-main .module"
);

modules.forEach(function (module) {
    module.addEventListener("mouseenter", function () {
        module.classList.add("admin-module-active");
    });

    module.addEventListener("mouseleave", function () {
        module.classList.remove("admin-module-active");
    });
});


/* -----------------------------------------------------
   3. Add a class to Django success messages
   ----------------------------------------------------- */

const successMessages = document.querySelectorAll(
    ".messagelist .success"
);

successMessages.forEach(function (message) {
    message.classList.add("paraclete-success-message");
});


/* -----------------------------------------------------
   4. Admin loaded successfully
   ----------------------------------------------------- */

console.log(
    "Paraclete Classical International School Admin loaded."
);


});
