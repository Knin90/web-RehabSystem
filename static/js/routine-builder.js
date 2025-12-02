// Base de datos de ejercicios
const exerciseDatabase = [
    { id: 1, name: 'Flexiones de rodilla', category: 'lower', duration: 5, calories: 25, reps: '3x15', difficulty: 'easy' },
    { id: 2, name: 'Elevaciones de pierna', category: 'lower', duration: 5, calories: 30, reps: '3x12', difficulty: 'medium' },
    { id: 3, name: 'Estiramientos lumbares', category: 'lower', duration: 3, calories: 15, reps: '4x30seg', difficulty: 'easy' },
    { id: 4, name: 'Rotación de hombros', category: 'upper', duration: 4, calories: 20, reps: '3x10', difficulty: 'easy' },
    { id: 5, name: 'Flexiones de brazo', category: 'upper', duration: 6, calories: 40, reps: '3x8', difficulty: 'hard' },
    { id: 6, name: 'Plancha abdominal', category: 'core', duration: 3, calories: 25, reps: '3x30seg', difficulty: 'medium' },
    { id: 7, name: 'Sentadillas asistidas', category: 'lower', duration: 7, calories: 50, reps: '3x12', difficulty: 'medium' },
    { id: 8, name: 'Puente de glúteos', category: 'lower', duration: 5, calories: 35, reps: '3x15', difficulty: 'easy' },
    { id: 9, name: 'Estiramiento cuádriceps', category: 'lower', duration: 3, calories: 10, reps: '2x30seg', difficulty: 'easy' },
    { id: 10, name: 'Rotación de tronco', category: 'core', duration: 4, calories: 20, reps: '3x12', difficulty: 'easy' },
    { id: 11, name: 'Press de hombros', category: 'upper', duration: 6, calories: 45, reps: '3x10', difficulty: 'hard' },
    { id: 12, name: 'Zancadas alternas', category: 'lower', duration: 8, calories: 55, reps: '3x10', difficulty: 'hard' }
];

let selectedExercises = [];
let currentFilter = 'all';

function openRoutineBuilder() {
    const modal = new bootstrap.Modal(document.getElementById('routineBuilderModal'));
    modal.show();
    loadExerciseLibrary();
    resetBuilder();
}

function loadExerciseLibrary(filter = 'all') {
    currentFilter = filter;
    const library = document.getElementById('exerciseLibrary');
    const searchTerm = document.getElementById('exerciseSearch').value.toLowerCase();
    
    let exercises = filter === 'all' ? exerciseDatabase : exerciseDatabase.filter(e => e.category === filter);
    
    if (searchTerm) {
        exercises = exercises.filter(e => e.name.toLowerCase().includes(searchTerm));
    }
    
    library.innerHTML = exercises.map(exercise => `
        <div class="exercise-item" draggable="true" data-exercise-id="${exercise.id}">
            <div class="d-flex justify-content-between align-items-start mb-2">
                <div class="flex-grow-1">
                    <strong class="d-block">${exercise.name}</strong>
                    <small class="text-muted">${exercise.reps} • ${exercise.duration} min</small>
                </div>
                <button class="btn btn-sm btn-primary" onclick="addExercise(${exercise.id})" title="Agregar">
                    <i class="fas fa-plus"></i>
                </button>
            </div>
            <div class="d-flex gap-2">
                <span class="exercise-badge badge-${exercise.category}">${getCategoryName(exercise.category)}</span>
                <span class="badge bg-secondary">${exercise.calories} kcal</span>
            </div>
        </div>
    `).join('');
    
    setupDragAndDrop();
}

function filterExercises(category) {
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    loadExerciseLibrary(category);
}

function addExercise(exerciseId) {
    const exercise = exerciseDatabase.find(e => e.id === exerciseId);
    if (!exercise) return;
    
    if (selectedExercises.find(e => e.id === exerciseId)) {
        showToast('⚠️ Este ejercicio ya está en la rutina', 'warning');
        return;
    }
    
    selectedExercises.push({...exercise, order: selectedExercises.length + 1});
    updateRoutineBuilder();
    showToast(`✅ ${exercise.name} agregado`, 'success');
    triggerConfetti();
}

function removeExercise(exerciseId) {
    selectedExercises = selectedExercises.filter(e => e.id !== exerciseId);
    updateRoutineBuilder();
}

function updateRoutineBuilder() {
    const container = document.getElementById('selectedExercises');
    const placeholder = document.querySelector('.drop-zone-placeholder');
    
    if (selectedExercises.length === 0) {
        placeholder.style.display = 'block';
        container.innerHTML = '';
    } else {
        placeholder.style.display = 'none';
        container.innerHTML = selectedExercises.map((exercise, index) => `
            <div class="selected-exercise" data-exercise-id="${exercise.id}">
                <span class="drag-handle"><i class="fas fa-grip-vertical"></i></span>
                <div class="exercise-info">
                    <strong>${index + 1}. ${exercise.name}</strong>
                    <div class="small text-muted">${exercise.reps} • ${exercise.duration} min • ${exercise.calories} kcal</div>
                </div>
                <div class="exercise-controls">
                    <button class="btn btn-sm btn-outline-danger" onclick="removeExercise(${exercise.id})" title="Eliminar">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('');
    }
    
    updateStats();
    updateAISuggestions();
}

function updateStats() {
    const totalDuration = selectedExercises.reduce((sum, e) => sum + e.duration, 0);
    const totalCalories = selectedExercises.reduce((sum, e) => sum + e.calories, 0);
    const intensity = totalCalories > 200 ? 'Alta' : totalCalories > 100 ? 'Media' : 'Baja';
    
    document.getElementById('exerciseCount').textContent = `${selectedExercises.length} ejercicio${selectedExercises.length !== 1 ? 's' : ''}`;
    document.getElementById('totalDuration').textContent = `${totalDuration} min`;
    document.getElementById('totalCalories').textContent = `${totalCalories} kcal`;
    document.getElementById('intensityLevel').textContent = intensity;
    
    const intensityEl = document.getElementById('intensityLevel');
    intensityEl.className = intensity === 'Alta' ? 'text-danger' : intensity === 'Media' ? 'text-warning' : 'text-success';
}

function updateAISuggestions() {
    const suggestions = document.getElementById('aiSuggestions');
    
    if (selectedExercises.length === 0) {
        suggestions.innerHTML = '<small class="text-muted">Agrega ejercicios para recibir recomendaciones inteligentes...</small>';
        return;
    }
    
    const categories = [...new Set(selectedExercises.map(e => e.category))];
    const totalDuration = selectedExercises.reduce((sum, e) => sum + e.duration, 0);
    const avgDifficulty = selectedExercises.filter(e => e.difficulty === 'hard').length;
    
    let tips = [];
    
    if (totalDuration < 15) {
        tips.push('💡 Sesión corta detectada. Considera agregar 2-3 ejercicios más para alcanzar 20-30 minutos.');
    } else if (totalDuration > 45) {
        tips.push('⚠️ Sesión muy larga. Podría ser agotadora para pacientes en rehabilitación.');
    }
    
    if (categories.length === 1) {
        tips.push('🎯 Rutina enfocada en una zona. Considera agregar variedad para trabajo integral.');
    }
    
    if (selectedExercises.length < 4) {
        tips.push('📊 Una rutina efectiva suele tener 5-7 ejercicios diferentes.');
    }
    
    if (avgDifficulty > selectedExercises.length / 2) {
        tips.push('💪 Alta intensidad detectada. Asegúrate que sea apropiada para el paciente.');
    }
    
    if (tips.length === 0) {
        tips.push('✅ ¡Rutina bien balanceada! Duración y variedad óptimas.');
    }
    
    suggestions.innerHTML = tips.map(tip => `<div class="ai-tip">${tip}</div>`).join('');
}

function saveRoutine() {
    const name = document.getElementById('routineName').value.trim();
    const category = document.getElementById('routineCategory').value;
    const difficulty = document.getElementById('routineDifficulty').value;
    
    if (!name) {
        showToast('⚠️ Ingresa un nombre para la rutina', 'warning');
        document.getElementById('routineName').focus();
        return;
    }
    
    if (selectedExercises.length === 0) {
        showToast('⚠️ Agrega al menos un ejercicio', 'warning');
        return;
    }
    
    const btn = event.target;
    const originalHTML = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Guardando...';
    btn.disabled = true;
    
    setTimeout(() => {
        const totalDuration = selectedExercises.reduce((sum, e) => sum + e.duration, 0);
        const totalCalories = selectedExercises.reduce((sum, e) => sum + e.calories, 0);
        
        triggerSuccessAnimation();
        
        setTimeout(() => {
            showToast(`🎉 Rutina "${name}" creada exitosamente!`, 'success');
            bootstrap.Modal.getInstance(document.getElementById('routineBuilderModal')).hide();
            
            setTimeout(() => location.reload(), 1500);
        }, 1000);
    }, 1500);
}

function resetBuilder() {
    selectedExercises = [];
    document.getElementById('routineName').value = '';
    document.getElementById('routineCategory').value = 'general';
    document.getElementById('routineDifficulty').value = 'medium';
    updateRoutineBuilder();
}

function getCategoryName(category) {
    const names = {
        'upper': 'Superior',
        'lower': 'Inferior',
        'core': 'Core',
        'cardio': 'Cardio',
        'general': 'General'
    };
    return names[category] || category;
}

function setupDragAndDrop() {
    document.querySelectorAll('.exercise-item').forEach(item => {
        item.addEventListener('dragstart', (e) => {
            e.target.classList.add('dragging');
            e.dataTransfer.effectAllowed = 'copy';
            e.dataTransfer.setData('exerciseId', e.target.dataset.exerciseId);
        });
        
        item.addEventListener('dragend', (e) => {
            e.target.classList.remove('dragging');
        });
    });
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.classList.add('show'), 10);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function triggerConfetti() {
    const colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe'];
    for (let i = 0; i < 15; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.animationDelay = Math.random() * 0.5 + 's';
        document.body.appendChild(confetti);
        setTimeout(() => confetti.remove(), 2000);
    }
}

function triggerSuccessAnimation() {
    const overlay = document.createElement('div');
    overlay.className = 'success-overlay';
    overlay.innerHTML = '<div class="success-icon"><i class="fas fa-check-circle"></i></div>';
    document.body.appendChild(overlay);
    
    for (let i = 0; i < 50; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.background = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b'][Math.floor(Math.random() * 5)];
        confetti.style.animationDelay = Math.random() * 0.3 + 's';
        document.body.appendChild(confetti);
        setTimeout(() => confetti.remove(), 3000);
    }
    
    setTimeout(() => overlay.remove(), 2000);
}

// Inicializar cuando el modal se abre
setTimeout(() => {
    const dropZone = document.getElementById('routineDropZone');
    if (dropZone) {
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'copy';
            dropZone.classList.add('drag-over');
        });
        
        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('drag-over');
        });
        
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
            const exerciseId = parseInt(e.dataTransfer.getData('exerciseId'));
            if (exerciseId) addExercise(exerciseId);
        });
    }
    
    const searchInput = document.getElementById('exerciseSearch');
    if (searchInput) {
        searchInput.addEventListener('input', () => loadExerciseLibrary(currentFilter));
    }
}, 500);
