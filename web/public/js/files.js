const uploadRealDataButton = document.getElementById('upload-real-data');

let listOfFiles;

async function loadListOfFiles() {
    listOfFiles = await getListOfFiles();
}

uploadRealDataButton.onclick = async () => {
    const selectFileEl = document.getElementById('real-data-file-select')
    let selectHtml = "";

    listOfFiles.forEach(e => {
        selectHtml += `<option value="${e.name}">${e.name}</option>`
    });

    selectFileEl.innerHTML = selectHtml;

    if(listOfFiles.length > 0) {
        const file = await getFile(listOfFiles[0].name);
        jQuery('#xlx_json').val(file.parsed);
        handleTextParsingFinished();
        uploadMode=1;
    }
}

loadListOfFiles()