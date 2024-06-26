<?php

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['video'])) {
    $targetDir = "uploads/";
    $targetFile = $targetDir . basename($_FILES["video"]["name"]);
    $uploadOk = 1;
    $videoFileType = strtolower(pathinfo($targetFile, PATHINFO_EXTENSION));

    $check = getimagesize($_FILES["video"]["tmp_name"]);
    if ($check !== false) {
        echo json_encode(["error" => "File is not a video."]);
        $uploadOk = 0;
    }

    if (file_exists($targetFile)) {
        echo json_encode(["error" => "Sorry, file already exists."]);
        $uploadOk = 0;
    }

    if ($_FILES["video"]["size"] > 50000000) { // 50MB limit
        echo json_encode(["error" => "Sorry, your file is too large."]);
        $uploadOk = 0;
    }


    if ($videoFileType != "mp4" && $videoFileType != "avi" && $videoFileType != "mov" && $videoFileType != "mpeg") {
        echo json_encode(["error" => "Sorry, only MP4, AVI, MOV & MPEG files are allowed."]);
        $uploadOk = 0;
    }

    if ($uploadOk == 0) {
        echo json_encode(["error" => "Sorry, your file was not uploaded."]);

    } else {
        if (move_uploaded_file($_FILES["video"]["tmp_name"], $targetFile)) {
         $results = analyzeVideo($targetFile);
            echo json_encode($results);
        } else {
            echo json_encode(["error" => "Sorry, there was an error uploading your file."]);
        }
    }
} else {
    echo json_encode(["error" => "Invalid request."]);
}

function analyzeVideo($videoPath) {
   return ["message" => "Video analysis completed", "details" => "Object counts and other details"];
}
