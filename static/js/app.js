let allPlanets = document.querySelector("#planets");
let page = 1;

let previousButton = document.querySelector(".previous")
let nextButton = document.querySelector(".next")


function downloadPlanets(url) {
    fetch(url)
        .then((response) => response.json())
        .then((planets) => {
            let previousData = planets.previous
            let nextData = planets.next
            previousData !== null ? previousButton.removeAttribute("disabled") : previousButton.setAttribute("disabled", "disabled")
            nextData === null ? nextButton.setAttribute("disabled", "disabled") : nextButton.removeAttribute("disabled")
            displayPlanets(planets)
        })
}


function displayPlanets(data) {
    allPlanets.innerHTML = `
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>NAME</th>
                        <th>DIAMETER</th>
                        <th>CLIMATE</th>
                        <th>TERRAIN</th>
                        <th>SURFACE WATER</th>
                        <th>POPULATION</th>
                    </tr>
                </thead>
                `
    let tBody = document.createElement('tbody');
    tBody.setAttribute("id", "tbody");
    allPlanets.appendChild(tBody)
    data.results.forEach((detail, index) => {
        document.querySelector("#tbody")
            .innerHTML += `<tr>
                               <td>${index + 1}</td>
                               <td>${detail.name}</td>
                               <td>${detail.diameter}</td>
                               <td>${detail.climate}</td>
                               <td>${detail.terrain}</td>
                               <td>${detail.surface_water}</td>
                               <td>${detail.population}</td>
                           </tr>`
    })
}


previousButton.addEventListener('click', function () {
    page -= 1
    downloadPlanets(`https://swapi.dev/api/planets/?page=${page}`)
})


nextButton.addEventListener('click', function () {
    page += 1
    downloadPlanets(`https://swapi.dev/api/planets/?page=${page}`)
})


downloadPlanets(`https://swapi.dev/api/planets/?page=${page}`)