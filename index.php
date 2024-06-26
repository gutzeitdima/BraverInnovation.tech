<head>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
<div class="container">
    <form id="uploadForm">
        <div class="form-group">
            <label for="videoInput">Choose File</label>
            <input type="file" id="videoInput" accept="video/*">
            <button type="button" id="uploadButton">Upload</button>
            <span class="file-name" id="fileName">No file chosen</span>
        </div>
    </form>
    <video id="videoPlayer" controls></video>
    <div class="button-group">
        <button id="analyzeButton">Start Analyzing</button>
        <button id="fullAccessButton">Get Full Access</button>
    </div>
</div>
<script src="script.js"></script>
</body>