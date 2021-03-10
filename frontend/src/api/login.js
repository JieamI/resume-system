import request from "@/utils/request.js"

export function handleCommonLogin(data) {
    return request({
        url: "/login/common",
        method: "post",
        data
    })
}

export function handleSuperLogin(data) {
    return request({
        url: "/login/super",
        method: "post",
        data
    })
}

export function handleUpdateInfo() {
    return request({
        url: "/login/update",
        method: "get"
    })
}