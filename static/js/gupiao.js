$(function () {
        var box=document.getElementById('box');
        var browser_wid=document.documentElement.clientWidth;
        box.style.cssText='width:'+browser_wid+'px;';
        var obj = new ScrollImg();
        obj.fetchImg();
        obj.scrollEvent();

    });
    function ScrollImg() {
        if (window.location.href=='http://127.0.0.1:8000/gupiao/'){
            this.url='/gupiao_ajax/';
        }else if (window.location.href=='http://127.0.0.1:8000/gupiao/gainian/'){
            this.url='/gupiao/gainian_ajax/';
        }else if (window.location.href=='http://127.0.0.1:8000/gupiao/getevery/'){
            this.url='/gupiao/getevery_ajax/';
        }
        this.NID = 0;
        this.nids=new Array();
        this.fetchImg = function () {
            var that = this;
            if (!that.nids.includes(that.NID)) {
                that.nids.push(that.NID);
                $.ajax({
                    url: that.url,
                    type: 'GET',
                    data: {nid: that.NID},
                    dataType: 'JSON',
                    success: function (arg) {
                        var img_list = arg.data;
                        $.each(img_list, function (key, value) {
                            var div = document.createElement('div');
                            var browser_wid = document.documentElement.clientWidth;
                            div.style.cssText = 'width:' + (browser_wid - 30) / 2 + 'px;height: 400px ;position: relative;display: inline-block ;float: left;margin-left: 10px;margin-top: 10px;background-color: gold ;padding: 10px;border: 1px solid #cccccc;box-shadow: 0 0 5px #cccccc;border-radius: 5px;';
                            div_id = "main_" + value.fid;
                            div.setAttribute("id", div_id);
                            click_url="'http://q.10jqka.com.cn/thshy/detail/code/"+value.code;
                            div.setAttribute("onclick", "window.open("+click_url+"')");
                            $('#box').append(div);
                            var titles=null;
                            if (value.industry != undefined){
                                titles=value.name+','+value.industry+','+value.area;
                            }else{
                                titles=value.name
                            }
                                drawkins(div_id,value,titles);
                            if (key + 1 == img_list.length) {
                                that.NID = value.fid;
                            }
                        })
                    }
                })
            }
        };
        this.scrollEvent = function () {
            var that = this;
            $(window).scroll(function () {
                var scrollTop = $(window).scrollTop();
                var winHeight = $(window).height();
                var docHeight = $(document).height();
                if ((scrollTop + winHeight) > (docHeight-20)) {
                    that.fetchImg();
                }
            })
        }
    }

function upload_method() {
    if (window.location.href=='http://127.0.0.1:8000/gupiao/' || window.location.href=='http://127.0.0.1:8000/gupiao/gainian/'){
        document.form1.action='/seach_byname/';
    }else if (window.location.href=='http://127.0.0.1:8000/gupiao/getevery/'){
        document.form1.action='/seach_bystockname/';
    }
}

function drawkins(div_id,value,titles) {
    var myChart = echarts.init(document.getElementById(div_id));
    var upColor = '#ec0000';
    var upBorderColor = '#8A0000';
    var downColor = '#00da3c';
    var downBorderColor = '#008F28';
    // 数据意义：开盘(open)，收盘(close)，最低(lowest)，最高(highest)
    var data0 = splitData(eval(value.data));

    function splitData(rawData) {
        var categoryData = [];
        var values = [];
        for (var i = 0; i < rawData.length; i++) {
            categoryData.push(rawData[i].splice(0, 1)[0]);
            values.push(rawData[i])
        }
        return {
            categoryData: categoryData,
            values: values
        };
    }

    function calculateMA(dayCount) {
        var result = [];
        for (var i = 0, len = data0.values.length; i < len; i++) {
            if (i < dayCount) {
                result.push('-');
                continue;
            }
            var sum = 0;
            for (var j = 0; j < dayCount; j++) {
                sum += data0.values[i - j][1];
            }
            result.push(sum / dayCount);
        }
        return result;
    }

    // 指定图表的配置项和数据
    var option = {
        title: {
            text: titles,
            left: 0
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            }
        },
        legend: {
            data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30']
        },
        grid: {
            left: '10%',
            right: '10%',
            bottom: '15%'
        },
        xAxis: {
            type: 'category',
            data: data0.categoryData,
            scale: true,
            boundaryGap: false,
            axisLine: {onZero: false},
            splitLine: {show: false},
            splitNumber: 20,
            min: 'dataMin',
            max: 'dataMax'
        },
        yAxis: {
            scale: true,
            splitArea: {
                show: true
            }
        },
        dataZoom: [
            {
                type: 'inside',
                start: 50,
                end: 100
            },
            {
                show: true,
                type: 'slider',
                top: '90%',
                start: 50,
                end: 100
            }
        ],
        series: [
            {
                name: '日K',
                type: 'candlestick',
                data: data0.values,
                itemStyle: {
                    color: upColor,
                    color0: downColor,
                    borderColor: upBorderColor,
                    borderColor0: downBorderColor
                },
                markPoint: {
                    label: {
                        normal: {
                            formatter: function (param) {
                                return param != null ? Math.round(param.value) : '';
                            }
                        }
                    },
                    data: [
                        {
                            name: 'XX标点',
                            coord: ['2013/5/31', 2300],
                            value: 2300,
                            itemStyle: {
                                color: 'rgb(41,60,85)'
                            }
                        },
                        {
                            name: 'highest value',
                            type: 'max',
                            valueDim: 'highest'
                        },
                        {
                            name: 'lowest value',
                            type: 'min',
                            valueDim: 'lowest'
                        },
                        {
                            name: 'average value on close',
                            type: 'average',
                            valueDim: 'close'
                        }
                    ],
                    tooltip: {
                        formatter: function (param) {
                            return param.name + '<br>' + (param.data.coord || '');
                        }
                    }
                },
                markLine: {
                    symbol: ['none', 'none'],
                    data: [
                        [
                            {
                                name: 'from lowest to highest',
                                type: 'min',
                                valueDim: 'lowest',
                                symbol: 'circle',
                                symbolSize: 10,
                                label: {
                                    show: false
                                },
                                emphasis: {
                                    label: {
                                        show: false
                                    }
                                }
                            },
                            {
                                type: 'max',
                                valueDim: 'highest',
                                symbol: 'circle',
                                symbolSize: 10,
                                label: {
                                    show: false
                                },
                                emphasis: {
                                    label: {
                                        show: false
                                    }
                                }
                            }
                        ],
                        {
                            name: 'min line on close',
                            type: 'min',
                            valueDim: 'close'
                        },
                        {
                            name: 'max line on close',
                            type: 'max',
                            valueDim: 'close'
                        }
                    ]
                }
            },
            {
                name: 'MA5',
                type: 'line',
                data: calculateMA(5),
                smooth: true,
                lineStyle: {
                    opacity: 0.5
                }
            },
            {
                name: 'MA10',
                type: 'line',
                data: calculateMA(10),
                smooth: true,
                lineStyle: {
                    opacity: 0.5
                }
            },
            {
                name: 'MA20',
                type: 'line',
                data: calculateMA(20),
                smooth: true,
                lineStyle: {
                    opacity: 0.5
                }
            },
            {
                name: 'MA30',
                type: 'line',
                data: calculateMA(30),
                smooth: true,
                lineStyle: {
                    opacity: 0.5
                }
            },

        ]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

