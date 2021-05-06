<template>
    <div class="container">
            <b-button @click="showAddProjectModal()" variant="light" class="float-right mr-2 mb-2"><b-icon icon="plus" scale="1.3" class="pt-1 pr-1"></b-icon>New project</b-button>
        <div class="table">
            <b-table class="" responsive=true :items="projectsList" :fields="fields">
                <template #cell(project_name)="row">
                    <b-button variant="outline-dark" size="sm" class="font-weight-bold" v-on:click="openProjectModal(row.item.id, row.item.project_name)">{{ row.item.project_name }}</b-button>
                </template>
                <template #cell(get_total_project_time)="row">
                    {{ row.item.get_total_project_time ? row.item.get_total_project_time : "Still procrastinating"}}
                </template>
                <template #cell(actions)="row">
                    <b-button size="sm" variant="danger" @click="showDeleteProjectModal(row.item.id)">Delete</b-button>
            </template>
            </b-table>
        </div>
        <b-modal ref="projectModal">
            <b-table class="sm" :fields="projectModalFields" :items="projectModalItems">
            <template #cell(start_time)="row">
                {{ buildTime(row.item.start_time) }}
            </template>
            <template #cell(end_time)="row">
                {{ row.item.end_time ? buildTime(row.item.end_time) : "In progress..."}}
            </template>
            <template #cell(get_total_time)="row">
                {{ row.item.get_total_time ? row.item.get_total_time : "In progress"}}
            </template>
            <template #cell(date)="row">
                {{ buildDate(row.item.start_time) }}
            </template>
            </b-table>
        </b-modal>

        <b-modal ref="projectAddModal" @ok="createNewProject">
            <div>
            <h4>Create new project</h4>
            <b-input-group prepend="Project name" class="mt-3">
                <b-form-input v-model="newProjectName"></b-form-input>
            </b-input-group>
            </div>
        </b-modal>
        <b-modal ref="deleteProjectModal" @ok="deleteProjectFunction">
            Are you sure?
        </b-modal>
     </div>
</template>

<script>
import { getProjectsList, createProject, deleteProject } from '../api/projects';
import { getHoursList } from '../api/hours';

export default {
    data() {
        return {
            deleteProjectId: -1,
            newProjectName: "",
            projectModalTitle: "",
            projectModalItems: [],
            projectModalFields: [
                {key: "id", label: "Id"},
                {key: "start_time", label: "Start Time"},
                {key: "end_time", label: "End Time"},
                {key: "get_total_time", label: "Total Time"},
                {key: "date", label: "Date"}
            ],
            projectsList: [],
            fields: [
                {key: "id", label: "Id"},
                {key: "project_name", label: "Project"},
                {key: "get_total_project_time", label: "Total time spent"},
                {key: "actions", label: "Actions"}
            ],
        }
    },
    methods: {
        buildDate(time) {
            let date = new Date(time)
            let offset = -date.getTimezoneOffset()/60
            let hours = date.getHours() + offset
            if (hours == 24 || hours == 25 ) {
                date.setDate(date.getDate() + 1)
            }
            return date.toDateString()
        },
        showDeleteProjectModal(id) {
            this.deleteProjectId = id
            this.$refs.deleteProjectModal.show()
        },
        deleteProjectFunction() {
            deleteProject(this.deleteProjectId).then(response => {
                if (response.status == 204) {
                    this.$toast.success("Deleted successfully!", {duration: 1000})
                    this.refreshTable()
                    this.$emit('project-created')
                }
                else {
                    this.$toast.error("Something went wrong", {duration: 1000})
                }
            })
        },
        refreshTable() {
            this.getProjects()
        },
        createNewProject() {
            if (!this.newProjectName) {
                return this.$toast.error("Project name is required", {duration: 1000})
            }
            createProject(this.newProjectName).then(response => {
                if (response.status == 201) {
                    this.$toast.success("Project created", {duration: 1000})
                    this.refreshTable()
                    this.$emit('project-created')
                }
                else {
                    this.$toast.error("Something went wrong", {duration: 1000})
                }
            })
            this.newProjectName = ""
        },
        showAddProjectModal() {
            this.$refs.projectAddModal.show()
        },
        buildTime(time) {
            let date = new Date(time)
            let offset = -date.getTimezoneOffset()/60
            let hours = date.getHours() + offset
            if (hours >= 24) {
                hours -= 24
            }
            hours = hours.toLocaleString('en-US', {minimumIntegerDigits: 2})
            let minutes = date.getMinutes().toLocaleString('en-US', {minimumIntegerDigits: 2})
            let seconds = date.getSeconds().toLocaleString('en-US', {minimumIntegerDigits: 2})
            return hours + ":" + minutes + ":" + seconds
        },
        getProjects() {
            getProjectsList().then(response => {
                this.projectsList = response.data
            })
        },
        onMounted() {
            this.getProjects()
        },
        async openProjectModal(id, projectTitle) {
            let response = await getHoursList(id).then(res => res.data.hours)
            if (response) {
                this.projectModalItems = response
            }
            else {
                this.projectModalItems = []
            }
            this.projectModalTitle = projectTitle
            this.$refs.projectModal.show("projectModal", {duration: 1000})
        }
    },
    mounted() {
        this.onMounted()
    }
}
</script>

<style>
.container {
    
}
table {
    width: 100%;
}
#project-btn {
    border: none;
}

</style>