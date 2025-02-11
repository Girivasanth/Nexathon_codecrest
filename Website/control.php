<?php
header("Content-Type: application/json");
header("Cache-Control: no-cache, must-revalidate");
header("Expires: Mon, 26 Jul 1997 05:00:00 GMT");

$esp_ip = "http://192.168.95.32";  // Change this to your ESP32's IP
$stateFile = "relay_state.txt";   // File to store the relay state

// If state query is requested, return current relay status
if (isset($_GET['state'])) {
    $currentState = file_exists($stateFile) ? file_get_contents($stateFile) : "off";
    echo json_encode(["status" => trim($currentState)]);
    exit;
}

// Control relay via GET request
if (isset($_GET['relay'])) {
    $command = $_GET['relay'];

    if ($command == "on") {
        file_put_contents($stateFile, "on"); // Save state
        file_get_contents("$esp_ip/on");
        echo json_encode(["status" => "on"]);
    } elseif ($command == "off") {
        file_put_contents($stateFile, "off"); // Save state
        file_get_contents("$esp_ip/off");
        echo json_encode(["status" => "off"]);
    }
}
?>