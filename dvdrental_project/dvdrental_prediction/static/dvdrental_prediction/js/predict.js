document.addEventListener("DOMContentLoaded", function () {
    const statusBox = document.getElementById("statusBox");
    const predictionChart = document.getElementById("predictionChart");

    // Example input data, replace with actual input collection
    const inputData = {
        store_id: 1,
        active: 1,
        total_payment: 150,
        payment_count: 3,
        average_payment: 50
    };

    // Send the data to the backend
    fetch('/predict-customer/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(inputData)
    })
    .then(response => response.json())
    .then(data => {
        // Once the response is received, update the chart with the prediction
        if (data.prediction !== undefined) {
            statusBox.textContent = `Prediction: ${data.prediction}`;

            // Create the chart using Chart.js
            new Chart(predictionChart, {
                type: 'bar', // You can change this to line, pie, etc.
                data: {
                    labels: ['Class 0', 'Class 1'], // Adjust as per your classes
                    datasets: [{
                        label: 'Prediction Probability',
                        data: data.probability, // Probability array received from the backend
                        backgroundColor: ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)'],
                        borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)'],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        } else {
            statusBox.textContent = 'Error: Could not fetch prediction.';
        }
    })
    .catch(error => {
        statusBox.textContent = 'Error: ' + error.message;
    });
});