window.onload = function () {
    'use strict';
    let deleteBuildingButtons = document.getElementsByClassName('delete-building-button');
    [].forEach.call(deleteBuildingButtons, function (elem) {
        elem.addEventListener('click', function (e) {
            let buildingId = e.srcElement.dataset.buildingId;
            var Request = new XMLHttpRequest();
            Request.open('DELETE', '/api/v1/building/'+buildingId, true);
            Request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
            Request.addEventListener("readystatechange", () => {
                if (Request.readyState === 4 && Request.status === 200) {
                    let buildingRow=document.getElementsByClassName('row-building-'+buildingId)[0].remove();
                }
            });
            Request.send(buildingId);
        })
    })
}