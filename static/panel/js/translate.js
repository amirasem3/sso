function __(element, lang_dict) {
    if (
        typeof lang_dict !== "undefined" &&
        lang_dict[element.dataset.translate]
    ) {
        element.innerText = lang_dict[element.dataset.translate];
    } else if (element.dataset.default) {
        element.innerText = element.dataset.default;
    }
}

function translate_page(lang_dict) {
    var translate_elements = document.getElementsByClassName("translate"),
        i;
    for (i = 0; i < translate_elements.length; i++) {
        __(translate_elements[i], lang_dict);
    }
}

var fa_lang = {
    dashboard: "داشبورد",
    'manage-campains': "مدیریت کمپین‌ها",
    'transaction_reports': "گزارشات مالی",
    profile: "پروفایل کاربری",
    logout: "خروج",
    balance: "موجودی:",
    toman: "تومان",
    show_all_messages: "نمایش تمامی پیام‌ها",
    admin: "ادمین"
};

var en_lang = {
    dashboard: "Dashboard",
    'manage-campains': "Campains",
    'transaction_reports': "Accounting",
    profile: "user profile",
    logout: "logout",
    balance: "balance:",
    toman: "toman",
    show_all_messages: "Show all messages",
    admin: "admin"
};

translate_page(fa_lang);