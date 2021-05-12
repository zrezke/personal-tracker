import axios from 'axios'
const endpoint = "http://api.zrezke.com:8000/api/projects/"

export function getProjectsList() {
        return axios.get(endpoint)
    }
export function getProject(id) {
        return axios.get(`${endpoint}${id}/`)
    }
export function createProject(projectName) {
        return axios.post(endpoint, {
                project_name: projectName
        })
    }
export function deleteProject(id) {
    return axios.delete(`${endpoint}${id}/`)
}
