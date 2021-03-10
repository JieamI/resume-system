import checkPermission from "./index"

export function switchPermission(el, binding) {
    if(!checkPermission(binding)) {
        el.disabled = true
        el.classList.add("ant-switch-disabled")
    }
}

