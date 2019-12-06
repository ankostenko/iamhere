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
        .attr("preserveAspectRatio", "xMidYMid meet");
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
    destinationCoordinate[0] = url.searchParams.get("x")
    destinationCoordinate[1] = url.searchParams.get("y")
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
    let myCoordinate = [0, 0];
    let destinationCoordinate= [0, 0];

    /*
     * Здесь надо получить данные из ссылки 
     */

    if (floor == null) {
        floor = document.getElementsByClassName('circle')[0].dataset.stageId;
    }

    if (destinationCoordinate[0] == null) {
        x = -10000
    }

    if (destinationCoordinate[1] == null) {
        y = -10000
    }

    

    document.getElementsByClassName('circle-' + floor)[0].classList.add('select-circle');
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

                        svg.selectAll('circle')
                        .attr('cx', function (d) {
                                return x(d.x + translateVar[0]) 

                            })
                            .attr('cy', function (d) {
                                return x(d.x + translateVar[1]) 
                            })
                    }));

                    let resize = () => {
                        svg.attr('width', "100%")
                            .attr('height', "100%")
<<<<<<< HEAD
=======
                        var circles = svg.selectAll('circle')

                        circles.attr('cx', function (d, i) {
                                return console.log(d.cx);

                            })
                            .attr('cy', function (d, i) {
                                return
                            })
>>>>>>> 20a7cf29ff6482852a81237430806d4033081101
                    };
                    resize();
                    d3.select(window).on('resize', resize);
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
            //+ `?f=${floor}&x=${myCoordinate[0]}&y=${myCoordinate[1]}`
            //.append("svg:svg")
            //.attr("xlink:href", "../../static/images/placeholder.svg")
            var events = [];
            g.on('click', function () {
                events.push(d3.event);
                if (events.length > 1) events.shift();
                var circles = svg.selectAll('circle')
                    .data(events, function (e) {
                        return e.timeStamp
                    })
                    .attr('fill', 'gray');
                circles
                    .enter()
                    .append('circle')
                    .attr('cx', function (d) {
                        myCoordinate[0] = d3.mouse(svg.node())[0]
                        return myCoordinate[0]
                    })
                    .attr('cy', function (d) {
                        myCoordinate[1] = d3.mouse(svg.node())[1]
                        return myCoordinate[1]
                    })
                    .attr('fill', 'red')
                    .attr('r', 10);
                circles
                    .exit()
                    .remove();
                window.history.pushState('','',`?f=${floor}&x=${Math.round(myCoordinate[0])}&y=${Math.round(myCoordinate[0])}`);
            });



            svg.selectAll("rect")
                .data(zones)
                .enter()
                .append("rect")
                .attr("id", function (d) {
                    return "zone" + d.zone;
                })
                .attr("class", "zone")
                .attr("x", function (d, i) {
                    if (parseInt(i / (wcount)) % 2 == 0) {
                        this.xcor = (i % wcount) * zoneW;

                    } else {
                        this.xcor = (zoneW * (wcount - 1)) - ((i % wcount) * zoneW);

                    }
                    return this.xcor;
                });


        } else if (mapMode === 2) {
            var events = [];
            g.on('click', function () {
                events.push(d3.event);
                if (events.length > 2) events.shift();
                var circles = svg.selectAll('circle')
                    .data(events, function (e) {
                        return e.timeStamp
                    })
                    .attr('fill', 'gray');
                circles
                    .enter()
                    .append('circle')
                    .attr('cx', function (d) {
                        myCoordinate[0] = d3.mouse(svg.node())[0]
                        return myCoordinate[0]
                    })
                    .attr('cy', function (d) {
                        myCoordinate[1] = d3.mouse(svg.node())[1]
                        return myCoordinate[1]
                    })
                    .attr('fill', 'red')
                    .attr('r', 10);
                circles
                    .exit()
                    .remove();

            });



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