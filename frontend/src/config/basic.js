const Config = {
	//前端的域名（必须是域名，不能是ip:port形式），注意域名最后不要加斜杠
	FrontDomain: process.env.VUE_APP_FRONT_DOMAIN ? process.env.VUE_APP_FRONT_DOMAIN : "https://token.vaiwan.com",
	//后端域名（可以是ip:port形式），注意最后不要加斜杠
	BackendDomain: process.env.VUE_APP_BACKEND_DOMAIN ? process.env.VUE_APP_BACKEND_DOMAIN : "http://localhost:8000/api",
}

export default Config