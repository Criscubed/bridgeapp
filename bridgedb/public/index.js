const baseUrl = "http://localhost:5500/";

const input = document.getElementById('input');
const getBtn = document.getElementById('get');
getBtn.addEventListener('click', getInfo);

async function getInfo(e) {
    e.preventDefault();
    console.log("WHAT IS HAPPENING")
    window.location.href = baseUrl + input.value;
    // e.preventDefault();
    // if (input.value == '') { return };
    // const res = await fetch(baseUrl + 'redirect/' + input.value,
    // {
    //     method: 'GET'
    // });
    // const data = await res.json()
    // window.location = baseUrl + data.redirectUrl
}


// async function postInfo(e) {
//     e.preventDefault();
//     if (input.value == '') { return }
//     console.log("trying to redirect")
//     const res = await fetch(baseUrl,
//     {
//         method: 'POST',
//         headers: {
//             "Content-Type": 'application/json'
//         },
//         body: JSON.stringify({
//             parcel: input.value
//         })
//     })
// }