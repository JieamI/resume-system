import request from "@/utils/request.js"

export function getAuthInfo() {
    return request({
        url: "/authority/getinfo",
        method: "get"
    })
}

export function updateAuthority(data) {
    return request({
        url: "/authority/updateinfo",
        method: "post",
        data
    })
}