<template>
    <keep-alive>
        <component :is="currentComponent"></component>
    </keep-alive>
</template>


<script>
import FirstPage from "./components/FirstPage.vue"
import SecondPage from "./components/SecondPage.vue"
import ThirdPage from "./components/ThirdPage.vue"
import FourthPage from "./components/FourthPage.vue"
export default {
    components: {
        FirstPage,
        SecondPage,
        ThirdPage,
        FourthPage
    },
    setup() {
        let currentComponent = FirstPage

        return {
            currentComponent
        }
    }
}
</script>

<style>

</style>