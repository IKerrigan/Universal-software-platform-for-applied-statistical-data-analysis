const generateRealButtonEl = document.getElementById('generate-real-data');

let uploadMode = 0;
let fileData = {};

const ExcelToJSON = function () {
    this.parseExcel = function (file, cb) {
        let reader = new FileReader();

        reader.onload = function (e) {
            let content = e.target.result;

            let workbook = XLSX.read(content, {
                type: 'binary'
            });

            fileData = { content, name: file.name };

            workbook.SheetNames.forEach(function (sheetName) {
                let XL_row_object = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
                let json_object = JSON.stringify(XL_row_object);
                fileData.parsed = json_object;

                jQuery('#xlx_json').val(json_object);
            })

            cb();
        };

        reader.onerror = function (ex) {
            console.log(ex);
        };

        reader.readAsBinaryString(file);
    };
};

function handleFileSelect(evt) {
    var files = evt.target.files;
    var xl2json = new ExcelToJSON();
    uploadMode = 0;
    xl2json.parseExcel(files[0], handleTextParsingFinished);
}

function handleTextParsingFinished() {
    const textAreaEl = document.getElementById('xlx_json')
    const rowArray = JSON.parse(textAreaEl.value)

    const selectHeaderEl = document.getElementById('real-data-header-select')
    let selectHtml = "";
    let id = 1;

    for (const header of Object.keys(rowArray[0])) {
        selectHtml += `<option value="${id}">${header}</option>`
        id++;
    }

    selectHeaderEl.innerHTML = selectHtml;
    generateRealButtonEl.disabled = false;
}

async function handleRemoteFileSelect(e) {
    const file = await getFile(e.target.value);
    jQuery('#xlx_json').val(file.parsed);
    handleTextParsingFinished();
    uploadMode = 1;
}

document.getElementById('upload').addEventListener('change', handleFileSelect, false);
document.getElementById('real-data-file-select').addEventListener('change', handleRemoteFileSelect);