// 🔹 Agregar un evento al botón con id "classifyButton" para ejecutar la función classifyImage al hacer clic
document.getElementById("classifyButton").addEventListener("click", classifyImage);

// 🔹 Función para clasificar la imagen
function classifyImage() {
    // 🔹 Obtener el elemento de entrada de archivo (file input)
    let fileInput = document.getElementById("fileInput");
    // 🔹 Obtener el archivo seleccionado por el usuario
    let file = fileInput.files[0];

    // 🔹 Validar si el usuario subió un archivo
    if (!file) {
        alert("Por favor, sube una imagen primero."); // Mostrar alerta si no hay archivo
        return; // Salir de la función
    }

    // 🔹 Crear un objeto FormData para enviar el archivo al backend
    let formData = new FormData();
    formData.append("file", file); // Adjuntar la imagen al formulario

    // 🔹 Enviar la imagen al servidor usando la API fetch
    fetch("http://localhost:8000/predict/", {
        method: "POST",  // Método HTTP POST para enviar datos
        body: formData    // Enviar el objeto FormData con la imagen
    })
    .then(response => response.json()) // Convertir la respuesta en formato JSON
    .then(data => {
        // 🔹 Mostrar la imagen subida en el frontend
        let imgElement = document.getElementById("previewImage"); // Obtener el elemento de imagen
        imgElement.src = URL.createObjectURL(file); // Crear una URL temporal de la imagen subida
        imgElement.style.display = "block"; // Asegurar que la imagen sea visible

        // 🔹 Mostrar los resultados de clasificación en la interfaz
        let resultElement = document.getElementById("result"); // Obtener el contenedor de resultados
        resultElement.innerHTML = ""; // Limpiar resultados anteriores antes de agregar nuevos

        // 🔹 Iterar sobre las predicciones recibidas y mostrarlas en el frontend
        data.predictions.forEach(pred => {
            let resultItem = document.createElement("div"); // Crear un nuevo div para cada resultado
            resultItem.classList.add("result-item"); // Agregar una clase CSS para el estilo
            // 🔹 Formatear el resultado con etiqueta y porcentaje
            resultItem.innerHTML = `<strong>${pred.label}:</strong> ${pred.probability.toFixed(2)}%`;
            resultElement.appendChild(resultItem); // Agregar el resultado al contenedor de resultados
        });
    })
    .catch(error => console.error("Error:", error)); // Capturar y mostrar errores en la consola
}
