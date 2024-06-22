// Function to show clock on the home page.

function updateClock() {
    const now = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };
    const dateTime = now.toLocaleDateString('en-IN', options);
    document.getElementById('clock').textContent = dateTime;
}
setInterval(updateClock, 1000); // Update every second
updateClock(); // Initial call to display immediately

