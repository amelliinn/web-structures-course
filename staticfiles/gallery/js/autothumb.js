import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// Получаем ссылки на элементы DOM
const fileInput = document.querySelector('input[type="file"]');
const previewContainer = document.getElementById('preview-container');
const hiddenInput = document.getElementById('id_image_data');
const submitBtn = document.getElementById('submit-btn');

// Следим за выбором файла
if (fileInput) {
    fileInput.addEventListener('change', function (e) {
        const file = e.target.files[0];
        if (file) {
            // Создаем временную ссылку на файл
            const url = URL.createObjectURL(file);
            generateThumbnail(url);
        }
    });
}

function generateThumbnail(modelUrl) {
    previewContainer.innerHTML = 'Генерация...';

    // Настройка сцены
    const width = 300;
    const height = 200;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xffffff); // Белый фон

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);

    // Создаем рендерер с возможностью сохранения буфера
    const renderer = new THREE.WebGLRenderer({
        antialias: true,
        preserveDrawingBuffer: true  // Важно для скриншота!
    });
    renderer.setSize(width, height);
    renderer.outputColorSpace = THREE.SRGBColorSpace;

    // Очищаем контейнер и добавляем canvas
    previewContainer.innerHTML = '';
    previewContainer.appendChild(renderer.domElement);

    // Добавляем освещение
    const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 1.5);
    dirLight.position.set(5, 10, 7);
    scene.add(dirLight);

    // Загружаем модель
    const loader = new GLTFLoader();
    loader.load(modelUrl,
        // Успешная загрузка
        (gltf) => {
            const model = gltf.scene;

            // Центрируем модель
            const box = new THREE.Box3().setFromObject(model);
            const center = box.getCenter(new THREE.Vector3());
            const size = box.getSize(new THREE.Vector3());
            const maxDim = Math.max(size.x, size.y, size.z);

            model.position.sub(center); // Перемещаем центр в (0,0,0)
            scene.add(model);

            // Настраиваем камеру
            const fov = camera.fov * (Math.PI / 180);
            let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2)) * 1.5;
            camera.position.set(cameraZ * 0.5, cameraZ * 0.5, cameraZ);
            camera.lookAt(0, 0, 0);

            // Рендерим один кадр
            renderer.render(scene, camera);

            // Делаем скриншот (конвертируем canvas в base64)
            const dataURL = renderer.domElement.toDataURL('image/jpeg', 0.8);

            // Сохраняем в скрытое поле
            hiddenInput.value = dataURL;

            // Разблокируем кнопку отправки
            submitBtn.disabled = false;
            submitBtn.innerHTML = "Загрузить в базу";

            console.log("Скриншот создан!");

            // Очищаем временную ссылку
            URL.revokeObjectURL(modelUrl);
        },
        // Прогресс загрузки (опционально)
        undefined,
        // Ошибка загрузки
        (err) => {
            console.error(err);
            previewContainer.innerHTML = 'Ошибка генерации превью';
        }
    );
}