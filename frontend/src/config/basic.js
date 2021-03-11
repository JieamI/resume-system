const Config = {
	//前端的域名（必须是域名，不能是ip:port形式），注意域名最后不要加斜杠
	FrontDomain: process.env.VUE_APP_FRONT_DOMAIN ? process.env.VUE_APP_FRONT_DOMAIN : "https://recruit.itoken.team",
	//后端域名（可以是ip:port形式），注意最后不要加斜杠
	BackendDomain: process.env.VUE_APP_BACKEND_DOMAIN ? process.env.VUE_APP_BACKEND_DOMAIN : "https://recruit.itoken.team/api",
	// //钉钉AppId
	DingAppId: "dingoalrnidom4p3khixr0",
	// //钉钉AppSecret
	DingAppSecret: "QNDiNQbWbJfiLLuTkR523G8VDRT79Geo-2VplHBEZVJqOKQ62mE8v03lySvPRpoT",
	//钉钉AppId
	// DingAppId: "dingoapm6ohzqxmd1kzesi",
	//钉钉AppSecret
	// DingAppSecret: "ccBS_06R4SFXSevbHCKrQco2aQzLVGavH3AkAjeUWuQwt3KK-RxmI5Nw_PK9HLe6"
}

// Config.FrontDomain = "http://token.vaiwan.com/login"

export default Config