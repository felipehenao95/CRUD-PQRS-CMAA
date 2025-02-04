// graficos.js

document.addEventListener('DOMContentLoaded', function() {
    // Datos recibidos desde Django
    var datos1 = data_json1;
    var datos2 = data_json2;
    var datos3 = data_json3;
    var datos4 = data_json4;
    var datos5 = data_json5;
    var datos6 = data_json6;

    // CONFIGURACION GRAFICO 1
    datos1.forEach(function(item) {
        item.fecha = new Date(item.fecha);
    });
    var seriesData1 = datos1.map(function(item) {
        return [item.fecha, item.cantidad];
    });

    var chart1 = echarts.init(document.getElementById('chart1'));
    var option1 = {
        title: { text: 'PQRS RECIBIDAS',
            subtext: 'Cantidad de PQRS recibidas por día'
         },
        tooltip: {
            trigger: 'axis',
            formatter: function(params) {
                params = params[0];
                var date = new Date(params.value[0]);
                var formattedDate = date.getFullYear() + '/' + 
                                    (date.getMonth() + 1).toString().padStart(2, '0') + '/' + 
                                    date.getDate().toString().padStart(2, '0');
                return formattedDate + ' : ' + params.value[1];
            },
            axisPointer: { animation: false }
        },
        toolbox: {
            show: true,
            feature: {
              saveAsImage: {}
            },
            left: 'left',    // Posiciona el toolbox a la izquierda
            bottom: '0%',
        },
        dataZoom: {show:true},
        xAxis: { type: 'time', boundaryGap: false },
        yAxis: { type: 'value', boundaryGap: [0, '100%'] },
        series: [{
            name: 'Cantidad',
            type: 'line',
            showSymbol: false,
            smooth: true,
            hoverAnimation: false,
            areaStyle: {},
            data: seriesData1,
            lineStyle: {
                width: 3,
                shadowColor: 'rgba(0,0,0,0.3)',
                shadowBlur: 10,
                shadowOffsetY: 8
              },
        }]
    };
    chart1.setOption(option1);

    // CONFIGURACION GRAFICO 2
    var seriesData2 = datos2.map(function(item) {
        return item.cantidad;
    });
    var categories2 = datos2.map(function(item) {
        return item.mes;
    });

    var chart2 = echarts.init(document.getElementById('chart2'));
    var option2 = {
        title: { text: 'CONSOLIDADO MENSUAL DE PQRS',
            subtext: 'Cantidad de PQRS recibidas por mes'
         },
        tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'shadow' },
            formatter: function(params) {
                var formattedDate = params[0].name;
                return formattedDate + ' : ' + params[0].value;
            }
        },
        toolbox: {
            show: true,
            feature: {
              saveAsImage: {}
            },
            left: 'left',    // Posiciona el toolbox a la izquierda
            bottom: '0%',
        },
        xAxis: { type: 'category', data: categories2,
            axisTick: {
                show: false
              },
            axisLine: {
                show: true
              },
         },
        yAxis: { type: 'value', axisLabel: {color: '#999'} },
        dataZoom: {show:true},
        series: [{
            name: 'Cantidad',
            type: 'bar',
            showBackground: true,
            data: seriesData2,
            label: {
                show: true,  // Muestra el label de cada sección
            },
            itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#83bff6' },
                  { offset: 0.5, color: '#188df0' },
                  { offset: 1, color: '#188df0' }
                ])},
            emphasis: {
                itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#2378f7' },
                    { offset: 0.7, color: '#2378f7' },
                    { offset: 1, color: '#83bff6' }
                    ])}},
        }]
    };
    chart2.setOption(option2);

    // CONFIGURACION GRAFICO 3 (Distribución por Localidad)
    var seriesData3 = datos3.map(function(item) {
        return { name: item.localidad, value: item.cantidad };
    });

    var chart3 = echarts.init(document.getElementById('chart3'));
    var option3 = {
        title: { text: 'AGRUPACIÓN POR LOCALIDAD',
            subtext: 'Distribución de PQRS por Localidad'
         },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        toolbox: {
            show: true,
            feature: {
              saveAsImage: {}
            },
            left: 'left',    // Posiciona el toolbox a la izquierda
            bottom: '0%',
        },
        legend: {
            orient: 'vertical',
            left: 'right'
          },
        series: [{
            name: 'Localidad',
            type: 'pie',
            radius: '55%',
            center: ['50%', '50%'],
            data: seriesData3,
            label: {
                show: true,  // Muestra el label de cada sección
                formatter: '{b}: {d}%'  // Formato del label: nombre y porcentaje
            },
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    };
    chart3.setOption(option3);

    // CONFIGURACION GRAFICO 4 (Distribución por Tipo DP)
    var seriesData4 = datos4.map(function(item) {
        return { name: item.tipo_dp, value: item.cantidad };
    });

    var chart4 = echarts.init(document.getElementById('chart4'));
    var option4 = {
        title: { text: 'AGRUPACIÓN POR TIPO',
            subtext: 'Distribución de PQRS por Tipo'
         },
        toolbox: {
            show: true,
            feature: {
              saveAsImage: {}
            },
            left: 'left',    // Posiciona el toolbox a la izquierda
            bottom: '0%',
        },
        dataZoom: {show:true},
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
            orient: 'horizontal',
            left: 'right'
          },
        series: [{
            name: 'Tipo DP',
            type: 'pie',
            radius: '55%',
            center: ['50%', '50%'],
            data: seriesData4,
            label: {
                show: true,  // Muestra el label de cada sección
                formatter: '{b}: {d}%'  // Formato del label: nombre y porcentaje
            },
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    };
    chart4.setOption(option4);

    // CONFIGURACION GRAFICO 5 (Distribución por Tema DP)
    var seriesData5 = datos5.map(function(item) {
        return { name: item.tema_dp, value: item.cantidad };
    });

    var chart5 = echarts.init(document.getElementById('chart5'));
    var option5 = {
        title: { text: 'AGRUPACIÓN POR TEMA',
            subtext: 'Distribución de PQRS por Tematica'
         },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        toolbox: {
            show: true,
            feature: {
              saveAsImage: {}
            },
            left: 'left',    // Posiciona el toolbox a la izquierda
            bottom: '0%',
        },
        legend: {
            orient: 'vertical',
            type: 'scroll',
            right: 10,
            top: 10,
            bottom: 10,
        },
        series: [{
            name: 'Tema DP',
            type: 'pie',
            radius: '55%',
            center: ['50%', '50%'],
            data: seriesData5,
            label: {
                show: true,  // Muestra el label de cada sección
                formatter: '{d}%'  // Formato del label: nombre y porcentaje
            },
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    };
    chart5.setOption(option5);

    // CONFIGURACION GRAFICO 6 (Distribución por Barrio)
    var seriesData6 = datos6.map(function(item) {
        return { name: item.barrio, value: item.cantidad };
    });

    // Ordena los datos por valor descendente
    seriesData6.sort(function(a, b) {
        return b.value - a.value;
    });

    var chart6 = echarts.init(document.getElementById('chart6'));
    var option6 = {
        title: { text: 'AGRUPACIÓN POR BARRIO',
            subtext: 'Distribución de PQRS por Barrio'
         },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        toolbox: {
            show: true,
            feature: {
              saveAsImage: {}
            },
            left: 'left',    // Posiciona el toolbox a la izquierda
            bottom: '0%',
        },
        legend: {
            orient: 'vertical',
            type: 'scroll',
            right: 10,
            top: 10,
            bottom: 10,
          },
        series: [{
            name: 'Barrio',
            type: 'pie',
            radius: '55%',
            center: ['50%', '50%'],
            data: seriesData6,
            //label: {show: false},
            label: {
                show: true,
                formatter: function(params) {
                    // Solo muestra etiquetas para los primeros 4 valores más altos
                    var index = seriesData6.findIndex(item => item.name === params.name);
                    return index < 8 ? `${params.percent.toFixed(2)}%` : '';
                }
            },
            emphasis: {
                itemStyle: {
                    borderRadius: 5,
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    };
    chart6.setOption(option6);

    // Ajustar el tamaño de los gráficos según el contenedor
    window.onresize = function() {
        chart1.resize();
        chart2.resize();
        chart3.resize();
        chart4.resize();
        chart5.resize();
        chart6.resize();
    };
});