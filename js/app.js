function submitContact(form) {
	var data = $(form).serialize();
	alert(data);
	return false;
}