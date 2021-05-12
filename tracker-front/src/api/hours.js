import axios from 'axios'
const endpoint = "http://api.zrezke.com:8000/api/hours/"

export function getHoursList(id) {
    if (id) {
        return axios.get(`${endpoint}project/${id}/`)
    }
    return axios.get(endpoint)
    }
export function getHours(id) {
        return axios.get(`${endpoint}${id}/`)
    }
export function startTracker(projId) {
        return axios.post(`${endpoint}project/${projId}/`)
    }
export function stopTracker(id) {
        return axios.patch(`${endpoint}${id}/`)
    }
