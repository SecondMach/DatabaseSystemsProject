document.addEventListener('DOMContentLoaded', () => {

    // ==================================================
    // 1. ATHLETES PAGE LOGIC (Updated for new Schema)
    // ==================================================
    const athleteTableBody = document.getElementById('athleteTableBody');
    
    // If we are on the Athlete page...
    if (athleteTableBody) {
        // Fetch data from your Python backend
        fetch('/api/athletes')
            .then(res => res.json())
            .then(data => {
                // Clear any existing placeholder rows
                athleteTableBody.innerHTML = ''; 
                
                // Loop through the athletes sent from app.py
                data.forEach(athlete => {
                    // We now use 'born_date' and 'born_country' to match app.py keys
                    const row = `
                        <tr>
                            <td>${athlete.name}</td>
                            <td>${athlete.born_date || 'N/A'}</td> 
                            <td>${athlete.born_country}</td>
                        </tr>
                    `;
                    athleteTableBody.innerHTML += row;
                });
            })
            .catch(err => console.error("Error loading athletes:", err));
    }

    // ==================================================
    // 2. ADD ATHLETE FORM LOGIC
    // ==================================================
    const athleteForm = document.querySelector('.athlete-form form');

    if (athleteForm) {
        athleteForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Get all inputs from the form
            const inputs = athleteForm.querySelectorAll('input');
            
            // Map the inputs to the keys expected by app.py
            // Make sure your HTML form inputs are in this order: Name, Date, Country
            const newAthlete = {
                Name: inputs[0].value,
                Born_date: inputs[1].value, 
                Born_country: inputs[2].value
            };

            fetch('/api/athletes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newAthlete)
            })
            .then(res => {
                if (res.ok) {
                    alert('Athlete Added Successfully!');
                    window.location.reload(); // Refresh page to see the new athlete
                } else {
                    // If app.py returns an error (like 500), show it
                    res.json().then(data => alert('Error: ' + data.error));
                }
            })
            .catch(err => alert('Network error: ' + err));
        });
    }

    // ==================================================
    // 3. ANALYTICS PAGE LOGIC (Chart.js)
    // ==================================================
    const chartCanvas = document.getElementById('goatChart');

    if (chartCanvas) {
        fetch('/api/analytics')
            .then(res => res.json())
            .then(data => {
                // app.py sends a list of objects like: { label: 'USA', value: 120 }
                new Chart(chartCanvas, {
                    type: 'bar',
                    data: {
                        labels: data.map(d => d.label), // x-axis labels
                        datasets: [{
                            label: 'Total Medals',
                            data: data.map(d => d.value), // y-axis values
                            backgroundColor: '#0057b7',   // Olympic Blue
                            borderColor: '#0057b7',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: { beginAtZero: true }
                        }
                    }
                });
            });
    }

    // ==================================================
    // 4. LOGIN LOGIC
    // ==================================================
    const loginForm = document.querySelector('.login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            
            // Simple mock login for demonstration
            if (username) {
                alert(`Welcome back, ${username}!`);
                window.location.href = '/index.html';
            }
        });
    }
});