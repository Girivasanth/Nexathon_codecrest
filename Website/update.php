<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

$file = "alert.txt";

// Debugging: Check if the file exists
if (!file_exists($file)) {
    die("❌ ERROR: alert.txt not found!");
}

// If an alert value is received, update alert.txt
if (isset($_GET['alert'])) {
    $alert = $_GET['alert'];

    // Debugging: Log the incoming request
    file_put_contents("log.txt", date("H:i:s") . " - Alert received: " . $alert . "\n", FILE_APPEND);

    $result = file_put_contents($file, $alert);
    
    if ($result !== false) {
        echo "✅ Alert updated to: " . $alert;
    } else {
        echo "❌ ERROR: Unable to write to alert.txt";
    }

    // **Reset alert.txt to 0 after 10 seconds**
    sleep(10);
    file_put_contents($file, "0");
    file_put_contents("log.txt", date("H:i:s") . " - Alert reset to 0\n", FILE_APPEND);
} else {
    echo "❌ ERROR: No alert parameter received";
}

// Debugging: Check current alert.txt value
echo "\nCurrent alert.txt Value: " . file_get_contents($file);
?>
