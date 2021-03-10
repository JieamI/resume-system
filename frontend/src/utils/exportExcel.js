export function toCsv(data) {
    // 由第一项取得各列标题
    let columns = Object.keys(data[0])
    // 去除sign和comment字段
    columns.splice(columns.indexOf("sign"), 1)
    columns.splice(columns.indexOf("comment"), 1)

    let text = columns.join(",") + "\n"
    for(let i = 0; i < data.length; i++) {
        // eslint-disable-next-line no-unused-vars
        let { sign, comment, ...others }  = data[i] 
        for(let item in others) {
            text += `${others[item]},`
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