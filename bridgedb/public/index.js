const getBtn = document.getElementById('get');
const stuffdiv = document.getElementById('stuff');

const baseUrl = "http://localhost:5500/";

getBtn.addEventListener('click', getInfo)
async function getInfo(e) {
    e.preventDefault();
    const res = await fetch(baseUrl + 'b?x=16C020301L',
    {
        mehtod: 'GET'
    })
    console.log(res);
    const data = await res.json();

    stuffdiv.innerHTML = JSON.stringify(data);
}