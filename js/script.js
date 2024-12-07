// script.js

// Function to fetch student data from the server
async function fetchStudentData() {
    try {
        const response = await fetch('/api/students'); // Replace with your actual API endpoint
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching student data:', error);
    }
}

// Function to calculate insights and update the cards
function updateCards(studentData) {
    const totalStudents = studentData.length;
    const averageGrade = studentData.reduce((sum, student) => sum + student.final_grade, 0) / totalStudents;
    const averageAttendance = studentData.reduce((sum, student) => sum + student.attendance_rate, 0) / totalStudents;

    document.getElementById('totalStudents').innerText = totalStudents;
    document.getElementById('averageGrade').innerText = averageGrade.toFixed(2) + '%';
    document.getElementById('averageAttendance').innerText = averageAttendance.toFixed(2) + '%';
}

// Function to create the chart
function createChart(studentData) {
    const labels = studentData.map(student => student.name);
    const finalGrades = studentData.map(student => student.final_grade);
    const attendanceRates = studentData.map(student => student.attendance_rate);

    const ctx = document.getElementById('studentChart').getContext('2d');
    
    // Clear previous chart if it exists
    if (window.studentChart) {
        window.studentChart.destroy();
    }

    window.studentChart = new Chart(ctx, {
        type: 'bar', // You can change this to 'line', 'pie', etc.
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Final Grades (%)',
                    data: finalGrades,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Attendance Rates (%)',
                    data: attendanceRates,
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Function to handle the button click event
async function visualizeData() {
    const studentData = await fetchStudentData();
    if (studentData) {
        updateCards(studentData);
        createChart(studentData);
    }
}

// Add event listener to the button
document.getElementById('visualizeButton').addEventListener('click', visualizeData);