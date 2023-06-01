async function makeRequest(method, url, data) {
    try {
        return (await axios[method](url, data)).data;
    } catch (e) {
        console.log(e)
        if(e.response.status === 401){
            localStorage.removeItem('auth')
            window.location = '/login.html'
        }

        jQuery("#errorModal").modal('toggle')
    }
}

function getWeatherData() {
    return makeRequest('get', '/api/weather/')
}

function generateModel() {
    return makeRequest('post', '/api/analyse/first-step', { mode: 1 })
}

function generateRealData(sv_av) {
    return makeRequest('post', '/api/analyse/first-step', { mode: 2, sv_av })
}

function execAdvancedFeature(mode) {
    const sv_av = localStorage.getItem('sv_av')
    const values = localStorage.getItem('values')
    return makeRequest('post', '/api/analyse/second-step', { mode, sv_av, values })
}

async function getFile(name) {
    return (await makeRequest('get', '/api/file/' + name)).file;
}

async function getListOfFiles() {
    return (await makeRequest('get', '/api/file/list')).files;
}

function createFile(payload) {
    return makeRequest('post', '/api/file/', payload);
}