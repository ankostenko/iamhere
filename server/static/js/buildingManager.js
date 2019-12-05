window.onload = function () {
    'use strict';
    let deleteStageButtons = document.getElementsByClassName('delete-stage-button');
    [].forEach.call(deleteStageButtons, function (elem) {
        elem.addEventListener('click', function (e) {
            let stageId = e.srcElement.dataset.stageId;
            var Request = new XMLHttpRequest();
            Request.open('DELETE', '/api/v1/stage/' + stageId, true);
            Request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
            Request.addEventListener("readystatechange", () => {
                if (Request.readyState === 4 && Request.status === 200) {
                    let buildingRow = document.getElementsByClassName('row-stage-' + stageId)[0].remove();
                }
            });
            Request.send(stageId);
        })
    })
};