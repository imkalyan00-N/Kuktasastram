document.getElementById('predictForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const date = document.getElementById('matchDate').value;
    const timeSlot = parseInt(document.getElementById('timeSlot').value);
    const punju1 = document.getElementById('punju1').value;
    const punju2 = document.getElementById('punju2').value;

    if(punju1 === punju2) {
        alert("Rendu same punjulu select chesav bro! Change cheyyi.");
        return;
    }

    const payload = {
        date: date,
        time_slot: timeSlot,
        punju_1: punju1,
        punju_2: punju2
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        // Update UI
        document.getElementById('winnerText').innerText = data.winner;
        document.getElementById('directionText').innerText = data.direction;
        document.getElementById('reasoningText').innerText = data.reasoning;
        
        document.getElementById('resultBox').classList.remove('hidden');

    } catch (error) {
        console.error("Error predicting:", error);
        alert("Backend API thagulthaledu. Server run avuthunda leda check chey.");
    }
});
