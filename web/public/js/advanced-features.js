const advancedFeaturesWaEl = document.getElementById('advanced-features-wa')
const advancedFeaturesStatsEl = document.getElementById('advanced-features-stats')

const advancedFeaturesIds = [...Array(7)].map((v, i) => `advanced-feature-${i + 1}`)
const advanceFeatureEls = advancedFeaturesIds.map(v => document.getElementById(v))

function createAdvanceFeatureHandler(mode) {
    return async function () {
        const { chart, stats } = await execAdvancedFeature(mode)

        advancedFeaturesWaEl.innerHTML = ""
        advancedFeaturesStatsEl.innerHTML = ""

        const parser = new DOMParser();
        const doc = parser.parseFromString(chart, "text/html");

        advancedFeaturesWaEl.innerHTML += doc.body.innerHTML
        executeScriptElements(advancedFeaturesWaEl)

        for (const stat of stats) {
            let statCol = (d) => `<div class="col-xl-4">${d}</div>`
            let statHtml = "";

            for (const statField of ['text', 'mean', 'variance', 'standard_deviation']) {
                statHtml += statEl(statField, stat[statField])
            }

            advancedFeaturesStatsEl.innerHTML += statCol(statHtml)
        }
    }
}

advanceFeatureEls.forEach((el, i) => {
    el.onclick = createAdvanceFeatureHandler(i + 1)
})