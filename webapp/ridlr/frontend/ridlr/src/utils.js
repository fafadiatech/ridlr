export const readCookie = function (name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
};

export const postHeaders = {
    "Content-Type": "application/json",
    "Accept": "application/json"
};

export const getRequest = function getRequest(url, successFunc, headers = false, extra_data = false) {
    if (!headers) {
        headers = postHeaders;
    }

    return fetch(url, {
            headers,
            method: "GET"
        })
        .then((response) => {
            if (response.status === 200 || response.status === 400) {
                return response.json().then(data => {
                    if (!extra_data) {
                        return successFunc(data);
                    } else {
                        return successFunc(data, extra_data);
                    }
                })
            }
            if (response.status === 401 || response.status === 403) {
                throw Error("Forbidden");
            }
            if (response.status >= 500) {
                throw Error("Internal Server Error");
            }
        }).catch((err) => {
            // setState({ "server_error": true })
            console.log(err);
        });
};

export const postRequest = function postRequest(url, body, successFunc, headers = false, method = "POST", extra_data = false) {
    if (!headers) {
        headers = postHeaders;
    }
    return fetch(url, {
            headers: headers,
            body: body,
            credentials: "same-origin",
            method: method
        })
        .then((response) => {
            console.log(response)
            if (response.status === 200 || response.status === 201 || response.status === 400) {
                return response.json().then(data => {
                    if (!extra_data) {
                        return successFunc(data);
                    } else {
                        return successFunc(data, extra_data);
                    }
                })
            }
            // for entity already exists
            if (response.status === 422) {
                return response.json().then(data => {
                    if (!extra_data) {
                        return successFunc(data);
                    } else {
                        return successFunc(data, extra_data);
                    }
                })
            }
            if (response.status === 401 || response.status === 403) {
                return response.json().then(data => {
                    console.log(data)
                    return successFunc(data);
                })
                // throw Error("Internal Server Error");
            }
            if (response.status >= 500) {
                console.log(response)
                throw Error("Internal Server Error");
            }
        }).catch((err) => {
            console.log(err);
            throw Error("Internal Server Error");
        });
};

export const putRequest = function putRequest(url, body, successFunc, headers = false, method = "PUT", extra_data = false) {
    if (!headers) {
        headers = postHeaders;
    }

    return fetch(url, {
            headers,
            body,
            method: method
        })
        .then((response) => {
            if (response.status === 200 || response.status === 201 || response.status === 400) {
                return response.json().then(data => {
                    if (!extra_data) {
                        return successFunc(data);
                    } else {
                        return successFunc(data, extra_data);
                    }
                })
            }
            // for entity already exists
            if (response.status === 422) {
                return response.json().then(data => {
                    if (!extra_data) {
                        return successFunc(data);
                    } else {
                        return successFunc(data, extra_data);
                    }
                })
            }
            if (response.status === 401 || response.status === 403) {
                console.log(response)
                throw Error("Internal Server Error");
            }
            if (response.status >= 500) {
                console.log(response)
                throw Error("Internal Server Error");
            }
        }).catch((err) => {
            console.log(err);
            successFunc("error")
            // throw Error("Internal Server Error");
        });
};