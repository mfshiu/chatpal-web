class AudioProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
        this.threshold = 0.02; // Define a threshold for voice detection
        this.isSpeaking = false;
        this.speakingDetectedCallback = () => {}; // Placeholder for a callback
    }

    process(inputs, outputs, parameters) {
        const input = inputs[0];
        const silence_count_threshold = 3
        let silence_count = 0

        // Assuming mono audio (one channel)
        if (input && input.length > 0) {
            const channelData = input[0];

            // Calculate the root mean square (RMS) of the audio frame
            let sum = 0;
            for (let i = 0; i < channelData.length; i++) {
                sum += channelData[i] * channelData[i];
            }
            let rms = Math.sqrt(sum / channelData.length);
            if (rms > this.threshold) {
                console.log("rms:", rms);
            }

            // Check if the RMS value exceeds the threshold
            if (rms > this.threshold && !this.isSpeaking) {
                this.isSpeaking = true;
                if (silence_count == 0) {
                    this.port.postMessage({ speaking: true });
                }
                silence_count = 0;
            } else if (rms <= this.threshold && this.isSpeaking) {
                this.isSpeaking = false;
                silence_count += 1;
                if (silence_count > silence_count_threshold) {
                    this.port.postMessage({ speaking: false });
                }
            }
        }

        return true;
    }
}

registerProcessor('audio-processor', AudioProcessor);
