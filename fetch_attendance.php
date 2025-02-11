<?php
header("Content-Type: application/json");

$csvFile = "C:/Users/HARISH KUMAR V/Desktop/Attendance//attendance_log.csv";

if (!file_exists($csvFile)) {
    echo json_encode(["error" => "Attendance file not found."]);
    exit;
}

$attendanceData = [];
$handle = fopen($csvFile, "r");

// Read CSV and store data in an array
while (($row = fgetcsv($handle)) !== false) {
    if (count($row) >= 3) { // Ensure there are at least 3 columns (Name, Date, Time)
        $attendanceData[] = [
            "name" => trim($row[0]),
            "date" => trim($row[1]),
            "time" => trim($row[2])
        ];
    }
}
fclose($handle);    

echo json_encode($attendanceData); // Return data as JSON
