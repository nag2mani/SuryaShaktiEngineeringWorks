function updateClock() {
    const now = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };
    const dateTime = now.toLocaleDateString('en-IN', options);
    document.getElementById('clock').textContent = dateTime;
}

// Update every second
setInterval(updateClock, 1000);
// Initial call to display immediately
updateClock();


function toggleEmployeeDropdown() {
    var checkBox = document.getElementById('is_employee_expense');
    var dropdown = document.getElementById('employee-dropdown');
    if (checkBox.checked == true) {
        dropdown.style.display = 'block';
    } else {
        dropdown.style.display = 'none';
    }
}
