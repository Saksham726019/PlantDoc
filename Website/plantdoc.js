// Initialize WebSocket (remove if not using WebSocket for this part)
// var socket = new WebSocket('ws://127.0.0.1:8070/ws');

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

    fetch('http://127.0.0.1:8070/predict', {  // URL of the FastAPI server
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        console.log('Result:', result);

        // Update the result element
        var resultElement = document.getElementById('predictionResult');  // Correct ID
        if (result.message) {
            resultElement.textContent = result.message;
        } else {
            var confidence = Math.min(result.confidence * 100, 100).toFixed(2);
            resultElement.innerHTML = "This is " + result.predicted_class + ".<br>Confidence: " + confidence + "%";
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('predictionResult').textContent = "Error processing the image.";
    });
});
