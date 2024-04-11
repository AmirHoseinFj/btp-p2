// Function to make a reservation
async function makeReservation() {
    const customerName = document.getElementById('name').value;
    const reservationDate = document.getElementById('reservation-date').value;
    const reservationTime = document.getElementById('reservation-time').value;
    const amountP = document.getElementById('amount').value;

    const reservationData = {
        customer_name: customerName,
        reservation_date: reservationDate,
        reservation_time: reservationTime,
        amount: parseInt(amountP),
        reservation_id: Math.random().toString(36).substr(2, 9) // Simple unique ID generator
    };

    try {
        const response = await fetch('http://localhost:8080/reservations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(reservationData),
        });

        if (response.ok) {
            alert("Reservation successful!");
            window.location.href = "confirm.html";
        } else {
            const text = await response.text();
            throw new Error(text);
        }
    } catch (error) {
        console.error('Error:', error);
        alert("Reservation failed. Please try again.");
    }
}

// Function to fetch and display reservations
async function getReservations() {
    try {
        const response = await fetch('http://localhost:8080/reservations');
        const data = await response.json();

        const reservationList = document.getElementById('reservation-list');
        reservationList.innerHTML = '';

        data.reservations.forEach(reservation => {
            const listItem = document.createElement('li');
            listItem.textContent = `ID: ${reservation.reservation_id}, Name: ${reservation.customer_name}, Date: ${reservation.reservation_date}, Time: ${reservation.reservation_time}, Amount of People: ${reservation.amount}`;
            
            
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.addEventListener('click', function() {
                deleteReservation(reservation.reservation_id);
            });

            listItem.appendChild(deleteButton);
            reservationList.appendChild(listItem);
        });
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('reservation-list').innerHTML = 'Failed to load reservations.';
    }
}
async function deleteReservation(reservationId) {
    try {
        const response = await fetch(`http://localhost:8080/reservations/${reservationId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            alert("Reservation deleted successfully!");
            window.location.reload(); // Refresh the page to reload the reservation list
        } else {
            const text = await response.text();
            throw new Error(text);
        }
    } catch (error) {
        console.error('Error:', error);
        alert("Failed to delete reservation. Please try again.");
    }
}

document.addEventListener('DOMContentLoaded', function() {
    getReservations();
});
