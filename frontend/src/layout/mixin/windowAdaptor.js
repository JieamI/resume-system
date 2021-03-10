export default {
    data() {
        const windowAdaptor = () => {
            let width = screen.width
            if(width < 1280) {
                let html = document.querySelector('html')
                let body = document.querySelector('body')
                let app = document.querySelector('#app')
                html.setAttribute('style', `overflow-y: hidden`)
                body.setAttribute('style', `overflow-y: hidden`)
                app.setAttribute('style', `width: 1280px`)
            }
        }
        return {
            windowAdaptor
        }
    },
    mounted() {
        this.windowAdaptor()
    }
}