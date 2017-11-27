
/**
 * Created by maicius on 2017/11/27.
 */

//排行数据
let backColor = '#404a59';
$(document).ready(function () {
    console.log("enter");
    console.log(China_it_top100)
});
function drawRankChart(domName, data, chartName, color) {
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
                        position: 'inside'
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

function convertJsonToArray(strData) {
    strData = JSON.parse(strData);
    let arr=[];
    for(let p in strData){
        arr.push([p, strData[p]]);
    }
    return arr;
}