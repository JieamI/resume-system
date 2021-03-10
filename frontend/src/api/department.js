import request from "@/utils/request.js"

export function handleGetInfo() {
    return request({
        url: "/dept/getinfo",
        method: "get"
    })
}

export function updateState(data) {
    return request({
        url: "/dept/updatestate",
        method: "post",
        data
    })
}

export function getRecord() {
    return request({
        url: "/dept/getrecord",
        method: "get"
    })
}

export function addTemplate(data) {
    return request({
        url: "dept/addtemplate",
        method: "post",
        data
    })
}

export function removeTemplate(data) {
    return request({
        url: "dept/removetemplate",
        method: "post",
        data
    })
}

export function editTemplate(data) {
    return request({
        url: "dept/edittemplate",
        method: "post",
        data
    })
}