/**
 * Created by Kutepov Alexey on 27.04.15.
 */


window.onload=function() {
    var pathname = window.location.pathname;

    if (pathname.indexOf('dashboard') + 1) {
        $("#liDashboard").addClass("active");
    } else if (pathname.indexOf('create/new/test') + 1) {
        $("#liTestConstructor").addClass("active");
    } else if (pathname.indexOf('create/new/question') + 1) {
        $("#liTestConstructor").addClass("active");
    } else if (pathname.indexOf('tests') + 1) {
        $("#liTests").addClass("active");
    } else if (pathname.indexOf('contacts') + 1) {
        $("#liContacts").addClass("active");
    } else if (pathname.indexOf('help') + 1) {
        $("#liHelp").addClass("active");
    }
};

$(function () {
  $('[data-toggle="popover"]').popover({html:true})
});