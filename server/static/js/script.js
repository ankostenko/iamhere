window.onload = function () {
    'use strict'
    var width = 5000,
        height = 5000,
        fill = "rgba(255, 5, 5, 0.888)",
        stroke = "rgba(0, 0, 0, 0.5)",
        strokeWidth = 0.1;
    var svg = d3.select("#canvas").append("svg")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr('id', 'map')
        .attr("preserveAspectRatio", "xMidYMid meet")
        .attr("xmlns", "http://www.w3.org/2000/svg");
    let mapMode = 1;
    /*
     * 1 - Положение на карте
     * 2 - Маршрут
     * 3 - Метка
     */

    let userMenuItems = document.getElementsByClassName('circle-menu');
    var url_string = window.location.href;
    var url = new URL(url_string);
    let placeLink = document.getElementById('place-link');
    let placeLinkNone = document.getElementById('place-link__none');
    var floor = url.searchParams.get("f");
    var x1 = url.searchParams.get("x")
    var y1 = url.searchParams.get("y")
    if (floor == null) {
        floor = document.getElementsByClassName('circle')[0].dataset.stageId;
    }

    /* 
     * Функция переключения кружков
     */
    [].forEach.call(userMenuItems, function (elem) {
        elem.addEventListener('click', function (e) {
            if (e.srcElement.dataset.mapMode !== mapMode) {
                document.getElementsByClassName('select-circle-menu')[0].classList.remove('select-circle-menu');
                e.srcElement.parentElement.parentElement.classList.add('select-circle-menu');
                mapMode = Number(e.srcElement.dataset.mapMode);
            }
        })
    });
    var scaleVar = 1;
    var translateVar = [0, 0];
    var g = svg.append("g");


    /*
     * Здесь надо получить данные из ссылки 
     */

    if (floor == null) {
        floor = document.getElementsByClassName('circle')[0].dataset.stageId;
    }

    if (x1 == null) {
        x1 = -10000;
    }

    if (y1 == null) {
        y1 = -10000;
    }
    let imageId;


    document.getElementsByClassName('circle-' + floor)[0].classList.add('select-circle');
    var Request = new XMLHttpRequest();
    Request.open('GET', '/api/v1/stage/' + floor, true);
    Request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    Request.addEventListener("readystatechange", () => {


    var Request2 = new XMLHttpRequest();
    Request2.open('GET', '/api/v1/tag', true);
    Request2.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    Request2.addEventListener("readystatechange", () => {
        if (Request.readyState === 4 && Request.status === 200) {
            let obj = JSON.parse(Request.response)

            let obj2 = JSON.parse(Request2.response)
            let tags = [], stagesId = []
            for (var i = 0; i < obj2.counters.length; i++) {
                tags[i] = obj2[i];
                stagesId[i] = obj2.file_type[i]
            }
           
            imageId = obj['image_id'];
            var imageRequest = new XMLHttpRequest();
            imageRequest.open('GET', '/api/v1/image/' + imageId, true);
            imageRequest.setRequestHeader('Content-type', 'application/json; charset=utf-8');
            imageRequest.addEventListener('readystatechange', () => {
                if (imageRequest.readyState === 4 && imageRequest.status === 200) {
                    let img = imageRequest.response.substr(1, imageRequest.response.length - 3);
                    var imageCheckSize = new Image();
                    imageCheckSize.onload = function () {
                        svg.attr('viewBox', '0 0 ' + imageCheckSize.width + ' ' + imageCheckSize.height);
                    }
                    imageCheckSize.src = '../../files/' + img;
                    let map = g.append("svg:image")
                        .attr('x', 0)
                        .attr('y', 0)
                        .attr("xlink:href", '../../files/' + img)
                        .attr("data-image-id", +imageId)
                        .attr('id', 'map-image');

                    map.data(stagesId)
                    .enter()
                    .append("svg:image")
                    .attr("xlink:href", () =>{
                        
                    })
                    .attr("class", "tags")
                    .attr("id", "cent")
                    .attr("width", "80px")
                    .attr("stroke", stroke)
                    .attr("stroke-width", strokeWidth)
                    .attr("x", function (d) {
                        return 
                    })
                    .attr("y", function (d) {
                        return d[1];
                    });

                    svg.call(d3.zoom().on("zoom", () => {
                        let t = d3.event.transform;
                        if (t.k >= 0.5) {
                            g.attr("transform", t);
                            translateVar[0] = t.x;
                            translateVar[1] = t.y;
                            scaleVar = t.k;
                        } else {
                            t.k = 0.5;
                            t.x = translateVar[0];
                            t.y = translateVar[1];
                            g.attr("transform", t);
                            translateVar[0] = t.x;
                            translateVar[1] = t.y;
                        }
                    }));

                    let resize = () => {
                        svg.attr('width', "100%")
                            .attr('height', "100%")
                    };
                    resize();

                    d3.select(window).on('resize', resize);
                    g.selectAll(".here-circle").data([
                            [x1, y1]
                        ])
                        .enter()
                        .append("svg:image")
                        .attr("xlink:href", "https://psv4.userapi.com/c856220/u223208300/docs/d13/0c10d9df03ee/placeholder_1.svg?extra=G_8SkZskxMPuibJDBp3vpxIeEcWpmGz2wQ3Wqx41hQAJc9YNK5DI8HH_bTPwPpKVZFGXRLv-Cn12G--hGZFkZDEX8WjHandlF8055L0Y5_SFE1LP7JI5BqKZfbzuG-aulk41LqMwCVzV1gdsvx9q1Jr3AQ&dl=1")
                        .attr("class", "here-circle")
                        .attr("id", "cent")
                        .attr("width", "120px")
                        .attr("stroke", stroke)
                        .attr("stroke-width", strokeWidth)
                        .attr("x", function (d) {
                            return d[0];
                        })
                        .attr("y", function (d) {
                            return d[1];
                        });
                    g.selectAll(".hence-circle").data([
                            [x1, y1]
                        ])
                        .enter()
                        .append("svg:image")
                        .attr("xlink:href", "https://psv4.userapi.com/c856236/u223208300/docs/d17/940fe658c332/placeholder.svg?extra=U7pyHY43wpEQrZWBWRHAu8a-K5DkB8Bf10z1PqAyBnZIZ5v2CvnGrpbUkc66irDwz68f__EkIIyXsJuIbzJHKC_itwufEAtceJkMGstgBc_s1GzRWspdydl-eqWjcfTRd4CFdqLNcTUTJnmKHz_rv6922g&dl=1")
                        .attr("class", "hence-circle")
                        .attr("id", "cent")
                        .attr("width", "120px")
                        .attr("stroke", stroke)
                        .attr("stroke-width", strokeWidth)
                        .attr("x", function (d) {
                            return d[0];
                        })
                        .attr("y", function (d) {
                            return d[1];
                        });
                }
            });
            imageRequest.send(imageId);
        }
    });
    Request.send(floor);


    function changexlinkhref(floor) {
        var Request = new XMLHttpRequest();
        Request.open('GET', '/api/v1/stage/' + floor, true);
        Request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
        Request.addEventListener("readystatechange", () => {
            if (Request.readyState === 4 && Request.status === 200) {
                let obj = JSON.parse(Request.response);
                let imageId = obj['image_id'];
                var imageRequest = new XMLHttpRequest();
                imageRequest.open('GET', '/api/v1/image/' + imageId, true);
                imageRequest.setRequestHeader('Content-type', 'application/json; charset=utf-8');
                imageRequest.addEventListener('readystatechange', () => {
                    if (imageRequest.readyState === 4 && imageRequest.status === 200) {
                        let img = imageRequest.response.substr(1, imageRequest.response.length - 3);
                        document.querySelector("svg image").setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', '../../files/' + img);
                        document.querySelector("svg image").setAttribute('data-image-id', +imageId);
                        var imageCheckSize = new Image();
                        imageCheckSize.onload = function () {
                            svg.attr('viewBox', '0 0 ' + imageCheckSize.width + ' ' + imageCheckSize.height);
                        }
                        imageCheckSize.src = '../../files/' + img;
                    }
                });
                imageRequest.send(floor);
            }
        });
        Request.send(floor);
    }



    svg.on("click", function () {
        if (mapMode === 1) { // СЮДА ФИГАЧИМ ОБРАБОТКУ КЛИКА С ВКЛЮЧЕННОЙ ФУНКЦИЕЙ "Я ЗДЕСЬ!"

            var coords = d3.mouse(svg.node());
            x1 = Math.round(coords[0]);
            y1 = Math.round(coords[1]);
            g.selectAll(".here-circle")
                .attr('x', Math.round((x1 - translateVar[0]) / scaleVar) - 53)
                .attr('y', Math.round((y1 - translateVar[1]) / scaleVar) - 90);
            window.history.pushState('', '', `?f=${floor}&x=${Math.round(x1)}&y=${Math.round(y1)}`);


        } else if (mapMode === 2) {
            var coords = d3.mouse(svg.node());
            var x = Math.round(coords[0]);
            var y = Math.round(coords[1]);
            let obj = {
                "start_row": Math.round((+y1 - translateVar[1]) / scaleVar),
                "start_col": Math.round((+x1 - translateVar[0]) / scaleVar),
                "end_row": Math.round((y - translateVar[1]) / scaleVar),
                "end_col": Math.round((x - translateVar[0]) / scaleVar)
            }
            let jsonObj = JSON.stringify(obj);
            g.selectAll(".hence-circle")
                .attr('x', Math.round((x - translateVar[0]) / scaleVar) - 53)
                .attr('y', Math.round((y - translateVar[1]) / scaleVar) - 90);
            var routeRequest = new XMLHttpRequest();
            routeRequest.open('POST', '/api/v1/way/' + imageId, true);
            routeRequest.setRequestHeader('Content-type', 'application/json; charset=utf-8');
            routeRequest.addEventListener('readystatechange', () => {
                if (routeRequest.readyState === 4 && routeRequest.status === 200) {
                    let dataJson = routeRequest.response;
                    let lineData = JSON.parse(dataJson);
                    d3.select('.myline').remove()
                    let line = d3.line()
                        .x(function (d) {
                            return Math.round((d[1] * scaleVar - translateVar[0]))
                        })
                        .y(function (d) {
                            return Math.round((d[0] * scaleVar - translateVar[1]))
                        })

                    g.append('path')
                        .attr('class', 'line')
                        .attr('d', line(lineData))
                        .attr('stroke-width', 10)
                        .attr('stroke', 'red')
                        .attr('fill', 'none')
                        .attr('class', 'myline')
                }
            });
            routeRequest.send(jsonObj);
            //lineData = data;


            //А СЮДА ОБРАБОТКУ КЛИКА С ВКЛЮЧЕННОЙ ФУНКЦИЕЙ ПОСТРОЕНИЯ МАРШРУТА
        } else if (mapMode === 3) {

            //НУ А ЗДЕСЬ БУДЕТ КРАСОВАТЬСЯ ОБРАБОТКА КЛИКА МЕТКИ
        }
    });

    let saveButton = document.getElementById('save-map');
    saveButton.addEventListener("click", function () {
        saveSvgAsPng(document.getElementById("map"), "map.png");
    });

    var changeFloor = function (d) {
        floor = d.currentTarget.dataset.stageId;
        let selectCircle = document.getElementsByClassName('select-circle');
        if (selectCircle.length) {
            selectCircle[0].classList.remove('select-circle');
        }
        d.srcElement.classList.add('select-circle');
        scaleVar = 1;
        translateVar = [0, 0];
        g.attr("transform", "translate(0, 0)scale(1)");
        changexlinkhref(floor);
    };

    placeLink.addEventListener('click', function (e) {
        // ОБРАБОТКА КЛИКА ПО ИНПУТУ С ССЫЛКОЙ
    })
    var elems = document.querySelectorAll(".circle");
    for (var i = 0, len = elems.length; i < len; i++) elems[i].onclick = changeFloor;
    d3.select(self.frameElement).style("height", height + "px");
}