var socket = new WebSocket('ws://127.0.0.1:8070/ws');  // specify the WebSocket URL of your FastAPI server here

document.getElementById('selectImage').addEventListener('click', function() {
    var fileInput = document.getElementById('fileInput');
    fileInput.click();
});

document.getElementById('fileInput').addEventListener('change', function() {
    var file = this.files[0];
    var formData = new FormData();
    formData.append('file', file);

    // Display the selected image
    var img = document.getElementById('displayImage');
    img.src = URL.createObjectURL(file);
    img.style.display = 'block';

    fetch('http://127.0.0.1:8070/predict', {  // specify the URL of your FastAPI server here
        method: 'POST',
        body: formData
    })
    .then(response => response.json())  // Parse the response as JSON
    .then(result => {
        console.log('Result:', result);

        // Check if the result contains a 'message' property
        if (result.message) {
            // If it does, display the message
            document.getElementById('result').textContent = result.message;
        } else {
            // Ensure the confidence does not exceed 100%
            var confidence = Math.min(result.confidence, 100);
            // Format the confidence to 2 decimal places
            confidence = confidence.toFixed(2);
            // Display the prediction and confidence in the desired format
            document.getElementById('result').innerHTML = "This is " + result.prediction + ".<br>Confidence: " + confidence + "%";
        }
    });
});