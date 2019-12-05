window.onload = function() {
    'use strict'
    let addButton = document.getElementsByClassName('add-building')[0];
    let resultCaption = document.getElementsByClassName('result-caption')[0];
    addButton.addEventListener('click', function () {
        let buildingName = document.getElementById('building-name');
        let buildingDescription = document.getElementById('building-description');


        let obj = {
            'name': buildingName.value,
            'description': buildingDescription.value
        };
        let json = JSON.stringify(obj);
        var Request = new XMLHttpRequest();
        Request.open('POST', '/api/v1/buildings', true);
        Request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
        Request.addEventListener("readystatechange", () => {
            if (Request.readyState === 4 && Request.status === 200) {
                resultCaption.textContent = 'Здание добавлено успешно!';
                setTimeout(hideResultCaption,3000);
            }
        });
        Request.send(json);
        buildingName.value = '';
        buildingDescription.value = '';
    });

    function hideResultCaption(){
        resultCaption.textContent='';
    }
};
