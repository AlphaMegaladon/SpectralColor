    var ctx = document.getElementById("myChart").getContext("2d");
    var myChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: {{ labels | safe }},
            datasets: [
                {
                    label: "Data points",
                    data: {{ values | safe }},
                    backgroundColor: "rgb(0,255,0)",
                    borderColor: "rgb(255,0,0)",
                    // borderWidth: 2,
                    tension: 0.5
                }
            ]
        },
        options: {
            plugins: {
            dragData: {
                round: 2, // rounds the values to n decimal places 
                        // in this case 1, e.g 0.1234 => 0.1)
                showTooltip: true, // show the tooltip while dragging [default = true]
                // dragX: true // also enable dragging along the x-axis.
                            // this solely works for continous, numerical x-axis scales (no categories or dates)!
                onDragStart: function(e, element) {
                    //startingValue = myChart.data.datasets[element._datasetIndex].data[element._index]
                /*
                // e = event, element = datapoint that was dragged
                // you may use this callback to prohibit dragging certain datapoints
                // by returning false in this callback
                if (element.datasetIndex === 0 && element.index === 0) {
                    // this would prohibit dragging the first datapoint in the first
                    // dataset entirely
                    return false
                }
                */
                },
                onDrag: function(e, datasetIndex, index, value) {
                    let startValueLeft2 = myChart.data.datasets[datasetIndex].data[index-2];
                    let startValueLeft = myChart.data.datasets[datasetIndex].data[index-1];
                    let startValue = myChart.data.datasets[datasetIndex].data[index];
                    let startValueRight = myChart.data.datasets[datasetIndex].data[index+1];
                    let startValueRight2 = myChart.data.datasets[datasetIndex].data[index+2];
                    let delta = (value - startValue);
                    if (value < 0) {
                        return false
                    }
                    else if (value > 1) {
                        return false
                    }
                   
                    if (index === 0) {
                        if (delta*(startValueRight-value) < 0) {
                            myChart.data.datasets[datasetIndex].data[index + 1] = startValueRight + delta/2;
                            if (delta*(startValueRight2-startVlaueRight) < 0) {
                                myChart.data.datasets[datasetIndex].data[index + 2] = startValueRight2 + delta/4;
                            }
                        }
                    } else if (index === (myChart.data.datasets[datasetIndex].data.length - 1)) {
                        if (delta*(startValueLeft-value) < 0) {
                            myChart.data.datasets[datasetIndex].data[index - 1] = startValueLeft + delta/2;
                            if (delta*(startValueLeft2-StartValueLeft) < 0) {
                                myChart.data.datasets[datasetIndex].data[index - 2] = startValueLeft2 + delta/4;
                            }
                        }
                    } else {
                        if (delta*(startValueLeft-value) < 0) {
                            myChart.data.datasets[datasetIndex].data[index - 1] = startValueLeft + delta/2;
                            if (delta*(startValueLeft2-startValueLeft) < 0) {
                                myChart.data.datasets[datasetIndex].data[index - 2] = startValueLeft2 + delta/4;
                            }
                        }
                        if (delta*(startValueRight-value) < 0) {
                            myChart.data.datasets[datasetIndex].data[index + 1] = startValueRight + delta/2;
                            if (delta*(startValueRight2-startValueRight) < 0) {
                                myChart.data.datasets[datasetIndex].data[index + 2] = startValueRight2 + delta/4;
                            }
                        }
                    }
                    myChart.update()     
                /*     
                // you may control the range in which datapoints are allowed to be
                // dragged by returning `false` in this callback
                if (value < 0) return false // this only allows positive values
                if (datasetIndex === 0 && index === 0 && value > 20) return false 
                */
                },
                onDragEnd: function(e, datasetIndex, index, value) {
                // you may use this callback to store the final datapoint value
                // (after dragging) in a database, or update other UI elements that
                // dependent on it
                console.log(myChart.data.datasets[datasetIndex].data)
                
                },
            }
            },
        },
        scales: {
            yAxes: {
                max: 1.01,
                min: 0
            }
        }
    });