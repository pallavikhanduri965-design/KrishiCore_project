/**
 * FasalNirnay AI - Voice Interface Handler
 * Provides seamless Speech-to-Text & Text-to-Speech using browser Web Speech API & Backend Service
 */
const VoiceHandler = {
    isRecording: false,
    recognition: null,
    audioPlayer: new Audio(),
    
    init() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            
            this.recognition.onstart = () => {
                this.isRecording = true;
                this.updateMicUI(true);
            };

            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.handleSpeechResult(transcript);
            };

            this.recognition.onerror = (event) => {
                console.warn("Speech recognition error:", event.error);
                this.stopRecording();
            };

            this.recognition.onend = () => {
                this.stopRecording();
            };
        } else {
            console.log("Web Speech Recognition not supported in this browser. Fallback enabled.");
        }
    },

    toggleRecording() {
        if (this.isRecording) {
            this.stopRecording();
        } else {
            this.startRecording();
        }
    },

    startRecording() {
        const langMap = { en: "en-IN", hi: "hi-IN", pa: "pa-IN", mr: "mr-IN" };
        const langCode = langMap[State.profile.language] || "hi-IN";

        if (this.recognition) {
            try {
                this.recognition.lang = langCode;
                this.recognition.start();
            } catch (e) {
                console.warn("Recognition start error:", e);
                this.simulateVoicePrompt();
            }
        } else {
            this.simulateVoicePrompt();
        }
    },

    stopRecording() {
        this.isRecording = false;
        if (this.recognition) {
            try { this.recognition.stop(); } catch(e) {}
        }
        this.updateMicUI(false);
    },

    simulateVoicePrompt() {
        this.updateMicUI(true);
        setTimeout(() => {
            const prompts = {
                hi: "क्या मुझे अभी गेहूं बेचना चाहिए या इंतजार करना चाहिए?",
                en: "What is the best mandi to sell wheat this week?",
                pa: "ਕੀ ਮੈਨੂੰ ਹੁਣੇ ਕਣਕ ਵੇਚਣੀ ਚਾਹੀਦੀ ਹੈ ਜਾਂ ਉਡੀਕ ਕਰਨੀ ਚਾਹੀਦੀ ਹੈ?",
                mr: "मी आता गहू विकावा की वाट पहावी?"
            };
            const sample = prompts[State.profile.language] || prompts.hi;
            this.handleSpeechResult(sample);
            this.updateMicUI(false);
        }, 2200);
    },

    async handleSpeechResult(transcript) {
        if (!transcript) return;
        
        // Add user message to chat state
        State.chatHistory.push({
            sender: "user",
            text: transcript,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        });

        // Trigger UI update
        if (typeof window.renderVoiceChat === 'function') {
            window.renderVoiceChat();
        }

        // Fetch AI Response
        const res = await ApiService.sendChatQuery(transcript);
        
        // Add assistant message
        State.chatHistory.push({
            sender: "assistant",
            text: res.answer,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            source: res.source
        });

        if (typeof window.renderVoiceChat === 'function') {
            window.renderVoiceChat();
        }

        // Auto speak response
        this.speakText(res.answer);
    },

    async speakText(text) {
        const langMap = { en: "en-IN", hi: "hi-IN", pa: "pa-IN", mr: "mr-IN" };
        const langCode = langMap[State.profile.language] || "hi-IN";

        // Try backend TTS first
        const ttsRes = await ApiService.textToSpeech(text, langCode);
        if (ttsRes && ttsRes.audio_base64 && ttsRes.audio_base64.length > 50) {
            try {
                this.audioPlayer.src = `data:audio/${ttsRes.format || 'mp3'};base64,${ttsRes.audio_base64}`;
                await this.audioPlayer.play();
                return;
            } catch (err) {
                console.warn("Backend audio playback error:", err);
            }
        }

        // Fallback to Web Speech Synthesis API
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = langCode;
            utterance.rate = 0.95;
            utterance.pitch = 1.0;
            window.speechSynthesis.speak(utterance);
        }
    },

    updateMicUI(recording) {
        const micBtn = document.getElementById('voice-mic-btn');
        const micPulse = document.getElementById('voice-mic-pulse');
        const micStatus = document.getElementById('voice-mic-status');

        if (micBtn) {
            if (recording) {
                micBtn.classList.add('bg-red-600', 'scale-110');
                micBtn.classList.remove('bg-emerald-700');
                if (micPulse) micPulse.classList.remove('hidden');
                if (micStatus) micStatus.innerText = State.profile.language === 'hi' ? "सुन रहे हैं... बोलिए" : "Listening... Speak now";
            } else {
                micBtn.classList.remove('bg-red-600', 'scale-110');
                micBtn.classList.add('bg-emerald-700');
                if (micPulse) micPulse.classList.add('hidden');
                if (micStatus) micStatus.innerText = State.t('tapToSpeak');
            }
        }
    }
};

window.VoiceHandler = VoiceHandler;
