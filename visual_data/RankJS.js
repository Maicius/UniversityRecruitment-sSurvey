/**
 * Created by maicius on 2017/11/27.
 */

//排行数据
let backColor = '#404a59';
$(document).ready(function () {
    let rank_it = echarts.init(document.getElementById("rank_it"));
    let rank_china = echarts.init(document.getElementById("rank_china"));
    let rank_world = echarts.init(document.getElementById("rank_world"));
    let rank_investment = echarts.init(document.getElementById("rank_investment"));
    let rank_private = echarts.init(document.getElementById("rank_private"));
    let rank_consulting = echarts.init(document.getElementById("rank_consulting"));
    let rank_service = echarts.init(document.getElementById("rank_service"));
    let rank_manufacture = echarts.init(document.getElementById("rank_manufacture"));
    let rank_usa = echarts.init(document.getElementById("rank_usa"));
    let rank_compre = echarts.init(document.getElementById("rank_compre"));
    let color1 = ['#CCFF99', '#66CCCC', '#339999', '#CCFFFF', '#66CC99', '#339999', '#66CC99', '#009999', '#336666', '#CCFF99', 'orange', '#CC9933', '#336666', '#CCCC99'];
    let color2 = ['#009999', '#CCFF99', '#CCFFFF', '#66CCCC', '#339999', '#336666', '#CCFF99', 'orange', '#CC9933', '#336666', '#CCCC99', '#66CC99', '#339999', '#66CC99'];
    let color3 = ['orange', '#339999', '#CCFFFF', '#66CC99', '#CCFF99', '#66CCCC', '#336666', '#CCFF99', '#339999', '#66CC99', '#009999', '#CC9933', '#336666', '#CCCC99'];
    let color4 = ['#66CCCC', '#336666', '#CCFF99', '#339999', '#66CC99', 'orange', '#339999', '#CCFFFF', '#66CC99', '#CCFF99', '#009999', '#CC9933', '#336666', '#CCCC99'];

    //console.log(China_it_top100_result);
    let China_it_top100_list = get_Rank_Data(China_it_top100_result);
    let World_top500_list = get_Rank_Data(world_top500_result);
    let China_top500_list = get_Rank_Data(China_top500_result);
    let usa_top500_list = get_Rank_Data(usa_top500_result);
    let China_manufacture_top500_list = get_Rank_Data(China_manufacture_top500_result);
    let China_service_top100_list = get_Rank_Data(China_service_top100_result);
    let China_private_top500_list = get_Rank_Data(China_private_top500_result);
    let world_investment_top100_list = get_Rank_Data(world_investment_top100_result);
    let world_consult_top75_list = get_Rank_Data(world_consult_top75_result);
    let compre_rank_list = [];

    drawRankChart(rank_it, China_it_top100_list, "中国互联网企业100强", color1);
    drawRankChart(rank_world, World_top500_list, "世界五百强", color2);
    drawRankChart(rank_china, China_top500_list, "中国五百强", color3);
    drawRankChart(rank_usa, usa_top500_list, "美国五百强", color4);
    drawRankChart(rank_manufacture, China_manufacture_top500_list, "中国制造业五百强", color2);
    drawRankChart(rank_service, China_service_top100_list, "中国服务业一百强", color3);
    drawRankChart(rank_private, China_private_top500_list, "中国私营企业五百强", color2);
    drawRankChart(rank_investment, world_investment_top100_list, "世界投资机构100强", color4);
    drawRankChart(rank_consulting, world_consult_top75_list, "世界咨询业75强", color3);

    for (let i = 0; i < 45; i++) {

        console.log(China_it_top100_result[i].data.length * 0.6 + (world_consult_top75_result[i].data.length + world_investment_top100_result[i].data.length) * 1.0);
        let compre_value = China_it_top100_result[i].data.length * 0.6 +
            (world_consult_top75_result[i].data.length + world_investment_top100_result[i].data.length) * 1.0 +
            (world_top500_result[i].data.length + usa_top500_result[i].data.length + China_top500_result[i].data.length) * 0.5 +
            (China_manufacture_top500_result[i].data.length + China_service_top100_result[i].data.length + China_private_top500_result[i].data.length) * 0.3;
        console.log(compre_value);
        compre_rank_list.push([China_it_top100_result[i].name, compre_value])
    }
    drawRankChart(rank_compre,compre_rank_list, "综合排名", color3);
});
function get_Rank_Data(raw_data) {
    let rank_data = [];
    console.log("raw_data");
    console.log(raw_data);
    for (let i = 0; i < raw_data.length; i++) {
        rank_data.push([raw_data[i].name, raw_data[i].data.length])
    }

    console.log(rank_data);
    return rank_data.sort(function (a, b) {
        return a[1] > b[1]
    });
}
function drawRankChart(domName, data, chartName, color) {
    let option = {
        title: {
            text: '2017年' + chartName + '到部分高校的招聘次数',
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

function convertJsonToArray(strData) {
    strData = JSON.parse(strData);
    let arr = [];
    for (let p in strData) {
        arr.push([p, strData[p]]);
    }
    return arr;
}