import { createStore } from "vuex"
import { handleGetInfo, updateState, addTemplate, removeTemplate, editTemplate } from "@/api/department"
import { handleCommonLogin, handleSuperLogin, handleUpdateInfo } from "@/api/login"

export default createStore({
    state() {
        return {
            userInfo: "",
            deptInfo: ""
        }
    },
    getters: {
        computeRole(state) {
            let scopes = state.userInfo.scopes
            let role = "NULL"
            if(scopes.length) {
                scopes.indexOf("supervisor") !== -1? 
                role =  "超级管理员" : scopes.indexOf("administrator") !== -1? 
                role =  "部门管理员" : role =  "普通成员"
            }
            return role
            
        }
    },
    mutations: {
        GET_USER_INFO(state) {
            try {
                state.userInfo = JSON.parse(window.localStorage.getItem("userInfo"))
            }catch(error) {
                // 如果出现异常则说明本地信息被人为纂改，此时移除本地信息 
                window.localStorage.removeItem("userInfo")
            }   
        },
        SET_USER_INFO(_, data) {
            window.localStorage.setItem("userInfo", JSON.stringify(data))
        },
        SET_DEPT_INFO(state, data) {
            state.deptInfo = data
        },
        UPDATE_DEPT_STATE(state) {
            let show = state.deptInfo.show
            state.deptInfo.show = !show
        },
        UPDATE_DEPT_TEMPLATE(state, data) {
            state.deptInfo.mail_template = data
        }
    },
    actions: {
        handleCommonLogin({ commit }, code) {
            return new Promise((resolve, reject) => {
                handleCommonLogin({code: code}).then(res => {
                    commit("SET_USER_INFO", res)
                    resolve()
                }).catch(error => {
                    reject(error)
                })
            })
        },
        handleSuperLogin({ commit }, data) {
            return new Promise((resolve, reject) => {
                handleSuperLogin(data).then(res => {
                    commit("SET_USER_INFO", res)
                    resolve()
                }).catch(error => {
                    reject(error)
                })
            })
        },
        handleUpdateInfo({ commit }, data) {
            return new Promise((resolve, reject) => {
                handleUpdateInfo().then(res => {
                    commit("SET_USER_INFO", Object.assign(data, res))
                    resolve()
                }).catch(error => {
                    reject(error)
                })
            })
        },
        getDeptInfo({ commit }) {
            return new Promise((resolve, reject) => {
                handleGetInfo().then(res => {
                    commit("SET_DEPT_INFO", res)
                    resolve()
                }).catch(error => {
                    reject(error)
                })
            })
        },
        updateState({ commit }, data) {
            return new Promise((resolve, reject) => {
                updateState(data).then(() => {
                    commit("UPDATE_DEPT_STATE")
                    resolve()
                }).catch(error => {
                    reject(error)
                })
            })
        },
        addTemplate({ commit }, data) {
            return new Promise((resolve, reject) => {
                addTemplate(data).then(res => {
                    commit("UPDATE_DEPT_TEMPLATE", res.mail_template)
                    resolve()
                }).catch(error => {
                    reject(error)
                })
            })
        },
        removeTemplate({ commit }, data) {
            return new Promise((resolve, reject) => {
                removeTemplate(data).then(res => {
                    commit("UPDATE_DEPT_TEMPLATE", res.mail_template)
                    resolve()
                }).catch(error => {
                    reject(error)
                })
            })
        },
        editTemplate({ commit }, data) {
            return new Promise((resolve, reject) => {
                editTemplate(data).then(res => {
                    commit("UPDATE_DEPT_TEMPLATE", res.mail_template)
                    resolve()
                }).catch(error => {
                    reject(error)
                })
            })
        }

    }
});