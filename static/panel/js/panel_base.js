let dashboard = $(".dashboard");

$(".menu-toggle-btn").click(function () {
    if (!dashboard.hasClass("close-menu") && !dashboard.hasClass("open-menu")) {
        if (document.body.clientWidth > 768) {
            dashboard.addClass("close-menu");
        } else {
            dashboard.addClass("open-menu");
        }
    } else if (dashboard.hasClass("close-menu")) {
        dashboard.removeClass("close-menu");
        dashboard.addClass("open-menu");
    } else {
        if (dashboard.hasClass("open-menu")) {
            dashboard.removeClass("open-menu");
        }
        dashboard.addClass("close-menu");
    }
});

$(".dashboard-content").click(function (e) {
    if (
        document.body.clientWidth <= 768 &&
        !$(e.target).hasClass("menu-toggle-btn") &&
        !$(e.target).parents(".menu-toggle-btn").length
    ) {
        if (dashboard.hasClass("open-menu")) {
            dashboard.removeClass("open-menu");
        }
        dashboard.addClass("close-menu");
    }
});

$(".dropdown-btn").click(function () {
    $(this)
        .parent()
        .find(".dropdown-content")
        .toggleClass("hide");
});

$(".language-dropdown").click(function (e) {
    $(this)
        .children()
        .children()
        .toggleClass("hide");
    dashboard.toggleClass("rtl-dashboard");
    dashboard.toggleClass("ltr-dashboard");
    if (dashboard.hasClass("rtl-dashboard")) {
        translate_page(fa_lang);
    } else {
        translate_page(en_lang);
    }
});

$(document).click(function (e) {
    let target_parents = $(e.target).parents(".dropdown");
    $(".dropdown").each(function (index, element) {
        if (element !== target_parents[0]) {
            $(element)
                .find(".dropdown-content")
                .addClass("hide");
        }
    });
});

$(".change-page").click(function () {
    alert('!!!');
    let menu_item = $(".menu ul").find("[data-target='" + $(this).data('target') + "']");
    $(".menu ul li.activate").removeClass("activate");
    if (menu_item.length === 0) {
        if ($('.menu-bar').hasClass('selected')) {
            $('.menu-bar').removeClass('selected');
        }
    } else {
        if (!$('.menu-bar').hasClass('selected')) {
            $('.menu-bar').addClass('selected');
        }
        $(".selector-row").offset({top: menu_item[0].offsetTop + 86});
        menu_item.addClass("activate");
    }
    $('.page').removeClass('current-شpage');
    $('.' + $(this).data('target')).addClass('current-page');
    $("html, body, .dashboard-content").animate({scrollTop: 0}, 300);
});

$(".dashboard-content").scroll(function () {
    if ($(this).scrollTop() >= 0 && !$(this).hasClass('full-header')) {
        $(this).addClass('full-header')
    }
    $(".page").scrollTop($(this).scrollTop() + 5);
});

$(".page").scroll(function () {
    if ($('.dashboard-content').hasClass('full-header') && $(this).scrollTop() === 0) {
        $(".dashboard-content").removeClass('full-header')
    } else if (!$('.dashboard-content').hasClass('full-header') && $(this).scrollTop() >= 10) {
        $(".dashboard-content").addClass('full-header')
    }
});
