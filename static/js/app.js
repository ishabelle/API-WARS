let allPlanets = document.querySelector("#planets");
let page = 1;

let previousButton = document.querySelector(".previous");
let nextButton = document.querySelector(".next");

let residentsTable = document.querySelector("#residents-table");
let modalResidents = document.querySelector(".modal");
const overlay = document.querySelector(".overlay");
const closeModal = document.querySelector(".close-modal");
const headerResidents = document.querySelector("#header-residents");

const votingStatistics = document.querySelector("#voting-statistics");
const tableStatistics = document.querySelector("#statistics")
let username = document.getElementById("username")


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
                        <th>NAME</th>
                        <th>DIAMETER</th>
                        <th>CLIMATE</th>
                        <th>TERRAIN</th>
                        <th>SURFACE WATER</th>
                        <th>POPULATION</th>
                        <th>RESIDENTS</th>
                        ${username ?`<th>VOTE</th>` : ``}
                    </tr>
                </thead>
                `
    let tBody = document.createElement('tbody');
    tBody.setAttribute('id', 'tbody');
    allPlanets.appendChild(tBody)
    data.results.forEach((detail) => {
        document.querySelector("#tbody")
            .innerHTML += `<tr>
                               <td>${detail.name}</td>
                               <td>${dataDiameterFormat(detail.diameter)}</td>
                               <td>${detail.climate}</td>
                               <td>${detail.terrain}</td>
                               <td>${dataWaterFormat(detail.surface_water)}</td>
                               <td>${dataPopulationFormat(detail.population)}</td>
                               <td>${detail.residents.length === 0 ?
            `<button class="buttonResidents disabled" disabled>"NO KNOW RESIDENTS"</button>` :
            `<button class="${detail.name.split(" ")[0]} buttonResidents ">${detail.residents.length} RESIDENT(S)</button>`}
                               </td>
                               ${username ? `<td>${username ?`<button class="vote-planets" id="${detail.name}">VOTE</button>`: `<small></small>`}</td>` : ``}
                           </tr>`
    })

    let voteButtons = document.querySelectorAll(".vote-planets");
    voteButtons.forEach((butt) => {
        butt.addEventListener('click', function (e){
            e.preventDefault()
            let userId = document.querySelector("#user-id").value
            let planetId = e.target.id
            let planetName = e.target.id
            let newEntry = {
                'planet_id': planetId,
                'planet_name': planetName,
                'user_id': userId
            }
            fetch('/api/vote-planets', {
                method: 'POST',
                body: JSON.stringify(newEntry),
                headers: {
                    'Content-type': 'application/json'
                },
            })
                .then((response) => response)


        })
    })


    let buttonResidents = document.querySelectorAll('.buttonResidents');
    buttonResidents.forEach((button, idx) => {
        button.addEventListener('click', function () {
            modalResidents.classList.toggle('hidden');
            overlay.classList.toggle('hidden')
            const linksResidents = data.results[idx].residents
            const thead = `
                        <thead>
                                <tr>
                                    <th>NAME</th>
                                    <th>HEIGHT</th>
                                    <th>MASS</th>
                                    <th>HAIR COLOR</th>
                                    <th>SKIN COLOR</th>
                                    <th>EYE COLOR</th>
                                    <th>BIRTH YEAR</th>
                                    <th>GENDER</th>
                                </tr>
                        </thead>`
            residentsTable.insertAdjacentHTML('beforeend', thead)
            linksResidents.forEach((link) => {
                link = link.replace('http', 'https')
                fetch(link)
                    .then((response) => response.json())
                    .then((residents) => {
                        let tBodyResidents = document.createElement('tbody');
                        tBodyResidents.setAttribute('id', 'tbodyResidents');
                        residentsTable.appendChild(tBodyResidents);
                        let tBodyR = document.querySelector('#tbodyResidents')
                        let html = `<tr>
                                        <td>${residents['name']}</td>
                                        <td>${dataHeightFormat(residents['height'])}</td>
                                        <td>${dataMassFormat(residents['mass'])}</td>
                                        <td>${residents['hair_color']}</td>
                                        <td>${residents['skin_color']}</td>
                                        <td>${residents['eye_color']}</td>
                                        <td>${residents['birth_year']}</td>
                                        <td>${dataGenderFormat(residents['gender'])}</td>
                                    </tr>`
                        tBodyR.insertAdjacentHTML('beforeend', html)
                    })
            })

            let residentsHeader = `<h1 class="residents-title page-titles">Residents of ${button.classList[0]}</h1>`
            headerResidents.insertAdjacentHTML('beforeend', residentsHeader)

        })
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


function dataWaterFormat(data) {
    if (data !== 'unknown') {
        return data + ' %'
    } else {
        return data
    }
}


function dataDiameterFormat(data) {
    if (data !== 'unknown') {
        return new Intl.NumberFormat().format(data) + ' km'
    } else {
        return data
    }
}

function dataPopulationFormat(data) {
    if (data !== 'unknown') {
        return new Intl.NumberFormat().format(data) + ' people'
    } else {
        return data
    }
}


function dataMassFormat(data) {
    if (data !== 'unknown') {
        return new Intl.NumberFormat().format(data) + ' kg'
    } else {
        return data
    }
}


function dataHeightFormat(data) {
    if (data !== 'unknown') {
        return new Intl.NumberFormat().format(data / 100) + ' m'
    } else {
        return data
    }
}


function dataGenderFormat(data) {
    if (data === 'female') {
        return String('♀')
    }
    if (data === 'male') {
        return String('♂')
    } else {
        return data
    }
}


closeModal.addEventListener('click', function () {
    modalResidents.classList.add('hidden')
    overlay.classList.add('hidden')
    residentsTable.innerHTML = '';
    headerResidents.innerHTML = '';
})


votingStatistics.addEventListener('click', function (e){
    e.preventDefault()
    modalResidents.classList.toggle("hidden");
    overlay.classList.toggle("hidden")
    fetch('/api/get-planets-votes')
        .then((response) => response.json())
        .then((data) => {
            const thead = `
                        <thead>
                                <tr>
                                    <th>PLANET NAME</th>
                                    <th>RECEIVED VOTES</th>
                                </tr>
                        </thead>`
            tableStatistics.insertAdjacentHTML('beforeend', thead)
            let tBody = document.createElement("tbody");
            tableStatistics.appendChild(tBody)
            data.forEach((details) => {
                tBody.innerHTML += `<tr>
                                        <td>${details.planet_name}</td>
                                        <td>${details.recived_votes}</td>
                                    </tr>`
            })

        })
})


downloadPlanets(`https://swapi.dev/api/planets/?page=${page}`)