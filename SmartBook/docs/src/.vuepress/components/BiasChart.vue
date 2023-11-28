<template>
    <div class="bias-container-container">
        <div class="bias-container">
            <div
                class="rectangle"
                :style="{ backgroundColor: getColor('Left') }"
            >
                L
            </div>
            <div
                class="rectangle"
                :style="{ backgroundColor: getColor('Lean Left') }"
            >
                L
            </div>
            <div
                class="rectangle"
                :style="{ backgroundColor: getColor('Center') }"
            >
                C
            </div>
            <div
                class="rectangle"
                :style="{ backgroundColor: getColor('Lean Right') }"
            >
                R
            </div>
            <div
                class="rectangle"
                :style="{ backgroundColor: getColor('Right') }"
            >
                R
            </div>
        </div>
        <div>Bias: {{ this.bias ? this.bias : "" }}</div>
        <br />
    </div>
</template>

<script>
export default {
    name: "BiasChart",
    props: {
        bias: {
            type: String,
            default: "Center",
        },
    },
    methods: {
        getColor(position) {
            const colors = {
                Left: "blue",
                "Lean Left": "lightblue",
                Center: "green",
                "Lean Right": "lightcoral", // 'light red' is not a standard color, lightcoral is a light red color
                Right: "red",
            };
            if (this.bias === position) return colors[position];
            else return "grey";
        },
    },
};
</script>

<style scoped>
.bias-container-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    row-gap: 0;
}
.bias-container {
    display: flex;
    justify-content: center;
    align-items: center;
}

.rectangle {
    width: 20px;
    height: 30px;
    color: white;
    display: flex;
    justify-content: Center;
    align-items: Center;
    margin: 0 2px;
    font-weight: bold;
    font-size: 1.2em;
}
</style>
