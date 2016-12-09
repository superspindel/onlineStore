var ck_name = /^[A-Za-z0-9 ]{3,20}$/;
var ck_email = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i
var ck_password = /^[A-Za-z0-9!@#$%^&*()_]{6,20}$/;
var ck_zip = /^[0-9]{3,9}$/;
var ck_ssn = /^(19|20)?[0-9]{6}[- ]?[0-9]{4}$/;

function validateForm(form){
    var name = form.name.value;
    var email = form.email.value;
    var password = form.password.value;
    var zip = form.ZIP.value;
    var ssn = form.ssn.value;
    var errors = [];

    if (!ck_name.test(name)) {
        errors[errors.length] = "Skriv in ett riktigt namn.";
    }
    if (!ck_email.test(email)) {
        errors[errors.length] = "Skriv in en riktig epostadress.";
    }
    if (!ck_password.test(password)) {
        errors[errors.length] = "Skriv in ett riktigt lösenord.";
    }
    if (!ck_zip.test(zip)) {
        errors[errors.length] = "Skriv in ett ordentligt zip nummer."
    }
    if (!ck_ssn.test(ssn)) {
        errors[errors.length] = "Skriv in ett riktigt personnummer."
    }
    if (errors.length > 0) {
        reportErrors(errors);
        return false;
    }
    return true;
}
function reportErrors(errors){
    var msg = "Var vänlig fyll i korrekt data...\n";
    for (var i = 0; i<errors.length; i++) {
        var numError = i + 1;
        msg += "\n" + numError + ". " + errors[i];
    }
    alert(msg);
}
