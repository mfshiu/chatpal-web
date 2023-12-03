const SILENCE_THRESHOLD = 250;
const RMS_THRESHOLD = 0.03;

class VoiceProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
        this.silenceCount = 0;
        this.isSpeaking = false;
        this.buffer = [];
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
                this.isSpeaking = true;

                input.forEach(channel => {
                    // For simplicity, just taking the first channel
                    this.buffer.push(...channel);
                });

                this.silenceCount = 0;    
                if (this.buffer.length >= 44100) {            
                    this.port.postMessage({ speaking: true, buffer: this.buffer });
                    console.log("speaking: true, buffer: ", this.buffer.length);
                    this.buffer = [];
                }
            }
            else {
                if (this.isSpeaking) {
                    this.silenceCount++;
                    if (this.silenceCount > SILENCE_THRESHOLD) {
                        this.isSpeaking = false;
                        console.log("speaking:", this.isSpeaking);
                        this.port.postMessage({ speaking: false });
                    }
                    // console.log("speaking:", this.isSpeaking, ", silenceCount:", this.silenceCount);
                }
            }
        }

        return true;
    }
}

registerProcessor('voice-processor', VoiceProcessor);
