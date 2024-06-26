const videoInput = document.getElementById('videoInput');
const uploadButton = document.getElementById('uploadButton');
const videoPlayer = document.getElementById('videoPlayer');
const analyzeButton = document.getElementById('analyzeButton');
const fullAccessButton = document.getElementById('fullAccessButton');
const fileNameDisplay = document.getElementById('fileName');

uploadButton.addEventListener('click', function() {
    const file = videoInput.files[0];
    if (file) {
        const url = URL.createObjectURL(file);
        videoPlayer.src = url;
        videoPlayer.style.display = 'block'; // Show video player
        videoPlayer.load();
        analyzeButton.style.display = 'inline-block'; // Show analyze button
        fullAccessButton.style.display = 'inline-block'; // Show full access button
    } else {
        alert('Please select a video file first.');
    }
});

videoInput.addEventListener('change', function() {
    const fileName = videoInput.files[0] ? videoInput.files[0].name : 'No file chosen';
    fileNameDisplay.textContent = fileName;
});

analyzeButton.addEventListener('click', function() {
const file = videoInput.files[0];
if (file) {
    const formData = new FormData();
    formData.append('video', file);

    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error analyzing video: ' + data.error);
        } else {
            console.log('Analysis results:', data);
            displayAnalysisResults(data);
            alert('Analysis completed. Check the console for results.');
        }
    })
    .catch(error => {
        console.error('Error analyzing video:', error);
        alert('Error analyzing video.');
    });
} else {
    alert('Please upload a video first.');
}
});

function displayAnalysisResults(data) {
// Display the analysis results on the web page
// This function can be customized to show detailed analysis results
const resultsContainer = document.createElement('div');
resultsContainer.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
document.body.appendChild(resultsContainer);
}

fullAccessButton.addEventListener('click', function() {
    window.location.href = 'https://www.braverinnovation.tech/#contact';
});