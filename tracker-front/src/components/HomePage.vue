<template>
    <div class="container">
        <div class=tracker-div>
            <div class="tracker-text">
                <h2>{{ time }}</h2>
            </div>
            <b-button-group v-show="!start">
            <b-button variant="outline-success" @click="startTimer(selectedProject ? selectedProject.id : null)">Start tracker</b-button>
            <b-dropdown right variant="outline-info" :text="selectedProject ? selectedProject.project_name : 'Project'">
                <b-dropdown-item @click="selectedProject = project" v-for="project in projectsList" :key="project.id">{{ project.project_name }}</b-dropdown-item>
            </b-dropdown>
            </b-button-group>
            <b-button v-show="start" variant="outline-danger" @click="stopTimer()">Stop</b-button>
        </div>
        <projects-table ref="table" v-on:project-created="onMounted"></projects-table>
    </div>
</template>

<script>
import { getHoursList, getHours, startTracker, stopTracker } from '../api/hours';
import {getProjectsList, getProject, createProject} from '../api/projects';
import ProjectsTable from './ProjectsTable.vue';

//window.addEventListener('focus', () => $refs.updateTimeOnFocus)
// get time from api
export default {
    components: {
        ProjectsTable
    },
    props: {
    },
    data() {
        return {
            update: false,
            selectedProject: null,
            start: false,
            interval: null,
            timerId: 0,
            time: "00:00:00",
            projectsList: [],
            hoursList: [],
            seconds: 0,
            minutes: 0,
            hours: 0
        }
    },
    methods: {
        updateTimeOnFocus() {
            if(this.start) {
                getHours(this.timerId).then(response => {
                let date = new Date(response.data.hours[0].start_time)
                let offset = -date.getTimezoneOffset()/60
                let hours = date.getHours() + offset
                date.setHours(hours)
                let ms = new Date() - date
                var seconds = ms / 1000;
                hours = parseInt( seconds / 3600 )
                seconds = seconds % 3600
                var minutes = parseInt( seconds / 60 )
                seconds = Math.round(seconds % 60);
                this.hours = hours
                this.minutes = minutes
                this.seconds = seconds
                })
            }
        },
        startTimer(projectId) {
            if (!projectId) {
                this.$toast.error("Select a project", {duration: 1500})
                return;
            }
            this.start = true
            startTracker(projectId).then(response => {
                this.timerId = response.data.id
            })
            this.interval = setInterval(this.timeKeeper, 1000)
        },
        stopTimer() {
            this.start = false
            clearInterval(this.interval)
            this.$toast.info("Saving time...", 0)
            stopTracker(this.timerId).then(response => {
                this.$refs.table.refreshTable()
                this.$toast.clear()
                this.time = "00:00:00"
                this.hours = 0
                this.minutes = 0
                this.seconds = 0
            })
        },
        timeKeeper() {
            if (this.seconds == 59) {
                this.seconds = 0
                if (this.minutes == 59) {
                    this.minutes = 0
                    this.hours += 1
                    return this.formatTime();
                }
                this.minutes += 1
                return this.formatTime();
            }
            this.seconds += 1;
            return this.formatTime()
        },
        formatTime() {
            let h_str = this.hours.toLocaleString('en-US', {minimumIntegerDigits: 2})
            let m_str = this.minutes.toLocaleString('en-US', {minimumIntegerDigits: 2})
            let s_str = this.seconds.toLocaleString('en-US', {minimumIntegerDigits: 2})
            this.time = h_str + ":" + m_str + ":" + s_str
        },
        getProjects() {
            getProjectsList().then(response => {
                this.projectsList = response.data
            })
        },
        getHoursList() {
            getHoursList().then(response => {
                this.hoursList = response.data
            })
        },
        onMounted() {
            this.getProjects()
            this.getHoursList()
            window.addEventListener('focus', () => this.update = true)
        },
    },
    mounted() {
        this.onMounted()
    },
    watch: {
        update: function () {
            if (this.update){
                this.updateTimeOnFocus()
            }
            this.update = false;
        }
    }
}
</script>

<style>

.container {
    margin-top: 5%;
}
.tracker-div {
    margin-top: 30%;
}
.start-track-btn {
    min-width: 85px;
    min-height: 35px;
    border: none;
    border-radius: 5px;
    background: #EAB464;
    color: #646E78;
}
.stop-track-btn {
    min-width: 85px;
    min-height: 35px;
    border: none;
    border-radius: 5px;
    background: #721817;
    color: #646E78;
}
</style>