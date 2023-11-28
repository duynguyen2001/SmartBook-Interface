<template>
    <div id="app">
        <div class="text-display">
            <template v-if="detailLevel === '1'">
                <slot name="less-detailed"></slot>
            </template>
            <template v-else-if="detailLevel === '2'">
                <slot name="summary"></slot>
            </template>
            <template v-else>
                <slot name="more-detailed"></slot>
            </template>
        </div>
        <div class="slider-container-container">
            <div class="slider-container">
                <input
                    type="range"
                    min="1"
                    max="3"
                    v-model="detailLevel"
                    class="slider"
                    @input="logValue"
                />
                <div class="slider-labels">
                    <span>Less Detailed</span>
                    <span>More Detailed</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            detailLevel: "2", // Default to normal detail
        };
    },
    methods: {
        logValue() {
            console.log(this.detailLevel);
        },
    },
};
</script>

<style>
#app {
    margin: auto;
}

.text-display {
    margin-top: 20px;
    padding: 10px;
}
.slider-container-container {
    display: flex;
    width: 100%;
    flex-flow: row-reverse;
}
.slider-container {
    display: flex;
    flex-direction: column;
    min-width: 200px;
    margin: auto;
    margin-right: 10px;
}

.slider-labels {
    display: flex;
    justify-content: space-between;
    width: 100%;
}

.slider-labels span {
    font-size: 12px;
    color: #666;
}

.slider {
    width: 100%;
    margin: 10px 0;
}
</style>
