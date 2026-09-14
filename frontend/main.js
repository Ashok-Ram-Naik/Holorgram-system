// Three.js Setup
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x000000); // Pitch black for hologram

// Main Camera
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 10;

// Renderer
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
container.appendChild(renderer.domElement);

// Lighting
const ambientLight = new THREE.AmbientLight(0x404040, 2); // Soft white light
scene.add(ambientLight);

const pointLight1 = new THREE.PointLight(0x00f3ff, 2, 50);
pointLight1.position.set(5, 5, 5);
scene.add(pointLight1);

const pointLight2 = new THREE.PointLight(0xff00f3, 2, 50);
pointLight2.position.set(-5, -5, 5);
scene.add(pointLight2);

// Objects Definition (10 Objects)
const objects = [];
const material = new THREE.MeshPhysicalMaterial({
    color: 0xffffff,
    metalness: 0.1,
    roughness: 0.2,
    transmission: 0.9, // glass-like
    thickness: 0.5,
    envMapIntensity: 1.0,
    clearcoat: 1.0,
    clearcoatRoughness: 0.1
});

// Wireframe material for sci-fi look
const wireframeMaterial = new THREE.LineBasicMaterial({ color: 0x00f3ff, transparent: true, opacity: 0.5 });

function createObject(geometry, name) {
    const mesh = new THREE.Mesh(geometry, material);
    const wireframe = new THREE.LineSegments(new THREE.WireframeGeometry(geometry), wireframeMaterial);
    mesh.add(wireframe);
    return { mesh, name };
}

// 1. Cube
objects.push(createObject(new THREE.BoxGeometry(3, 3, 3), "Cube"));
// 2. Sphere
objects.push(createObject(new THREE.SphereGeometry(2, 32, 32), "Sphere"));
// 3. Pyramid (Cone)
objects.push(createObject(new THREE.ConeGeometry(2, 3, 4), "Pyramid"));
// 4. Torus
objects.push(createObject(new THREE.TorusGeometry(1.5, 0.5, 16, 100), "Torus"));
// 5. Torus Knot
objects.push(createObject(new THREE.TorusKnotGeometry(1.2, 0.4, 100, 16), "DNA Knot"));
// 6. Dodecahedron
objects.push(createObject(new THREE.DodecahedronGeometry(2), "Dodecahedron"));
// 7. Icosahedron
objects.push(createObject(new THREE.IcosahedronGeometry(2), "Icosahedron"));
// 8. Cylinder
objects.push(createObject(new THREE.CylinderGeometry(1.5, 1.5, 3, 32), "Cylinder"));
// 9. Octahedron
objects.push(createObject(new THREE.OctahedronGeometry(2), "Octahedron"));
// 10. Ring
objects.push(createObject(new THREE.RingGeometry(1, 2, 32), "Ring"));

let currentObjectIndex = 0;
let currentObject = objects[currentObjectIndex].mesh;
scene.add(currentObject);

document.getElementById('object-display').innerText = objects[currentObjectIndex].name;

// State Variables
let isRotating = false;
let autoRotateSpeed = { x: 0.01, y: 0.02 };
let targetZoom = 10;
let isHologramMode = false;

// Hologram Cameras Setup
const holoCameras = [];
for (let i = 0; i < 4; i++) {
    const cam = new THREE.PerspectiveCamera(45, 1, 0.1, 1000);
    holoCameras.push(cam);
}

// Setup 4 views looking at origin from 4 sides
holoCameras[0].position.set(0, 0, 10); // Front (Bottom view)
holoCameras[1].position.set(10, 0, 0); // Right (Right view)
holoCameras[2].position.set(0, 0, -10); // Back (Top view)
holoCameras[3].position.set(-10, 0, 0); // Left (Left view)

holoCameras.forEach(cam => cam.lookAt(0, 0, 0));

// UI Button
document.getElementById('toggle-hologram').addEventListener('click', () => {
    isHologramMode = !isHologramMode;
    document.body.classList.toggle('hologram-mode', isHologramMode);
});

// Control Functions
window.rotateObject = function () {
    isRotating = true;
};

window.stopObject = function () {
    isRotating = false;
};

window.zoomObject = function () {
    // Toggle zoom in and out
    targetZoom = targetZoom === 10 ? 5 : 10;
};

window.nextObject = function () {
    scene.remove(currentObject);
    currentObjectIndex = (currentObjectIndex + 1) % objects.length;
    currentObject = objects[currentObjectIndex].mesh;
    currentObject.rotation.set(0, 0, 0);
    scene.add(currentObject);
    document.getElementById('object-display').innerText = objects[currentObjectIndex].name;
};

window.previousObject = function () {
    scene.remove(currentObject);
    currentObjectIndex = (currentObjectIndex - 1 + objects.length) % objects.length;
    currentObject = objects[currentObjectIndex].mesh;
    currentObject.rotation.set(0, 0, 0);
    scene.add(currentObject);
    document.getElementById('object-display').innerText = objects[currentObjectIndex].name;
};

window.setZoomValue = function (val) {
    targetZoom = val;
};

window.jumpToObject = function (name) {
    const index = objects.findIndex(obj => obj.name.toLowerCase() === name.toLowerCase());
    if (index !== -1 && index !== currentObjectIndex) {
        scene.remove(currentObject);
        currentObjectIndex = index;
        currentObject = objects[currentObjectIndex].mesh;
        currentObject.rotation.set(0, 0, 0);
        scene.add(currentObject);
        document.getElementById('object-display').innerText = objects[currentObjectIndex].name;
        return true;
    }
    return false;
};

window.setObjectAndRotate = function (count) {
    if (count === 0) {
        isRotating = false;
    } else if (count >= 1 && count <= 10) {
        let targetIndex = count - 1;
        if (currentObjectIndex !== targetIndex) {
            scene.remove(currentObject);
            currentObjectIndex = targetIndex;
            currentObject = objects[currentObjectIndex].mesh;
            currentObject.rotation.set(0, 0, 0);
            scene.add(currentObject);
            document.getElementById('object-display').innerText = objects[currentObjectIndex].name;
        }
        isRotating = true;
    }
};

window.rotateObject = function () {
    isRotating = true;
    autoRotateSpeed.y = 0.02;
};

window.rotateLeft = function () {
    isRotating = true;
    autoRotateSpeed.y = -0.02; // Reverse direction
};

window.rotateRight = function () {
    isRotating = true;
    autoRotateSpeed.y = 0.02; // Normal direction
};

window.stopObject = function () {
    isRotating = false;
};

window.manualRotate = function (dx, dy) {
    isRotating = false; // Override auto-rotate
    // Reverse dx for mirror effect
    currentObject.rotation.y += -dx * 5.0;
    currentObject.rotation.x += dy * 5.0;
};

// Window resize handler
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// Animation Loop
function animate() {
    requestAnimationFrame(animate);

    if (isRotating) {
        currentObject.rotation.y += autoRotateSpeed.y;
        currentObject.rotation.x += autoRotateSpeed.x;
    }

    // Smooth camera zoom
    camera.position.z += (targetZoom - camera.position.z) * 0.1;

    if (!isHologramMode) {
        renderer.setViewport(0, 0, window.innerWidth, window.innerHeight);
        renderer.setScissorTest(false);
        renderer.render(scene, camera);
    } else {
        // Hologram 4-split view
        renderer.setScissorTest(true);

        const w = window.innerWidth;
        const h = window.innerHeight;
        const size = Math.min(w, h) / 3;
        const cx = w / 2;
        const cy = h / 2;
        const offset = size / 2;

        // Bottom view (holoCameras[0] - +Z)
        renderer.setViewport(cx - size / 2, cy - offset - size, size, size);
        renderer.setScissor(cx - size / 2, cy - offset - size, size, size);
        holoCameras[0].position.z += (targetZoom - holoCameras[0].position.z) * 0.1;
        // Rotation for screen
        holoCameras[0].up.set(0, 1, 0);
        holoCameras[0].lookAt(0, 0, 0);
        renderer.render(scene, holoCameras[0]);

        // Right view (holoCameras[1] - +X)
        renderer.setViewport(cx + offset, cy - size / 2, size, size);
        renderer.setScissor(cx + offset, cy - size / 2, size, size);
        holoCameras[1].position.x += (targetZoom - holoCameras[1].position.x) * 0.1;
        // Rotate 90 deg counter-clockwise visually
        holoCameras[1].up.set(1, 0, 0);
        holoCameras[1].lookAt(0, 0, 0);
        renderer.render(scene, holoCameras[1]);

        // Top view (holoCameras[2] - -Z)
        renderer.setViewport(cx - size / 2, cy + offset, size, size);
        renderer.setScissor(cx - size / 2, cy + offset, size, size);
        holoCameras[2].position.z += (-targetZoom - holoCameras[2].position.z) * 0.1;
        // Upside down
        holoCameras[2].up.set(0, -1, 0);
        holoCameras[2].lookAt(0, 0, 0);
        renderer.render(scene, holoCameras[2]);

        // Left view (holoCameras[3] - -X)
        renderer.setViewport(cx - offset - size, cy - size / 2, size, size);
        renderer.setScissor(cx - offset - size, cy - size / 2, size, size);
        holoCameras[3].position.x += (-targetZoom - holoCameras[3].position.x) * 0.1;
        // Rotate 90 deg clockwise visually
        holoCameras[3].up.set(-1, 0, 0);
        holoCameras[3].lookAt(0, 0, 0);
        renderer.render(scene, holoCameras[3]);
    }
}

animate();
