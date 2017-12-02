/**
 * Created by maicius on 2017/12/2.
 */
function draw_pie_chart(domName, data, chartName) {
    let scale = 1.3;
    let rich = {
        yellow: {
            color: "#ffc72b",
            fontSize: 16 * scale,
            padding: [5, 4],
            align: 'right'
        },
        total: {
            color: "#ffc72b",
            fontSize: 40 * scale,
            align: 'center'
        },
        white: {
            color: "#fff",
            align: 'left',
            fontSize: 14 * scale,
            padding: [21, 0]
        },
        blue: {
            color: '#49dff0',
            fontSize: 16 * scale,
            align: 'right'
        },
        hr: {
            borderColor: '#0b5',
            width: '100%',
            borderWidth: 1,
            height: 0,
        }
    };
    let option = {
        backgroundColor: backColor,
        title: {
            text: chartName,
            left: 'center',
            top: '53%',
            padding: [24, 0],
            textStyle: {
                color: '#fff',
                fontSize: 18 * scale,
                align: 'center'
            }
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        legend: {
            selectedMode: true,
            formatter: function (name) {
                let total = parseFloat(data[0].total_num);
                console.log("total");
                console.log(total);
                return '{total|' + total + '}';
            },
            data: [data[0].name],
            left: 'center',
            top: 'center',
            icon: 'none',
            align: 'center',
            textStyle: {
                color: "#0b5",
                fontSize: 16 * scale,
                rich: rich
            },
        },
        series: [{
            name: '公司总数',
            type: 'pie',
            radius: ['40%', '50%'],
            hoverAnimation: false,
            color: ['#c487ee', '#deb140', '#49dff0', '#034079', '#6f81da', '#00ffb4'],
            label: {
                normal: {
                    formatter: function (params, ticket, callback) {
                        let percent = (parseFloat(params.value) / parseFloat(params.data.total_num)).toFixed(4);
                        console.log(params);
                        console.log(params.data.total_num);
                        return '{white|' + params.name + '}:{yellow|' + parseFloat(params.value) + '} {blue|' + parseFloat(percent * 100).toFixed(2) + '%}\n';
                    },
                    rich: rich
                },
            },
            labelLine: {
                normal: {
                    length: 50 * scale,
                    length2: 0,
                    lineStyle: {
                        color: '#0b5'
                    }
                }
            },
            data: data
        }]
    };
    domName.setOption(option);
}

function drawRankChart(domName, data, chartName, color) {
    if (chartName !== "2017年来校招聘的知名公司占总公司数量的比例排名" && chartName !== '2017年来校招聘的公司总数排名') {
        chartName = '2017年' + chartName + '到部分高校的招聘次数'
    }
    let option = {
        title: {
            text: chartName,
            left: 'center',
            textStyle: {
                color: '#fff'
            }
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        backgroundColor: backColor,
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value',
            boundaryGap: [0, 0.01],
            axisLabel: {
                textStyle: {
                    color: '#999'
                }
            }
        },
        yAxis: {
            type: 'category',
            data: data.map(function (item) {
                return item[0];
            }),
            axisLabel: {
                textStyle: {
                    color: '#999'
                }
            },

        },
        series: [
            {
                name: chartName,
                type: 'bar',
                data: data.map(function (item) {
                    return item[1];
                }),
                label: {
                    normal: {
                        show: true,
                        position: 'right'
                    }
                },
                itemStyle: {
                    normal: {
                        // callback,设定每一bar颜色,配置项color顶axis一组bars颜色
                        color: function (params) {
                            var num = color.length;
                            return color[params.dataIndex % num]
                        }
                    }
                }
            }
        ]
    };
    domName.setOption(option);
}

function draw_line_chart(domName, data, chartName, color) {
    let option = {
        backgroundColor: '#394056',
        title: {
            text: '请求数',
            textStyle: {
                fontWeight: 'normal',
                fontSize: 16,
                color: '#F1F1F3'
            },
            left: '6%'
        },
        tooltip: {
            trigger: 'axis', //触发类型。[ default: 'item' ] :数据项图形触发，主要在散点图，饼图等无类目轴的图表中使用;'axis'坐标轴触发，主要在柱状图，折线图等会使用类目轴的图表中使用
            axisPointer: {
                lineStyle: {
                    color: '#57617B'
                }
            }
        },
        legend: {
            icon: 'rect', //设置图例的图形形状，circle为圆，rect为矩形
            itemWidth: 14, //图例标记的图形宽度[ default: 25 ]
            itemHeight: 5, //图例标记的图形高度。[ default: 14 ]
            itemGap: 13, //图例每项之间的间隔。横向布局时为水平间隔，纵向布局时为纵向间隔。[ default: 10 ]
            data: ['移动', '电信', '联通'],
            right: '4%', //图例组件离容器右侧的距离
            textStyle: {
                fontSize: 12,
                color: '#F1F1F3'
            }
        },
        grid: {
            left: '3%', //grid 组件离容器左侧的距离。
            right: '4%', //grid 组件离容器右侧的距离。
            bottom: '3%', //grid 组件离容器下侧的距离。
            containLabel: true //grid 区域是否包含坐标轴的刻度标签[ default: false ]
        },
        xAxis: [{
            type: 'category',
            boundaryGap: false, //坐标轴两边留白策略，类目轴和非类目轴的设置和表现不一样
            axisLine: {
                lineStyle: {
                    color: '#57617B' //坐标轴线线的颜色。
                }
            },
            data: ['13:00', '13:05', '13:10', '13:15', '13:20', '13:25', '13:30', '13:35', '13:40', '13:45', '13:50', '13:55']
        }],
        yAxis: [{
            type: 'value', //坐标轴类型。'value' 数值轴，适用于连续数据;'category' 类目轴，适用于离散的类目数据，为该类型时必须通过 data 设置类目数据;'time' 时间轴;'log' 对数轴.
            name: '单位（%）', //坐标轴名称。
            axisTick: {
                show: false //是否显示坐标轴刻度
            },
            axisLine: {
                lineStyle: {
                    color: '#57617B' //坐标轴线线的颜色
                }
            },
            axisLabel: {
                margin: 10, //刻度标签与轴线之间的距离
                textStyle: {
                    fontSize: 14 //文字的字体大小
                }
            },
            splitLine: {
                lineStyle: {
                    color: '#57617B' //分隔线颜色设置
                }
            }
        }],
        series: [{
            name: '移动', //系列名称，用于tooltip的显示，legend 的图例筛选，在 setOption 更新数据和配置项时用于指定对应的系列
            type: 'line',
            smooth: true, //是否平滑曲线显示
            symbol: 'circle', //标记的图形。ECharts 提供的标记类型包括 'circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow'
            symbolSize: 5, //标记的大小，可以设置成诸如 10 这样单一的数字，也可以用数组分开表示宽和高，例如 [20, 10] 表示标记宽为20，高为10[ default: 4 ]
            showSymbol: false, //是否显示 symbol, 如果 false 则只有在 tooltip hover 的时候显示
            lineStyle: { //线条样式
                normal: {
                    width: 1 //线宽。[ default: 2 ]
                }
            },
            areaStyle: { //区域填充样式
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ //填充的颜色。
                        offset: 0, // 0% 处的颜色
                        color: 'rgba(137, 189, 27, 0.3)'
                    }, {
                        offset: 0.8, // 80% 处的颜色
                        color: 'rgba(137, 189, 27, 0)'
                    }], false),
                    shadowColor: 'rgba(0, 0, 0, 0.1)', //阴影颜色。支持的格式同color
                    shadowBlur: 10 //图形阴影的模糊大小。该属性配合 shadowColor,shadowOffsetX, shadowOffsetY 一起设置图形的阴影效果
                }
            },
            itemStyle: { //折线拐点标志的样式
                normal: {
                    color: 'rgb(137,189,27)',
                    borderColor: 'rgba(137,189,2,0.27)', //图形的描边颜色。支持的格式同 color
                    borderWidth: 12 //描边线宽。为 0 时无描边。[ default: 0 ]

                }
            },
            data: [220, 182, 191, 134, 150, 120, 110, 125, 145, 122, 165, 122]
        }, {
            name: '电信',
            type: 'line',
            smooth: true,
            symbol: 'circle',
            symbolSize: 5,
            showSymbol: false,
            lineStyle: {
                normal: {
                    width: 1
                }
            },
            areaStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: 'rgba(0, 136, 212, 0.3)'
                    }, {
                        offset: 0.8,
                        color: 'rgba(0, 136, 212, 0)'
                    }], false),
                    shadowColor: 'rgba(0, 0, 0, 0.1)',
                    shadowBlur: 10
                }
            },
            itemStyle: {
                normal: {
                    color: 'rgb(0,136,212)',
                    borderColor: 'rgba(0,136,212,0.2)',
                    borderWidth: 12

                }
            },
            data: [120, 110, 125, 145, 122, 165, 122, 220, 182, 191, 134, 150]
        }, {
            name: '联通',
            type: 'line',
            smooth: true,
            symbol: 'circle',
            symbolSize: 5,
            showSymbol: false,
            lineStyle: {
                normal: {
                    width: 1
                }
            },
            areaStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: 'rgba(219, 50, 51, 0.3)'
                    }, {
                        offset: 0.8,
                        color: 'rgba(219, 50, 51, 0)'
                    }], false),
                    shadowColor: 'rgba(0, 0, 0, 0.1)',
                    shadowBlur: 10
                }
            },
            itemStyle: {
                normal: {

                    color: 'rgb(219,50,51)',
                    borderColor: 'rgba(219,50,51,0.2)',
                    borderWidth: 12
                }
            },
            data: [220, 182, 125, 145, 122, 191, 134, 150, 120, 110, 165, 122]
        },]
    };
    domName.setOption(option)
}