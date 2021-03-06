/**
 * Created by maicius on 2017/11/27.
 */

//排行数据
let backColor = '#404a59';

let color1 = ['#CCFF99', '#66CCCC', '#339999', '#CCFFFF', '#66CC99', '#339999', '#66CC99', '#009999', '#336666', '#CCFF99', 'orange', '#CC9933', '#336666', '#CCCC99'];
let color2 = ['#009999', '#CCFF99', '#CCFFFF', '#66CCCC', '#339999', '#336666', '#CCFF99', 'orange', '#CC9933', '#336666', '#CCCC99', '#66CC99', '#339999', '#66CC99'];
let color3 = ['orange', '#339999', '#CCFFFF', '#66CC99', '#CCFF99', '#66CCCC', '#336666', '#CCFF99', '#339999', '#66CC99', '#009999', '#CC9933', '#336666', '#CCCC99'];
let color4 = ['#66CCCC', '#336666', '#CCFF99', '#339999', '#66CC99', 'orange', '#339999', '#CCFFFF', '#66CC99', '#CCFF99', '#009999', '#CC9933', '#336666', '#CCCC99'];
let list_c9 = [];
let list_985 = [];
let list_211 = [];
let list_top = [];
let list_basic = [];
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
    let pie_c9 = echarts.init(document.getElementById("pie_c9"));
    let pie_985 = echarts.init(document.getElementById("pie_985"));
    let pie_211 = echarts.init(document.getElementById("pie_211"));
    let pie_top = echarts.init(document.getElementById("pie_top"));
    let pie_basic = echarts.init(document.getElementById("pie_basic"));
    let line_chart = echarts.init(document.getElementById("line_chart"));
    let China_map = echarts.init(document.getElementById("china_map"));

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
    console.log(China_it_top100_list);
    drawRankChart(rank_it, China_it_top100_list, "中国互联网企业一百强", color1);
    drawRankChart(rank_world, World_top500_list, "世界五百强", color2);
    drawRankChart(rank_china, China_top500_list, "中国五百强", color3);
    drawRankChart(rank_usa, usa_top500_list, "美国五百强", color4);
    drawRankChart(rank_manufacture, China_manufacture_top500_list, "中国民营企业制造业五百强", color2);
    drawRankChart(rank_service, China_service_top100_list, "中国民营企业服务业一百强", color3);
    drawRankChart(rank_private, China_private_top500_list, "中国民营企业五百强", color2);
    drawRankChart(rank_investment, world_investment_top100_list, "世界投行100强", color4);
    drawRankChart(rank_consulting, world_consult_top75_list, "世界咨询业75强", color3);
    draw_compre_and_ratio_rank();
    let big_result_list = [[China_it_top100_result, "中国互联网企业100强"], [world_top500_result, "世界五百强"],
        [China_private_top500_result, "中国民营企业500强"],
        [China_service_top100_result, "中国民营企业服务企业100强"], [China_top500_result, "中国五百强"],
        [China_manufacture_top500_result, "中国民营企业制造业500强"],
        [usa_top500_result, "美国五百强"], [world_investment_top100_result, "世界投资机构100强"], [world_consult_top75_result, "世界咨询业公司75强"]];
    $.each(big_result_list, function (index, value) {
        // console.log("value");
        // console.log(value);
        get_university_class_in_diff_company_list(value[0], value[1])
    });
    console.log(list_c9);
    console.log(list_211);
    draw_pie_chart(pie_c9, list_c9, "2017年C9高校平均\n校园招聘企业分布情况");
    draw_pie_chart(pie_985, list_985, "2017年985高校平均\n校园招聘企业分布情况");
    draw_pie_chart(pie_211, list_211, "2017年211高校平均\n校园招聘企业分布情况");
    draw_pie_chart(pie_top, list_top, "2017年一本高校平均\n校园招聘企业分布情况");
    draw_pie_chart(pie_basic, list_basic, "2017年二本高校平均\n校园招聘企业分布情况");
    draw_line_chart(line_chart, total_date_result, "2017年不同类别高校校园招聘会平均数量分布情况");

    let map_data = [];
    //画中国地图
    draw_china_map(China_map, '2017年全国企业校园招聘数量分布');

});

function get_Rank_Data(raw_data) {
    let rank_data = [];
    console.log("raw_data");

    for (let i = 0; i < raw_data.length; i++) {

        rank_data.push([raw_data[i].name[0], raw_data[i].data.length])
    }

    // chrome在这里的排序有问题，详情参考这篇博客:
    // console.log("https://www.cnblogs.com/yzeng/p/3949182.html?utm_source=tuicool&utm_medium=referral");
    for (var i = 0; i < rank_data.length; i++) {
        rank_data[i].oldIndex = i;
    }
    return rank_data.sort(function (a, b) {
        return a[1] - b[1] || a.oldIndex - b.oldIndex;
    });
}

function convertJsonToArray(strData) {
    strData = JSON.parse(strData);
    let arr = [];
    for (let p in strData) {
        arr.push([p, strData[p]]);
    }
    return arr;
}

// 画综合排名和比例排名
function draw_compre_and_ratio_rank() {
    let rank_compre = echarts.init(document.getElementById("rank_compre"));
    let rank_ratio = echarts.init(document.getElementById("rank_ratio"));
    let rank_total_num = echarts.init(document.getElementById("rank_total_num"));
    let total_company_list = [];
    let compre_rank_list = [];
    let ratio_company_list = [];
    for (let i = 0; i < China_it_top100_result.length; i++) {
        let compre_value, ratio_value = 0;
        if (China_it_top100_result[i].total_num === 0) {
            compre_value = 0;
            ratio_value = 0;
        }
        else {
            ratio_value = (China_it_top100_result[i].data.length * 1 +
                (world_consult_top75_result[i].data.length + world_investment_top100_result[i].data.length) * 1 +
                (world_top500_result[i].data.length + usa_top500_result[i].data.length + China_top500_result[i].data.length) * 1 +
                (China_manufacture_top500_result[i].data.length +
                    China_service_top100_result[i].data.length + China_private_top500_result[i].data.length) * 1) / (China_it_top100_result[i].total_num * 1);

            compre_value = (China_it_top100_result[i].data.length * 1 +
                (world_consult_top75_result[i].data.length + world_investment_top100_result[i].data.length) * 1 +
                (world_top500_result[i].data.length + usa_top500_result[i].data.length + China_top500_result[i].data.length) * 1 +
                (China_manufacture_top500_result[i].data.length +
                    China_service_top100_result[i].data.length + China_private_top500_result[i].data.length) * 1) + (China_it_top100_result[i].total_num * 1);
        }
        let name = China_it_top100_result[i].name;
        let university_name = name[0];
        //console.log(university_name);
        ratio_company_list.push([university_name, ratio_value.toFixed(2)]);
        compre_rank_list.push([university_name, compre_value]);
        total_company_list.push([university_name, China_it_top100_result[i].total_num]);
    }

    compre_rank_list = compre_rank_list.sort(function (a, b) {
        return parseFloat(a[1]) > parseFloat(b[1])
    });

    total_company_list = total_company_list.sort(function (a, b) {
        return a[1] > b[1]
    });

    ratio_company_list = ratio_company_list.sort(function (a, b) {
        return parseFloat(a[1]) > parseFloat(b[1])
    });

    console.log(compre_rank_list);
    drawRankChart(rank_ratio, ratio_company_list, "2017年来校招聘的知名公司占总公司数量的比例排名", get_random_color());
    drawRankChart(rank_compre, compre_rank_list, "2017年部分高校校园招聘综合排名", get_random_color());
    drawRankChart(rank_total_num, total_company_list, "2017年来校招聘的公司总数排名", get_random_color());
}

function get_university_class_in_diff_company_list(raw_data, name) {
    let count_c9 = 0;
    let count_985 = 0;
    let count_211 = 0;
    let count_top = 0;
    let count_basic = 0;
    let c9 = 0, p985 = 0, p211 = 0, pTop = 0, pBasic = 0;
    let total_num_c9 = 0, total_num_985 = 0, total_num_211 = 0, total_num_basic = 0, total_num_top = 0;
    console.log(name);
    console.log(raw_data);
    for (let i = 0; i < raw_data.length; i++) {
        if (raw_data[i].name[1] === 'C9') {
            count_c9 += raw_data[i].data.length;
            total_num_c9 += raw_data[i].total_num;
            c9 += 1;
        }
        else if (raw_data[i].name[1] === '985') {
            count_985 += raw_data[i].data.length;
            total_num_985 += raw_data[i].total_num;
            p985 += 1;
        }
        else if (raw_data[i].name[1] === '211') {
            count_211 += raw_data[i].data.length;
            total_num_211 += raw_data[i].total_num;
            p211 += 1;
        }
        else if (raw_data[i].name[1] === '一本') {
            count_top += raw_data[i].data.length;
            total_num_top += raw_data[i].total_num;
            pTop += 1;
        }
        else if (raw_data[i].name[1] === '二本') {
            count_basic += raw_data[i].data.length;
            total_num_basic += raw_data[i].total_num;
            pBasic += 1;
        }
    }
    let float_length = 2;
    // 保留小数点的长度
    // list_c9.push([name, (count_c9 / c9).toFixed(float_length), (total_num_c9 / c9).toFixed(float_length)]);
    // list_985.push([name, (count_985 / p985).toFixed(float_length), (total_num_985 / p985).toFixed(float_length)]);
    // list_211.push([name, (count_211 / p211).toFixed(float_length), (total_num_211 / p211).toFixed(float_length)]);
    // list_top.push([name, (count_top / pTop).toFixed(float_length), (total_num_top / pTop).toFixed(float_length)]);
    // list_basic.push([name, (count_basic / pBasic).toFixed(float_length), (total_num_basic / pBasic).toFixed(float_length)]);
    // console.log("c9:" + p985);
    list_c9.push({
        "name": name,
        "value": (count_c9 / c9).toFixed(float_length),
        "total_num": (total_num_c9 / c9).toFixed(float_length)
    });
    list_985.push({
        "name": name,
        "value": (count_985 / p985).toFixed(float_length),
        "total_num": (total_num_985 / p985).toFixed(float_length)
    });
    list_211.push({
        "name": name,
        "value": (count_211 / p211).toFixed(float_length),
        "total_num": (total_num_211 / p211).toFixed(float_length)
    });
    list_top.push({
        "name": name,
        "value": (count_top / pTop).toFixed(float_length),
        "total_num": (total_num_top / pTop).toFixed(float_length)
    });
    list_basic.push({
        "name": name,
        "value": (count_basic / pBasic).toFixed(float_length),
        "total_num": (total_num_basic / pBasic).toFixed(float_length)
    });
}

function get_random_color() {
    let color = ['#66CCCC', '#336666', '#CCFF99', '#339999', '#66CC99', 'orange', '#339999', '#CCFFFF', '#66CC99', '#CCFF99', '#009999', '#CC9933', '#336666', '#CCCC99'];
    let random_color = [];
    for (let i = 0; i < color.length; i++) {
        let index = (Math.random() * 14).toFixed(0);
        random_color.push(color[index]);
    }
    return random_color;
}

function get_random_color_red() {
    let color = ['#ffffcc', '#ccffff', '#ffcccc', '#ff6666', '#ff6666'];
    let random_color = [];
    for (let i = 0; i < color.length; i++) {
        let index = (Math.random() * 5).toFixed(0);
        random_color.push(color[index]);
    }
    return random_color;
}
