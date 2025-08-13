/**
 * Chart Management for Performance Championship Dashboard
 */

// Chart configuration
const chartConfig = {
    colors: {
        snapdragon: '#e31837',
        intel: '#0071c5',
        grid: '#2a3142',
        text: '#b4b9c4'
    },
    maxDataPoints: 20
};

// Initialize additional charts
function initializeAdvancedCharts() {
    // Temperature comparison chart
    initializeTemperatureChart();
    
    // Battery drain chart
    initializeBatteryChart();
    
    // Performance score chart
    initializeScoreChart();
}

// Temperature comparison chart
function initializeTemperatureChart() {
    const canvas = document.createElement('canvas');
    canvas.id = 'temperatureChart';
    
    // Add to a chart container if exists
    const container = document.getElementById('additionalCharts');
    if (!container) return;
    
    container.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Idle', 'Light Load', 'Heavy Load', 'Stress Test'],
            datasets: [
                {
                    label: 'Snapdragon',
                    data: [35, 40, 45, 55],
                    backgroundColor: 'rgba(227, 24, 55, 0.7)',
                    borderColor: '#e31837',
                    borderWidth: 2
                },
                {
                    label: 'Intel',
                    data: [45, 55, 75, 95],
                    backgroundColor: 'rgba(0, 113, 197, 0.7)',
                    borderColor: '#0071c5',
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Temperature Comparison (°C)',
                    color: chartConfig.colors.text
                },
                legend: {
                    labels: {
                        color: chartConfig.colors.text
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        color: chartConfig.colors.text
                    },
                    grid: {
                        color: chartConfig.colors.grid
                    }
                },
                x: {
                    ticks: {
                        color: chartConfig.colors.text
                    },
                    grid: {
                        color: chartConfig.colors.grid
                    }
                }
            }
        }
    });
}

// Battery drain chart
function initializeBatteryChart() {
    const canvas = document.createElement('canvas');
    canvas.id = 'batteryChart';
    
    const container = document.getElementById('additionalCharts');
    if (!container) return;
    
    container.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['0 min', '30 min', '60 min', '90 min', '120 min', '150 min', '180 min'],
            datasets: [
                {
                    label: 'Snapdragon Battery',
                    data: [100, 97, 94, 91, 88, 85, 82],
                    borderColor: '#e31837',
                    backgroundColor: 'rgba(227, 24, 55, 0.1)',
                    tension: 0.4,
                    borderWidth: 3
                },
                {
                    label: 'Intel Battery',
                    data: [100, 93, 85, 76, 65, 52, 38],
                    borderColor: '#0071c5',
                    backgroundColor: 'rgba(0, 113, 197, 0.1)',
                    tension: 0.4,
                    borderWidth: 3
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Battery Life Comparison',
                    color: chartConfig.colors.text
                },
                legend: {
                    labels: {
                        color: chartConfig.colors.text
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        color: chartConfig.colors.text,
                        callback: function(value) {
                            return value + '%';
                        }
                    },
                    grid: {
                        color: chartConfig.colors.grid
                    }
                },
                x: {
                    ticks: {
                        color: chartConfig.colors.text
                    },
                    grid: {
                        color: chartConfig.colors.grid
                    }
                }
            }
        }
    });
}

// Performance score chart
function initializeScoreChart() {
    const canvas = document.createElement('canvas');
    canvas.id = 'scoreChart';
    
    const container = document.getElementById('additionalCharts');
    if (!container) return;
    
    container.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    
    return new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['AI Performance', 'Battery Life', 'Temperature', 'Fan Noise', 'Overall Speed'],
            datasets: [
                {
                    label: 'Snapdragon',
                    data: [95, 90, 85, 100, 88],
                    borderColor: '#e31837',
                    backgroundColor: 'rgba(227, 24, 55, 0.2)',
                    borderWidth: 3,
                    pointBackgroundColor: '#e31837',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#e31837'
                },
                {
                    label: 'Intel',
                    data: [24, 60, 40, 30, 75],
                    borderColor: '#0071c5',
                    backgroundColor: 'rgba(0, 113, 197, 0.2)',
                    borderWidth: 3,
                    pointBackgroundColor: '#0071c5',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#0071c5'
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Performance Comparison Score',
                    color: chartConfig.colors.text
                },
                legend: {
                    labels: {
                        color: chartConfig.colors.text
                    }
                }
            },
            scales: {
                r: {
                    angleLines: {
                        color: chartConfig.colors.grid
                    },
                    grid: {
                        color: chartConfig.colors.grid
                    },
                    pointLabels: {
                        color: chartConfig.colors.text
                    },
                    ticks: {
                        color: chartConfig.colors.text,
                        backdropColor: 'transparent'
                    },
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

// Export functions
window.chartUtils = {
    initializeAdvancedCharts,
    chartConfig
};
