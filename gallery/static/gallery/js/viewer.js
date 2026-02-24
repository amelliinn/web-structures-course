import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
// НОВЫЙ ИМПОРТ: Контроллер орбиты
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

export function loadModel(containerId, modelUrl) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // 1. Сцена
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf5f5f5); // Светло-серый фон

    // 2. Камера
    const camera = new THREE.PerspectiveCamera(
        45, 
        container.clientWidth / container.clientHeight, 
        0.1, 
        1000
    );

    // 3. Рендерер
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.outputColorSpace = THREE.SRGBColorSpace; // ВАЖНО для GLTF!

    container.innerHTML = '';
    container.appendChild(renderer.domElement);

    // 4. Контроль (OrbitControls)
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = 0.5;
    controls.maxDistance = 20;

    // 5. Окружение (Свет) - вместо старых лампочек
    const pmremGenerator = new THREE.PMREMGenerator(renderer);
    scene.environment = pmremGenerator.fromScene(new RoomEnvironment()).texture;

    // 6. Загрузка модели
    const loader = new GLTFLoader();
    let loadedModel = null;

    loader.load(
        modelUrl,
        (gltf) => {
            loadedModel = gltf.scene;
            fitCameraToObject(camera, loadedModel, controls);
            scene.add(loadedModel);
        },
        undefined,
        (error) => {
            console.error('Ошибка загрузки:', error);
            container.innerHTML = '❌ Error';
        }
    );

    // 7. Анимация
    function animate() {
        requestAnimationFrame(animate);
        controls.update(); // ОБНОВЛЯЕМ КОНТРОЛЛЕР
        renderer.render(scene, camera);
    }
    animate();

    // Resize handler
    window.addEventListener('resize', () => {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });
}

// Вспомогательная функция центровки (обновленная с controls)
function fitCameraToObject(camera, object, controls) {
    const boundingBox = new THREE.Box3();
    boundingBox.setFromObject(object);

    const center = boundingBox.getCenter(new THREE.Vector3());
    const size = boundingBox.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);

    // Сдвигаем модель в центр
    object.position.x = -center.x;
    object.position.y = -center.y;
    object.position.z = -center.z;

    // Ставим камеру
    const fov = camera.fov * (Math.PI / 180);
    let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2)) * 1.5;
    
    camera.position.set(cameraZ, cameraZ * 0.5, cameraZ);
    camera.lookAt(0, 0, 0);

    // ВАЖНО: Обновляем цель контроллера, чтобы вращение было вокруг центра модели
    controls.target.set(0, 0, 0);
    controls.update();
    
    camera.updateProjectionMatrix();
}