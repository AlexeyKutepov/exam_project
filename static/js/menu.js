/**
 * Created by Kutepov Alexey on 27.04.15.
 */


window.onload=function() {
    var pathname = window.location.pathname;

    if (pathname.indexOf('dashboard') + 1) {
        $("#liDashboard").addClass("active");
    } else if (pathname.indexOf('create_new_test') + 1) {
        $("#liTestConstructor").addClass("active");
    } else if (pathname.indexOf('create_new_question') + 1) {
        $("#liTestConstructor").addClass("active");
    } else if (pathname.indexOf('tests') + 1) {
        $("#liTests").addClass("active");
    } else if (pathname.indexOf('start_test') + 1) {
        $("#liTests").addClass("active");
    } else if (pathname.indexOf('next_question') + 1) {
        $("#liTests").addClass("active");
    } else if (pathname.indexOf('end_test') + 1) {
        $("#liTests").addClass("active");
    }
};