document.addEventListener('DOMContentLoaded', () => {
    
    // --- STATE VARIABLES ---
    let currentEditingId = null; // null = adding mode, number = editing mode

    // --- DOM ELEMENTS ---
    // We select these at the top so all functions can access them
    const athleteTableBody = document.getElementById('athleteTableBody');
    const athleteForm = document.querySelector('.athlete-form form');
    const submitBtn = athleteForm ? athleteForm.querySelector('button') : null;

    // ==================================================
    // 1. ATHLETES PAGE LOGIC
    // ==================================================
    if (athleteTableBody) {
        fetch('/api/athletes')
            .then(res => res.json())
            .then(data => {
                athleteTableBody.innerHTML = '';
                data.forEach(athlete => {
                    const row = document.createElement('tr');
                    
                    // Note: We use the keys sent from app.py
                    row.innerHTML = `
                        <td>${athlete.id}</td>
                        <td>${athlete.born_date}</td>
                        <td>${athlete.born_country}</td>
                        <td>${athlete.first_name}</td>
                        <td>${athlete.last_name}</td>
                        <td>
                            <button class="edit-btn">✎</button>
                            <button class="delete-btn">🗑</button>
                        </td>
                    `;
                    
                    // Attach Event Listener to the specific Edit button in this row
                    const editBtn = row.querySelector('.edit-btn');
                    editBtn.addEventListener('click', () => {
                        populateFormForEdit(athlete);
                    });

                    const deleteBtn = row.querySelector('.delete-btn');
                    deleteBtn.addEventListener('click', () => {
                        if (confirm(`Are you sure you want to delete athlete: ${athlete.first_name} ${athlete.last_name}?`)) {
                            fetch(`/api/athletes/${athlete.id}`, {
                                method: 'DELETE'
                            })
                            .then(res => {
                                if (res.ok) {
                                    alert('Athlete Deleted Successfully!');
                                    window.location.reload(); 
                                } else {
                                    res.json().then(data => alert('Error: ' + data.error));
                                }
                            });
                        }
                    });

                    athleteTableBody.appendChild(row);
                });
            })
            .catch(err => console.error("Error loading athletes:", err));
    }

    // ===============================
    // ATHLETE SEARCH BAR
    // ===============================
    const searchInput = document.getElementById('athleteSearch');

    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                runAthleteSearch(searchInput.value.trim());
            }
        });
    }

    function runAthleteSearch(query) {
        fetch(`/api/search_athletes?q=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(data => {
                athleteTableBody.innerHTML = ""; // clear table

                if (data.length === 0) {
                    // Show placeholder row
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td colspan="6" style="text-align:center; padding:1.5rem; color:#777;">
                            ❌ No results found for "<strong>${query}</strong>"
                        </td>
                    `;
                    athleteTableBody.appendChild(row);
                    return;
                }

                data.forEach(athlete => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${athlete.id}</td>
                        <td>${athlete.born_date}</td>
                        <td>${athlete.born_country}</td>
                        <td>${athlete.first_name}</td>
                        <td>${athlete.last_name}</td>
                        <td>
                            <button class="edit-btn">✎</button>
                            <button class="delete-btn">🗑</button>
                        </td>
                    `;

                    // reattach edit/delete listeners
                    row.querySelector('.edit-btn').addEventListener('click', () => {
                        populateFormForEdit(athlete);
                    });

                    row.querySelector('.delete-btn').addEventListener('click', () => {
                        if (confirm(`Are you sure you want to delete ${athlete.first_name} ${athlete.last_name}?`)) {
                            fetch(`/api/athletes/${athlete.id}`, { method: 'DELETE' })
                                .then(r => r.ok ? window.location.reload() : alert("Error deleting"));
                        }
                    });

                    athleteTableBody.appendChild(row);
                });
            })
            .catch(err => console.error("Search error:", err));
    }

    //Helper function to fill the form when "Edit" is clicked
    function populateFormForEdit(athlete) {
        if (!athleteForm) return;

        const inputs = athleteForm.querySelectorAll('input');
        
        // Fill inputs with the existing data from the row
        // Indices match the HTML form order: Date, Country, First, Last
        inputs[0].value = athlete.born_date;
        inputs[1].value = athlete.born_country;
        inputs[2].value = athlete.first_name;
        inputs[3].value = athlete.last_name;

        // Set the state to "Editing" using the ID from the database
        currentEditingId = athlete.id; 

        // Visual feedback
        submitBtn.textContent = "Update Athlete"; 
        submitBtn.style.backgroundColor = "#ffcc00"; // Gold color for edit mode
        
        // Scroll user to the form
        athleteForm.scrollIntoView({ behavior: 'smooth' });
    }

    // ==================================================
    // 2. FORM SUBMIT LOGIC (Handles ADD and EDIT)
    // ==================================================
    if (athleteForm) {
        athleteForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const inputs = athleteForm.querySelectorAll('input');
            
            // Map inputs to the exact keys your app.py expects
            const athleteData = {
                Born_date: inputs[0].value, 
                Born_country: inputs[1].value,
                FirstName: inputs[2].value,
                LastName: inputs[3].value
            };

            if (currentEditingId) {
                // === EDIT MODE (PUT) ===
                fetch(`/api/athletes/${currentEditingId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(athleteData)
                })
                .then(res => {
                    if (res.ok) {
                        alert('Athlete Updated Successfully!');
                        window.location.reload(); 
                    } else {
                        res.json().then(data => alert('Error: ' + data.error));
                    }
                });

            } else {
                // === ADD MODE (POST) ===
                fetch('/api/athletes', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(athleteData)
                })
                .then(res => {
                    if (res.ok) {
                        alert('Athlete Added Successfully!');
                        window.location.reload(); 
                    } else {
                        res.json().then(data => alert('Error: ' + data.error));
                    }
                });
            }
        });
    }

    // ==================================================
    // 3. ANALYTICS PAGE LOGIC (Chart.js)
    // ==================================================
    const goatTableBody = document.getElementById('goatTableBody');

    if (goatTableBody) {
        fetch('/api/analytics')
            .then(res => res.json())
            .then(data => {
                // Populate the GOAT table
                goatTableBody.innerHTML = data.map(d => `
                    <tr>
                        <td>${d.Name}</td>
                        <td>${d["Medal Count"]}</td>
                    </tr>
                `).join('');
            });
    }
    //                 data: {
    //                     labels: data.map(d => d.label),
    //                     datasets: [{
    //                         label: 'Total Medals',
    //                         data: data.map(d => d.value),
    //                         backgroundColor: '#0057b7',
    //                         borderColor: '#0057b7',
    //                         borderWidth: 1
    //                     }]
    //                 },
    //                 options: {
    //                     responsive: true,
    //                     scales: {
    //                         y: { beginAtZero: true }
    //                     }
    //                 }
    //             });
    //         });
    // }

    // ==================================================
    // 4. LOGIN LOGIC
    // ==================================================
    const loginForm = document.querySelector('.login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            if (username) {
                alert(`Welcome back, ${username}!`);
                window.location.href = '/index.html';
            }
        });
    }

    // =====================================
    // 5. GAMES PAGE LOGIC
    // =====================================
    const gamesGrid = document.querySelector('.games-grid');

    if (gamesGrid) {
        
        const seasonSelect = document.querySelector('.filter-bar select:nth-child(1)');
        const yearSelect = document.querySelector('.filter-bar select:nth-child(2)');
        const filterBtn = document.querySelector('.filter-btn');
        const clearBtn = document.querySelector('.clear-btn');

        // Load years dropdown
        fetch('/api/games')
            .then(res => res.json())
            .then(data => {

                // Populate years
                const years = [...new Set(data.map(g => g.year))].sort((a,b) => b - a);
                years.forEach(year => {
                    const opt = document.createElement('option');
                    opt.value = year;
                    opt.textContent = year;
                    yearSelect.appendChild(opt);
                });

                renderGames(data);
            });

        // Filter handler
        filterBtn.addEventListener('click', () => {
            const season = seasonSelect.value;
            const year = yearSelect.value;

            const url = `/api/games/filter?season=${season}&year=${year}`;

            fetch(url)
                .then(res => res.json())
                .then(data => renderGames(data));
        });

        // Clear button handler
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {

                // Reset dropdowns
                seasonSelect.selectedIndex = 0;
                yearSelect.selectedIndex = 0;

                // Re-fetch ALL games
                fetch('/api/games')
                    .then(res => res.json())
                    .then(data => renderGames(data));
            });
        }

        // Render games
        function renderGames(games) {
            gamesGrid.innerHTML = "";

            if (games.length === 0) {
                gamesGrid.innerHTML = `<p>No games found.</p>`;
                return;
            }

            games.forEach(game => {
                const card = document.createElement('div');
                card.classList.add('game-card');

                card.innerHTML = `
                    <h3>${game.year} — ${game.season}</h3>
                    <p><strong>Host City:</strong> ${game.city}</p>
                    <p><strong>Country:</strong> ${game.country}</p>
                `;

                gamesGrid.appendChild(card);
            });
        }
    }
});
