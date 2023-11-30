const SILENCE_THRESHOLD = 250;
const RMS_THRESHOLD = 0.03;

class AudioProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
        this.isSpeaking = false;
        this.silenceCount = 0;
        this.speakingDetectedCallback = () => {}; // Placeholder for a callback
    }

    process(inputs, outputs, parameters) {
        const input = inputs[0];

        // Assuming mono audio (one channel)
        if (input && input.length > 0) {
            const channelData = input[0];

            // Calculate the root mean square (RMS) of the audio frame
            let sum = 0;
            for (let i = 0; i < channelData.length; i++) {
                sum += channelData[i] * channelData[i];
            }

            let rms = Math.sqrt(sum / channelData.length);
            if (rms > RMS_THRESHOLD) {
                this.silenceCount = 0;               
                if (!this.isSpeaking) {
                    this.isSpeaking = true;
                    this.port.postMessage({ speaking: true });
                }
            }
            else {
                this.silenceCount++;
                if (this.isSpeaking) {
                    if (this.silenceCount > SILENCE_THRESHOLD) {
                        this.isSpeaking = false;
                        this.port.postMessage({ speaking: false });
                    }
                }
            }
        }

        return true;
    }
}

registerProcessor('audio-processor', AudioProcessor);
