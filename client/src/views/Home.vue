<style>
    div {
        margin: 10px 0;
    }
    canvas {
        -moz-box-shadow: 0px 0px 2px #333333;
        -webkit-box-shadow: 0px 0px 2px #333333;
        box-shadow: 0px 0px 2px #333333;
        border-radius: 12px;
    }
    .clear {
        margin-top: -24px;
    }
</style>

<template>
    <div id="mnist">
        <h3>手写数字识别 (by 潮戒)</h3>
        <img alt="GitHub stars"
             src="https://img.shields.io/github/stars/zhuzhezhe/mini_mnist"
             href="https://github.com/zhuzhezhe/mini_sms_classify">
        <a-row>
            <a-col :span="8" :offset="8">
                <div class="canvas-container">
                    <canvas
                            width="280"
                            height="280"
                            ref="canvas"
                            @mousedown="onMouseDown"
                            @mousemove="onMouseMove"
                            @mouseup="drawEnd"
                            @mouseleave="drawEnd"
                            @touchstart="onMouseDown"
                            @touchmove="onMouseMove"
                            @touchend="drawEnd"
                    />
                </div>
            </a-col>
        </a-row>

        <a-button class="clear" type="primary" @click="clear">clear</a-button>
        <div>
            <p class="result">识别结果：{{result}}</p>
        </div>
    </div>
</template>

<script>

    import {getCoordinates, reduceData} from "../utils";
    import axios from 'axios'

    export default {
        name: "home",
        data() {
            return {
                result: "",
                loading: true,
                modelLoadingProgress: 0
            };
        },
        created() {
            this.loading = false;
        },
        methods: {
            onMouseDown(e) {
                e.preventDefault();
                this.drawLine(...getCoordinates(e));
                this.listenMouseMove = true;
            },
            onMouseMove(e) {
                e.preventDefault();
                console.log("onMouseMove");
                if (!this.listenMouseMove) return;
                this.drawLine(...getCoordinates(e));
            },
            drawEnd() {
                if (!this.listenMouseMove) return;
                this.listenMouseMove = false;
                delete this.previousX;
                delete this.previousY;
                this.predict();
            },
            drawLine(x, y) {
                const {canvas} = this.$refs;
                const ctx = canvas.getContext("2d");
                ctx.lineWidth = 20;
                ctx.lineJoin = ctx.lineCap = "round";
                ctx.strokeStyle = "#393E46";
                ctx.beginPath();
                const {previousX, previousY} = this;
                if (previousX !== undefined) {
                    ctx.moveTo(previousX, previousY);
                } else {
                    ctx.moveTo(x, y);
                }
                ctx.lineTo(x, y);
                ctx.stroke();
                this.previousX = x;
                this.previousY = y;
            },
            predict() {
                const {canvas} = this.$refs;
                const ctx = canvas.getContext("2d");
                const data = reduceData(ctx.getImageData(0, 0, 280, 280).data);
                const inputData = {
                    input: new Float32Array(data)
                };
                console.log(inputData);

                const path = 'http://localhost:5000/predict?figure=' + JSON.stringify(inputData);
                axios.get(path)
                    .then((res) => {
                        this.result = res.data.label;
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        console.error(error);
                    });

                // this.models.predict(inputData).then(outputData => {
                //     var max = outputData.output.reduce((a, b) => Math.max(a, b), 0);
                //     console.log(outputData.output.indexOf(max));
                //     this.result = outputData.output.indexOf(max);
                // });
            },
            clear() {
                const {canvas} = this.$refs;
                const ctx = canvas.getContext("2d");
                ctx.clearRect(0, 0, 280, 280);
                this.result = "";
            }
        }
    };
</script>
