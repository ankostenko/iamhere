window.onload = function () {
    'use strict';
    let addFloor = document.getElementById('addFloor');
    let buildingId = addFloor.dataset.buildingId;
    let stageName = document.getElementById('stage-name');
    let image = document.getElementById('FormControlFile');
    let resultCaption = document.getElementsByClassName('result-caption')[0];
    addFloor.addEventListener('click', function () {
        if (stageName.value.length !== 0 && image.files.length !== 0) {

            var formData = new FormData();
            formData.append('file', image.files[0]);
            var Request = new XMLHttpRequest();
            Request.open('POST', '/api/v1/upload/', true);
            Request.addEventListener("readystatechange", () => {

                if (Request.readyState === 4 || Request.status === 200) {
                    let obj = {
                        'name': stageName.value,
                        'building_id': buildingId,
                        'image_id': Request.response.trim()
                    };
                    let json = JSON.stringify(obj);
                    var stageRequest = new XMLHttpRequest();
                    stageRequest.open('POST', '/api/v1/stages/' + buildingId, true);
                    stageRequest.setRequestHeader('Content-type', 'application/json; charset=utf-8');
                    stageRequest.addEventListener("readystatechange", () => {
                        if (stageRequest.readyState === 4 && stageRequest.status === 200) {
                            resultCaption.textContent = 'Этаж добавлен успешно!';
                            setTimeout(hideResultCaption, 3000);
                        }
                    });

                    function hideResultCaption() {
                        resultCaption.textContent = '';
                    }
                    stageRequest.send(json);
                    stageName.value = '';
                    image.value = '';

                }

            });
            Request.send(formData);
        }
    })
};