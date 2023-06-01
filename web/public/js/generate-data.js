const generateModelEl = document.getElementById('generate-model');
const generateRealDataEl = document.getElementById('generate-real-data');
const advancedFeaturesButton = document.getElementById('advanced-features');


generateModelEl.onclick = async function () {
    const { charts, stats, sv_av, values } = await generateModel();
    window.localStorage.setItem('sv_av', sv_av)
    window.localStorage.setItem('values', values)
    buildCharts(charts, stats)

    advancedFeaturesButton.disabled = false;
}

generateRealDataEl.onclick = async function () {
    const parsedSpreadsheet = document.getElementById('xlx_json')

    const headerEl = document.getElementById("real-data-header-select");
    const header = headerEl.options[headerEl.selectedIndex].text;

    const generatedSVAV = JSON.parse(parsedSpreadsheet.value).map(function (v) { 
        return Number(v[header]).toFixed(2).toString() })

    const { charts, stats, sv_av, values } = await generateRealData(generatedSVAV);

    if (uploadMode === 0) {
        await createFile(fileData)
    }

    window.localStorage.setItem('sv_av', sv_av)

    window.localStorage.setItem('values', values)
    buildCharts(charts, stats)

    advancedFeaturesButton.disabled = false;
}