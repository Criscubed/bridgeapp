const baseUrl = "http://localhost:5500/";

const input = document.getElementById('input');
const getBtn = document.getElementById('get');
getBtn.addEventListener('click', getInfo);

async function getInfo(e) {
    e.preventDefault();
    window.location.href = baseUrl + input.value;

}
