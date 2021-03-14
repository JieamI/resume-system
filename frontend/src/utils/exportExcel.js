export function toCsv(data) {
    let field = new Map([
        ["学号", "sno"],
        ["姓名", "name"],
        ["性别", "sex"],
        ["生日", "birthday"],
        ["籍贯", "hometown"],
        ["民族", "nation"],
        ["学院", "college"],
        ["年级", "grade"],
        ["专业班级", "proclass"],
        ["宿舍", "dormitory"],
        ["手机", "phone"],
        ["QQ", "qq"],
        ["邮箱", "mail"],
        ["自我介绍", "introduce"],
        ["加入理由", "reason"],
        ["个人经历", "experience"],
    ])
    let text = [...field.keys()].join(",") + "\n"

    for(let i = 0; i < data.length; i++) {
        // eslint-disable-next-line no-unused-vars
        let item = data[i]
        for(let val of field.values()) {
            let content = item[val].trim()
            if(content.includes("\n")) content = content.replace(/\n/g," ")
            
            if(content.includes('"')) content = content.replace(/"/g, '""')

            if(content.includes(",")) content = `"${content}"`
            
            text += `${content},`
        }
        text += "\n"
    }
    
    let blob = new Blob([text], { type: "text/plain;charset=utf-8" })  
    blob = new Blob([String.fromCharCode(0xFEFF), blob], { type: blob.type })
    let url = window.URL.createObjectURL(blob)
    let el = document.createElement("a")
    el.href = url
    el.download = "导出.csv"
    document.body.appendChild(el)
    el.click()
    document.body.removeChild(el)    
}