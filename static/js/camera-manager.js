/**
 * Camera Manager - RehabSystem
 * Gestiona la captura de video de la cámara del paciente
 */

class CameraManager {
    constructor(videoElementId) {
        this.videoElement = document.getElementById(videoElementId);
        this.stream = null;
        this.isActive = false;
        this.isRecording = false;
        this.mediaRecorder = null;
        this.recordedChunks = [];
        this.recordingStartTime = null;
    }

    /**
     * Iniciar la cámara
     */
    async startCamera() {
        try {
            // Solicitar acceso a la cámara
            const constraints = {
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: 'user'
                },
                audio: false
            };

            this.stream = await navigator.mediaDevices.getUserMedia(constraints);
            
            // Asignar el stream al elemento video
            if (this.videoElement) {
                this.videoElement.srcObject = this.stream;
                this.videoElement.play();
                this.isActive = true;
                
                console.log('✅ Cámara iniciada correctamente');
                this.showNotification('Cámara conectada', 'success');
                
                // Actualizar UI
                this.updateUI(true);
            }
        } catch (error) {
            console.error('❌ Error al acceder a la cámara:', error);
            this.handleCameraError(error);
        }
    }

    /**
     * Detener la cámara
     */
    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
            this.isActive = false;
            
            if (this.videoElement) {
                this.videoElement.srcObject = null;
            }
            
            console.log('🛑 Cámara detenida');
            this.showNotification('Cámara desconectada', 'info');
            
            // Actualizar UI
            this.updateUI(false);
        }
    }

    /**
     * Alternar cámara (encender/apagar)
     */
    toggleCamera() {
        if (this.isActive) {
            this.stopCamera();
        } else {
            this.startCamera();
        }
    }

    /**
     * Capturar foto de la cámara
     */
    captureSnapshot() {
        if (!this.isActive || !this.videoElement) {
            this.showNotification('La cámara no está activa', 'warning');
            return null;
        }

        const canvas = document.createElement('canvas');
        canvas.width = this.videoElement.videoWidth;
        canvas.height = this.videoElement.videoHeight;
        
        const ctx = canvas.getContext('2d');
        ctx.drawImage(this.videoElement, 0, 0);
        
        // Convertir a blob
        return canvas.toDataURL('image/jpeg', 0.8);
    }

    /**
     * Guardar foto en el servidor
     */
    async saveSnapshot(imageData, notes = '') {
        try {
            const response = await fetch('/api/save-snapshot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image: imageData,
                    patient_id: null, // Puedes agregar ID del paciente si está disponible
                    notes: notes
                })
            });

            const result = await response.json();
            
            if (result.success) {
                this.showNotification(`✅ Foto guardada: ${result.filename}`, 'success');
                return result;
            } else {
                this.showNotification(`❌ Error: ${result.message}`, 'danger');
                return null;
            }
        } catch (error) {
            console.error('Error al guardar foto:', error);
            this.showNotification('❌ Error al guardar foto en el servidor', 'danger');
            return null;
        }
    }

    /**
     * Iniciar grabación de video
     */
    startRecording() {
        if (!this.isActive || !this.stream) {
            this.showNotification('La cámara no está activa', 'warning');
            return;
        }

        try {
            // Crear MediaRecorder
            this.mediaRecorder = new MediaRecorder(this.stream, {
                mimeType: 'video/webm;codecs=vp9'
            });

            this.recordedChunks = [];
            this.recordingStartTime = Date.now();

            // Evento cuando hay datos disponibles
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.recordedChunks.push(event.data);
                }
            };

            // Evento cuando termina la grabación
            this.mediaRecorder.onstop = () => {
                const blob = new Blob(this.recordedChunks, { type: 'video/webm' });
                const duration = Math.floor((Date.now() - this.recordingStartTime) / 1000);
                this.saveRecording(blob, duration);
            };

            // Iniciar grabación
            this.mediaRecorder.start();
            this.isRecording = true;

            console.log('🔴 Grabación iniciada');
            this.showNotification('🔴 Grabación iniciada', 'info');
            this.updateRecordingUI(true);

        } catch (error) {
            console.error('Error al iniciar grabación:', error);
            this.showNotification('❌ Error al iniciar grabación', 'danger');
        }
    }

    /**
     * Detener grabación de video
     */
    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;

            console.log('⏹️ Grabación detenida');
            this.showNotification('⏹️ Grabación detenida, guardando...', 'info');
            this.updateRecordingUI(false);
        }
    }

    /**
     * Guardar grabación en el servidor
     */
    async saveRecording(blob, duration) {
        try {
            const formData = new FormData();
            formData.append('video', blob, 'recording.webm');
            formData.append('patient_id', ''); // Agregar ID del paciente si está disponible
            formData.append('notes', '');
            formData.append('duration', duration);

            const response = await fetch('/api/save-video', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (result.success) {
                this.showNotification(`✅ Video guardado: ${result.filename} (${duration}s)`, 'success');
                return result;
            } else {
                this.showNotification(`❌ Error: ${result.message}`, 'danger');
                return null;
            }
        } catch (error) {
            console.error('Error al guardar video:', error);
            this.showNotification('❌ Error al guardar video en el servidor', 'danger');
            return null;
        }
    }

    /**
     * Actualizar UI de grabación
     */
    updateRecordingUI(isRecording) {
        const btnRecord = document.getElementById('btnRecordVideo');
        const recordingIndicator = document.getElementById('recordingIndicator');
        
        if (btnRecord) {
            if (isRecording) {
                btnRecord.innerHTML = '<i class="fas fa-stop"></i> Detener Grabación';
                btnRecord.classList.remove('btn-danger');
                btnRecord.classList.add('btn-warning');
            } else {
                btnRecord.innerHTML = '<i class="fas fa-circle"></i> Grabar Video';
                btnRecord.classList.remove('btn-warning');
                btnRecord.classList.add('btn-danger');
            }
        }
        
        if (recordingIndicator) {
            recordingIndicator.style.display = isRecording ? 'flex' : 'none';
        }
    }

    /**
     * Manejar errores de cámara
     */
    handleCameraError(error) {
        let message = 'Error al acceder a la cámara';
        
        if (error.name === 'NotAllowedError') {
            message = 'Permiso de cámara denegado. Por favor, permite el acceso.';
        } else if (error.name === 'NotFoundError') {
            message = 'No se encontró ninguna cámara en el dispositivo.';
        } else if (error.name === 'NotReadableError') {
            message = 'La cámara está siendo usada por otra aplicación.';
        }
        
        this.showNotification(message, 'danger');
    }

    /**
     * Actualizar interfaz de usuario
     */
    updateUI(isActive) {
        const btnToggle = document.getElementById('btnToggleCamera');
        const btnCapture = document.getElementById('btnCaptureSnapshot');
        const btnRecord = document.getElementById('btnRecordVideo');
        const statusBadge = document.getElementById('cameraStatus');
        const placeholder = document.getElementById('cameraPlaceholder');
        
        if (btnToggle) {
            if (isActive) {
                btnToggle.innerHTML = '<i class="fas fa-video-slash"></i> Detener Cámara';
                btnToggle.classList.remove('btn-success');
                btnToggle.classList.add('btn-danger');
            } else {
                btnToggle.innerHTML = '<i class="fas fa-video"></i> Iniciar Cámara';
                btnToggle.classList.remove('btn-danger');
                btnToggle.classList.add('btn-success');
            }
        }
        
        if (btnCapture) {
            btnCapture.disabled = !isActive;
        }
        
        if (btnRecord) {
            btnRecord.disabled = !isActive;
        }
        
        if (statusBadge) {
            if (isActive) {
                statusBadge.textContent = 'Conectado';
                statusBadge.classList.remove('bg-secondary');
                statusBadge.classList.add('bg-success');
            } else {
                statusBadge.textContent = 'Desconectado';
                statusBadge.classList.remove('bg-success');
                statusBadge.classList.add('bg-secondary');
            }
        }
        
        if (placeholder) {
            placeholder.style.display = isActive ? 'none' : 'flex';
        }
    }

    /**
     * Mostrar notificación
     */
    showNotification(message, type = 'info') {
        // Crear elemento de notificación
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remover después de 3 segundos
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    /**
     * Verificar soporte de cámara
     */
    static checkCameraSupport() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            console.error('❌ Tu navegador no soporta acceso a cámara');
            return false;
        }
        return true;
    }

    /**
     * Listar cámaras disponibles
     */
    static async getAvailableCameras() {
        try {
            const devices = await navigator.mediaDevices.enumerateDevices();
            return devices.filter(device => device.kind === 'videoinput');
        } catch (error) {
            console.error('Error al listar cámaras:', error);
            return [];
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Verificar soporte
    if (!CameraManager.checkCameraSupport()) {
        alert('Tu navegador no soporta acceso a cámara. Usa Chrome, Firefox o Edge.');
        return;
    }

    // Crear instancia del gestor de cámara
    const cameraManager = new CameraManager('patientCamera');

    // Botón para iniciar/detener cámara
    const btnToggle = document.getElementById('btnToggleCamera');
    if (btnToggle) {
        btnToggle.addEventListener('click', () => {
            cameraManager.toggleCamera();
        });
    }

    // Botón para capturar foto
    const btnCapture = document.getElementById('btnCaptureSnapshot');
    if (btnCapture) {
        btnCapture.addEventListener('click', async () => {
            const snapshot = cameraManager.captureSnapshot();
            if (snapshot) {
                console.log('📸 Foto capturada');
                
                // Obtener notas si existen
                const notesElement = document.getElementById('sessionNotes');
                const notes = notesElement ? notesElement.value : '';
                
                // Guardar en el servidor
                await cameraManager.saveSnapshot(snapshot, notes);
            }
        });
    }

    // Botón para grabar video
    const btnRecord = document.getElementById('btnRecordVideo');
    if (btnRecord) {
        btnRecord.addEventListener('click', () => {
            if (cameraManager.isRecording) {
                cameraManager.stopRecording();
            } else {
                cameraManager.startRecording();
            }
        });
    }

    // Detener cámara y grabación al salir de la página
    window.addEventListener('beforeunload', () => {
        if (cameraManager.isRecording) {
            cameraManager.stopRecording();
        }
        cameraManager.stopCamera();
    });
});
