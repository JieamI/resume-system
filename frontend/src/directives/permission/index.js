import store from "@/store"

export default function checkPermission(binding) {
    let requestRole = binding.value
    let haveRole = store.state.userInfo.scopes

    for(let i = 0; i < haveRole.length; i++) {
        if(requestRole.indexOf(haveRole[i]) !== -1) return true
    }
    
    return false 
}
