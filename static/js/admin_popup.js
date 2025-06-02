// js/admin_popup.js

// Abre o pop-up de seleção
function showAddAnotherPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^add_/, '');
    var href = triggeringLink.href;
    var win = window.open(href, name + '_popup', 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

// Atualiza o campo com o novo valor selecionado ou criado
function dismissAddAnotherPopup(win, newId, newRepr) {
    var name = win.name.replace('_popup', '');
    var elem = document.getElementById('id_' + name);
    if (elem) {
        var option = new Option(newRepr, newId, true, true);
        elem.options[elem.options.length] = option;
        elem.selectedIndex = elem.options.length - 1;
    }
    win.close();
}
