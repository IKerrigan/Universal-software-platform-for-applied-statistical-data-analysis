function executeScriptElements(containerElement) {
    const scriptElements = containerElement.querySelectorAll("script");

    Array.from(scriptElements).forEach((scriptElement) => {
        const clonedElement = document.createElement("script");

        Array.from(scriptElement.attributes).forEach((attribute) => {
            clonedElement.setAttribute(attribute.name, attribute.value);
        });

        clonedElement.text = scriptElement.text;

        scriptElement.parentNode.replaceChild(clonedElement, scriptElement);
    });
}

const label = {
    "standard_deviation": "Середнє квадратичне відхилення випадкової величини",
    "mean": "Математичне сподівання випадкової величини",
    "variance": "Дисперсія випадкової величини",
}

const statEl = (name, value) => `<div class="mb-3">
<div class="card ${label[name] ? 'border-left-primary' : 'border-left-danger'} shadow h-30 py-2">
    <div class="card-body">
        <div class="row no-gutters align-items-center">
            <div class="col mr-2">
            ${label[name] ?
        `<div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                    ${label[name]} </div> ` : ''}
                <div class="h5 mb-0 font-weight-bold text-gray-800">${value}</div>
            </div>
            ${label[name] ?
        `<div class="col-auto">
                <i class="fas fa-lightbulb fa-2x text-gray-300"></i>
            </div>` : ''
    }
        </div>
    </div>
</div>
</div>`

function buildCharts(charts, stats) {
    const chartsEl = document.getElementById("charts-1");
    chartsEl.innerHTML = "";

    charts.forEach((v, i) => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(v, "text/html");
        let elHtml = `<div class="row justify-content-center align-items-center mb-5">`
        let statsHtml = "";

        for (const stat of ['text', 'mean', 'variance', 'standard_deviation']) {
            statsHtml += statEl(stat, stats[i][stat])
        }

        elHtml += `<div class="col-xl-6 col-lg-6 col-md-12 align-items-center">${doc.body.innerHTML}</div>`
        elHtml += `<div class="col-xl-4 col-lg-4 col-md-12 align-items-center">${statsHtml}</div>`
        elHtml += "</div>"

        chartsEl.innerHTML += elHtml
    });

    executeScriptElements(chartsEl)
}