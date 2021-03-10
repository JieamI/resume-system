import request from "@/utils/request.js"

export function getCvInfo() {
    return request({
        url: "/cv/getinfo",
        method: "get"
    })
}

export function updateState(data) {
    return request({
        url: "/cv/updatestate",
        method: "post",
        data
    })
}

export function updateSign(data) {
    return request({
        url: "/cv/updatesign",
        method: "post",
        data
    })
}

export function pushComment(data) {
    return request({
        url: "/cv/comment",
        method: "post",
        data
    })
}

export function getComment(data) {
    return request({
        url: "/cv/getcomment",
        method: "post",
        data
    })
}

export function removeCv(data) {
    return request({
        url: "/cv/remove",
        method: "post",
        data
    })
}

export function sendEmail(data) {
    return request({
        url: "cv/sendemail",
        method: "post",
        data,
    })
}

export function getTimeSection() {
    return request({
        url: "cv/timesection",
        method: "get",
    })
}

export function getStatistics(params) {
    return request({
        url: "cv/statistics",
        method: "get",
        params
    })
}




