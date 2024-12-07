let sipChart;
let mfChart;

function updateSIPValues() {
    const monthlyInvestment = parseFloat(document.getElementById('monthlyInvestment').value);
    const expectedReturn = parseFloat(document.getElementById('expectedReturn').value) / 100;
    const timePeriod = parseFloat(document.getElementById('timePeriodSIP').value);

    // Update displayed values
    document.getElementById('monthlyInvestmentValue').innerText = `₹${monthlyInvestment.toLocaleString()}`;
    document.getElementById('expectedReturnValue').innerText = `${(expectedReturn * 100).toFixed(1)}%`;
    document.getElementById('timePeriodSIPValue').innerText = `${timePeriod} Yr`;

    // Calculate SIP values
    const totalInvestment = monthlyInvestment * timePeriod * 12;
    const estimatedReturns = calculateSIPReturns(monthlyInvestment, expectedReturn, timePeriod);
    const totalValue = totalInvestment + estimatedReturns;

    // Update results
    document.getElementById('sipInvestedAmount').innerText = `₹${totalInvestment.toLocaleString()}`;
    document.getElementById('sipEstimatedReturns').innerText = `₹${estimatedReturns.toLocaleString()}`;
    document.getElementById('sipTotalValue').innerText = `₹${totalValue.toLocaleString()}`;

    // Update SIP Chart
    updateSIPChart(totalInvestment, estimatedReturns);
}

function calculateSIPReturns(monthlyInvestment, rateOfReturn, timePeriod) {
    const months = timePeriod * 12;
    let futureValue = 0;

    for (let i = 0; i < months; i++) {
        futureValue += monthlyInvestment * Math.pow(1 + rateOfReturn / 12, months - i);
    }

    return futureValue - (monthlyInvestment * months);
}

function updateSIPChart(investedAmount, estimatedReturns) {
    if (sipChart) {
        sipChart.destroy(); // Destroy previous chart instance
    }

    const ctx = document.getElementById('sipChart').getContext('2d');
    sipChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Invested Amount', 'Estimated Returns'],
            datasets: [{
                data: [investedAmount, estimatedReturns],
                backgroundColor: ['#36A2EB', '#FF6384'],
                hoverBackgroundColor: ['#36A2EB', '#FF6384']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'SIP Investment Breakdown'
                }
            }
        }
    });
}

function updateMFValues() {
    const totalInvestment = parseFloat(document.getElementById('totalInvestment').value);
    const expectedReturnRate = parseFloat(document.getElementById('expectedReturnRate').value) / 100;
    const timePeriod = parseFloat(document.getElementById('timePeriodMF').value);

    // Update displayed values
    document.getElementById('totalInvestmentValue').innerText = `₹${totalInvestment.toLocaleString()}`;
    document.getElementById('expectedReturnRateValue').innerText = `${(expectedReturnRate * 100).toFixed(1)}%`;
    document.getElementById('timePeriodMFValue').innerText = `${timePeriod} Yr`;

    // Calculate Mutual Fund values
    const estimatedReturns = calculateMFReturns(totalInvestment, expectedReturnRate, timePeriod);
    const totalValue = totalInvestment + estimatedReturns;

    // Update results
    document.getElementById('mfInvestedAmount').innerText = `₹${totalInvestment.toLocaleString()}`;
    document.getElementById('mfEstimatedReturns').innerText = `₹${estimatedReturns.toLocaleString()}`;
    document.getElementById('mfTotalValue').innerText = `₹${totalValue.toLocaleString()}`;

    // Update Mutual Fund Chart
    updateMFChart(totalInvestment, estimatedReturns);
}

function calculateMFReturns(investment, rateOfReturn, timePeriod) {
    return investment * Math.pow(1 + rateOfReturn, timePeriod) - investment;
}

function updateMFChart(investedAmount, estimatedReturns) {
    if (mfChart) {
        mfChart.destroy(); // Destroy previous chart instance
    }

    const ctx = document.getElementById('returnsChart').getContext('2d');
    mfChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels : ['Invested Amount', 'Estimated Returns'],
            datasets: [{
                data: [investedAmount, estimatedReturns],
                backgroundColor: ['#4BC0C0', '#FF9F40'],
                hoverBackgroundColor: ['#4BC0C0', '#FF9F40']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Mutual Fund Investment Breakdown'
                }
            }
        }
    });
}

// Initialize charts on page load
window.onload = function() {
    updateSIPValues();
    updateMFValues();
}; 