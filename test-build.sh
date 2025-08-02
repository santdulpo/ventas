#!/bin/bash

echo "🧪 Probando build del frontend..."

cd frontend

echo "📦 Instalando dependencias..."
npm install

echo "🔨 Ejecutando build..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Build exitoso!"
    echo "📂 Archivos generados en frontend/dist/"
    ls -la dist/
else
    echo "❌ Error en el build"
    exit 1
fi

echo "🎉 Todo listo para Netlify!"